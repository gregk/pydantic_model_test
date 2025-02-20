"""
Model evaluation script for testing different LLM providers and models.

This module provides a framework for testing different LLM models with standardized test cases.
It checks model capabilities before running tests and tracks test results and model capabilities.

Usage:
    python model_test.py --help
    python model_test.py --list-providers
    python model_test.py --run-tests
    python model_test.py --show-history
"""

import argparse
import asyncio
import json
import os
from datetime import datetime, UTC
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import logfire
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from model_utils import (
    KnownModelName,
    get_model_by_provider,
    get_latest_model,
    get_model_info
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logfire.configure()

class TestScenario(str, Enum):
    """Available test scenarios."""
    STANDARD = "standard"  # Basic markdown and reasoning tests
    MULTI_FILE = "multi-file"  # Tests involving multiple file generation

class ModelCapabilities(BaseModel):
    """Model capabilities tracking."""
    tools: bool = False
    function_calling: bool = False
    json_mode: bool = False
    system_prompt: bool = True
    vision: bool = False
    audio: bool = False

class ModelInfo(BaseModel):
    """Model information response format."""
    name: str = Field(..., description="The name of the model")
    version: str = Field(..., description="The version of the model")

class TestCase(BaseModel):
    """A single test case for model evaluation."""
    name: str
    prompt: str
    expected_type: str = "text"  # text, json, code
    system_prompt: str
    result_type: type
    validation_rules: Optional[Dict[str, str]] = None
    timeout: int = 30  # seconds
    retries: int = 2
    required_capabilities: List[str] = []  # List of required capabilities for this test

class TestResult(BaseModel):
    """Results from running a test case."""
    model: str
    test_case: str
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    duration: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ModelTestHistory(BaseModel):
    """Historical test results for a model."""
    model: str
    provider: str
    base_name: str
    capabilities: ModelCapabilities
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    failure_count: int = 0
    success_count: int = 0
    known_issues: List[str] = []

# Standard test cases
STANDARD_TESTS = [
    TestCase(
        name="basic_response",
        prompt="What is 2+2? Show your work in markdown format.",
        expected_type="markdown",
        system_prompt="You are a helpful math tutor. Explain your work step by step in markdown format.",
        result_type=str,
        validation_rules={"pattern": r"^#.*2.*\+.*2.*=.*4"},
        required_capabilities=["system_prompt"]
    ),
    TestCase(
        name="markdown_structure",
        prompt='Explain what a binary search tree is. Use proper markdown formatting with headers, bullet points, and code examples.',
        expected_type="markdown",
        system_prompt="You are a computer science teacher. Explain concepts using clear markdown formatting with headers, lists, and code examples.",
        result_type=str,
        validation_rules={"pattern": r"#.*\n.*\*.*\n.*```"},
        required_capabilities=["system_prompt"]
    ),
    TestCase(
        name="code_generation",
        prompt="Write a Python function that adds two numbers. Format your response in markdown with explanation and code block.",
        expected_type="markdown",
        system_prompt="You are a code instructor. Write clean, simple Python code with explanations in markdown format. Include docstrings and type hints.",
        result_type=str,
        validation_rules={"pattern": r"#.*\n.*```python"},
        required_capabilities=["system_prompt"]
    ),
    TestCase(
        name="reasoning",
        prompt="If a train travels 120 kilometers in 2 hours, what is its speed in kilometers per hour? Format your response in markdown with clear steps.",
        expected_type="markdown",
        system_prompt="You are a physics teacher. Break down problems step by step using markdown formatting with headers and bullet points.",
        result_type=str,
        validation_rules={"pattern": r"#.*\n.*\*"},
        required_capabilities=["system_prompt"]
    )
]

# Multi-file test cases
MULTI_FILE_TESTS = [
    TestCase(
        name="key_value_store",
        prompt="""Create a Python implementation of a key-value store with the following requirements:

1. An abstract interface defining the basic operations
2. A local file-based implementation
3. A Redis implementation

Use proper Python type hints, docstrings, and error handling.
Format your response in markdown with separate code blocks for each file.
Include a brief explanation before each file.

Required files:
- src/store/interfaces/key_value_store.py
- src/store/implementations/local_store.py
- src/store/implementations/redis_store.py
""",
        expected_type="markdown",
        system_prompt="""You are a senior Python developer creating a modular key-value store system.
Follow these guidelines:
1. Use abstract base classes for interfaces
2. Include comprehensive type hints
3. Add detailed docstrings for all classes and methods
4. Implement proper error handling
5. Format the response in markdown with clear headers and code blocks
6. Add brief explanations before each file
7. Ensure implementations properly inherit from the interface""",
        result_type=str,
        validation_rules={
            "pattern": r"#.*\n.*```python.*class.*ABC.*\n.*```.*\n.*```python.*class.*Store.*\n.*```.*\n.*```python.*class.*Redis.*\n.*```"
        },
        required_capabilities=["system_prompt"]
    )
]

class ModelTester:
    """Handles testing of different models and recording results."""
    
    def __init__(self, scenario: TestScenario = TestScenario.STANDARD):
        """Initialize the model tester.
        
        Args:
            scenario: The test scenario to run
        """
        self.scenario = scenario
        self.results_dir = Path("test_results")
        self.markdown_dir = Path("test_results/markdown")
        self.results_dir.mkdir(exist_ok=True)
        self.markdown_dir.mkdir(exist_ok=True)
        self.history_file = self.results_dir / "test_history.json"
        self.test_history: Dict[str, ModelTestHistory] = self._load_history()
        
        # Select test cases based on scenario
        if scenario == TestScenario.STANDARD:
            self.test_cases = STANDARD_TESTS
        else:
            self.test_cases = MULTI_FILE_TESTS
        
        # Available providers based on environment
        self.available_providers = set()
        self.provider_keys = {}  # Track which providers have valid keys
        self.missing_providers = set()  # Track which providers are missing keys
        
        # Define all supported providers
        self.all_providers = {
            # Major providers
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google-gla": "GEMINI_API_KEY",
            "google-vertex": "GEMINI_API_KEY",
            # Additional providers
            "mistral": "MISTRAL_API_KEY",
            "fireworks": "FIREWORKS_API_KEY",
            "groq": "GROQ_API_KEY",
            "cohere": "COHERE_API_KEY",
            # Meta providers
            "openrouter": "OPENROUTER_API_KEY"
        }
        
        # Check each provider
        for provider, env_var in self.all_providers.items():
            if (key := os.getenv(env_var)) and key.strip():
                self.available_providers.add(provider)
                self.provider_keys[provider] = key
            else:
                self.missing_providers.add(provider)

    def _load_history(self) -> Dict[str, ModelTestHistory]:
        """Load test history from file."""
        if not self.history_file.exists():
            return {}
        
        try:
            with open(self.history_file) as f:
                data = json.load(f)
                history_dict = {}
                
                for model, history in data.items():
                    try:
                        # Get model info for missing fields
                        model_info = get_model_info(model)
                        
                        # Update history with required fields
                        history.update({
                            "provider": model_info["provider"],
                            "base_name": model_info["base_name"],
                            "capabilities": model_info["capabilities"]
                        })
                        
                        history_dict[model] = ModelTestHistory(**history)
                    except Exception as e:
                        print(f"Warning: Could not load history for {model}: {str(e)}")
                        continue
                
                return history_dict
                
        except Exception as e:
            print(f"Warning: Could not load test history: {str(e)}")
            return {}

    def _save_history(self):
        """Save test history to file."""
        with open(self.history_file, "w") as f:
            json.dump(
                {model: history.model_dump() for model, history in self.test_history.items()},
                f,
                indent=2,
                default=str
            )

    def _get_latest_models(self) -> List[KnownModelName]:
        """Get list of latest models from available providers, eliminating duplicates and preferring prefixed versions."""
        latest_models = []
        seen_base_names = set()
        
        # Add Claude-3-Sonnet
        if "anthropic" in self.available_providers:
            latest_models.append("anthropic:claude-3-5-sonnet-latest")
            seen_base_names.add("claude-3-5-sonnet")
        
        # Add specific Groq models
        if "groq" in self.available_providers:
            priority_groq_models = [
                "groq:deepseek-r1-distill-llama-70b-specdec",
                "groq:qwen-2.5-coder-32b"
            ]
            for model in priority_groq_models:
                model_info = get_model_info(model)
                base_name = model_info["base_name"]
                if base_name not in seen_base_names:
                    latest_models.append(model)
                    seen_base_names.add(base_name)
        
        return latest_models

    def _can_run_test(self, model_info: Dict[str, Any], test_case: TestCase) -> bool:
        """Check if a model has the required capabilities for a test."""
        capabilities = model_info["capabilities"]
        return all(capabilities.get(cap, False) for cap in test_case.required_capabilities)

    async def run_test(self, model: str, test_case: TestCase) -> TestResult:
        """Run a single test case against a model."""
        start_time = datetime.now(UTC)
        try:
            # Get model info
            model_info = get_model_info(model)
            
            # Check if model can run this test
            if not self._can_run_test(model_info, test_case):
                print(f"  ⚠️  Skipping {test_case.name} - Model lacks capabilities: {test_case.required_capabilities}")
                return TestResult(
                    model=model,
                    test_case=test_case.name,
                    success=False,
                    error=f"Model lacks required capabilities: {test_case.required_capabilities}",
                    duration=0
                )
            
            print(f"  🔄 Running {test_case.name}...")
            
            # Create agent with model
            agent = Agent(
                model,
                result_type=test_case.result_type,
                system_prompt=test_case.system_prompt
            )
            
            # Run test asynchronously
            response = await agent.run(test_case.prompt)
            
            duration = (datetime.now(UTC) - start_time).total_seconds()
            
            # Print success with timing
            print(f"  ✓ {test_case.name} completed in {duration:.1f}s")
            print(f"    Response: {str(response.data)[:100]}..." if len(str(response.data)) > 100 else f"    Response: {response.data}")
            
            return TestResult(
                model=model,
                test_case=test_case.name,
                success=True,
                response=str(response.data),
                duration=duration
            )
            
        except Exception as e:
            duration = (datetime.now(UTC) - start_time).total_seconds()
            error_msg = str(e)
            
            # Print failure with timing
            print(f"  ✗ {test_case.name} failed in {duration:.1f}s")
            print(f"    Error: {error_msg}")
            
            return TestResult(
                model=model,
                test_case=test_case.name,
                success=False,
                error=error_msg,
                duration=duration
            )

    async def test_model(self, model: KnownModelName) -> List[TestResult]:
        """Run all test cases for a model."""
        results = []
        
        # Get model info
        model_info = get_model_info(model)
        
        # Initialize or update model history with capabilities
        if model not in self.test_history:
            self.test_history[model] = ModelTestHistory(
                model=model,
                provider=model_info["provider"],
                base_name=model_info["base_name"],
                capabilities=ModelCapabilities(**model_info["capabilities"])
            )
        
        print(f"\nTesting {model}:")
        print("Provider:", model_info["provider"])
        print("Base Name:", model_info["base_name"])
        print("\nRunning tests:")
        
        # Run tests with rate limiting
        for test_case in self.test_cases:
            # Add small delay between tests to avoid rate limits
            await asyncio.sleep(0.5)  # 500ms delay between tests
            
            result = await self.run_test(model, test_case)
            results.append(result)
            
            # Update history
            history = self.test_history[model]
            if result.success:
                history.last_success = result.timestamp
                history.success_count += 1
            else:
                history.last_failure = result.timestamp
                history.failure_count += 1
                if result.error:
                    history.known_issues.append(result.error)
        
        # Print test summary for this model
        success_count = sum(1 for r in results if r.success)
        print(f"\nModel Summary:")
        print(f"Tests passed: {success_count}/{len(results)}")
        print(f"Success rate: {(success_count/len(results))*100:.1f}%")
        
        return results

    def _clean_model_name(self, model: str) -> str:
        """Clean model name for file naming.
        
        Args:
            model: Full model name with optional provider prefix
            
        Returns:
            Clean model name without provider prefix
        """
        # Handle provider prefix if present
        if ":" in model:
            provider, base_name = model.split(":", 1)
        else:
            # Assume OpenAI if no provider specified
            base_name = model
            
        # Remove any "latest" suffix
        base_name = base_name.replace("-latest", "")
        
        return base_name

    def save_results(self, model: str, results: List[TestResult]):
        """Save test results to files.
        
        Saves both JSON results and markdown content.
        """
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        result_file = self.results_dir / f"{model}_{timestamp}.json"
        with open(result_file, "w") as f:
            json.dump(
                [result.model_dump() for result in results],
                f,
                indent=2,
                default=str
            )
        
        # Save markdown content
        clean_name = self._clean_model_name(model)
        for result in results:
            if result.success and result.response:
                # Create markdown file with clean model name
                md_file = self.markdown_dir / f"{clean_name}.md"
                
                # Add metadata header
                metadata = {
                    "model": model,
                    "test_case": result.test_case,
                    "timestamp": timestamp,
                    "duration": f"{result.duration:.2f}s"
                }
                
                with open(md_file, "w") as f:
                    # Write metadata as YAML frontmatter
                    f.write("---\n")
                    for key, value in metadata.items():
                        f.write(f"{key}: {value}\n")
                    f.write("---\n\n")
                    # Write the actual response
                    f.write(result.response)

    def _generate_capability_table(self, models_info: List[tuple[str, Dict[str, Any]]]) -> str:
        """Generate a markdown table of model capabilities.
        
        Args:
            models_info: List of tuples containing (model_name, model_info)
            
        Returns:
            Markdown formatted table string
        """
        # Get all capability names
        capabilities = ["tools", "function_calling", "json_mode", "system_prompt", "vision", "audio"]
        
        # Build header
        header = "| Model | " + " | ".join(cap.replace("_", " ").title() for cap in capabilities) + " |"
        separator = "|" + "|".join("---" for _ in range(len(capabilities) + 1)) + "|"
        
        # Build rows
        rows = []
        for model, info in models_info:
            caps = info["capabilities"]
            row = [
                model,
                *["✓" if caps.get(cap, False) else "✗" for cap in capabilities]
            ]
            rows.append("| " + " | ".join(row) + " |")
        
        # Combine all parts
        return "\n".join([header, separator] + rows)

    def _check_provider_availability(self) -> None:
        """Check and warn about provider availability."""
        if not self.available_providers:
            print("\n⚠️  WARNING: No API keys found for any providers!")
            print("Please set at least one of the following environment variables:")
            for provider, env_var in self.all_providers.items():
                print(f"  • {env_var} for {provider}")
            return

        print("\nProvider Status:")
        print("=" * 50)
        
        # Group providers by category
        categories = {
            "Major Providers": ["anthropic", "openai", "google-gla", "google-vertex"],
            "Additional Providers": ["mistral", "fireworks", "groq", "cohere"],
            "Meta Providers": ["openrouter"]
        }
        
        for category, providers in categories.items():
            print(f"\n{category}:")
            for provider in providers:
                status = "✓" if provider in self.available_providers else "✗"
                env_var = self.all_providers[provider]
                print(f"  {status} {provider:<15} ({env_var})")
                
                # Special notes for meta-providers that can access other models
                if provider == "groq" and provider in self.missing_providers:
                    print("    Note: GROQ can provide fast access to some Anthropic and Mistral models")
                elif provider == "openrouter" and provider in self.missing_providers:
                    print("    Note: OpenRouter can provide access to most major models")
        
        # Warn about potential limitations
        if "anthropic" in self.missing_providers and "groq" in self.missing_providers:
            print("\n⚠️  No access to Claude models (need either ANTHROPIC_API_KEY or GROQ_API_KEY)")
        if "openai" in self.missing_providers and "openrouter" in self.missing_providers:
            print("\n⚠️  No access to GPT models (need either OPENAI_API_KEY or OPENROUTER_API_KEY)")
        if "google-gla" in self.missing_providers and "google-vertex" in self.missing_providers:
            print("\n⚠️  No access to Gemini models (need GEMINI_API_KEY)")
        if "mistral" in self.missing_providers and "groq" in self.missing_providers:
            print("\n⚠️  No access to Mistral models (need either MISTRAL_API_KEY or GROQ_API_KEY)")

    def _generate_metrics_table(self, all_results: Dict[str, List[TestResult]]) -> str:
        """Generate a detailed metrics table for all models.
        
        Args:
            all_results: Dictionary mapping model names to their test results
            
        Returns:
            Markdown formatted table with metrics
        """
        headers = [
            "Model",
            "Test Case",
            "Success",
            "Duration (s)",
            "Response Length",
            "Has Headers",
            "Has Lists",
            "Has Code Blocks"
        ]
        
        separator = "|" + "|".join("---" for _ in range(len(headers))) + "|"
        header_row = "| " + " | ".join(headers) + " |"
        
        rows = []
        for model, results in all_results.items():
            model_metrics = {
                "total_duration": 0,
                "total_success": 0,
                "avg_response_length": 0
            }
            
            for result in results:
                if not result.success:
                    continue
                    
                response = result.response or ""
                has_headers = "#" in response
                has_lists = "*" in response or "-" in response
                has_code = "```" in response
                
                row = [
                    model,
                    result.test_case,
                    "✓" if result.success else "✗",
                    f"{result.duration:.2f}",
                    str(len(response)),
                    "✓" if has_headers else "✗",
                    "✓" if has_lists else "✗",
                    "✓" if has_code else "✗"
                ]
                rows.append("| " + " | ".join(row) + " |")
                
                # Update metrics
                model_metrics["total_duration"] += result.duration
                model_metrics["total_success"] += 1
                model_metrics["avg_response_length"] += len(response)
            
            # Add summary row for model
            if results:
                avg_duration = model_metrics["total_duration"] / len(results)
                success_rate = (model_metrics["total_success"] / len(results)) * 100
                avg_length = model_metrics["avg_response_length"] / len(results)
                
                summary_row = [
                    f"{model} (Summary)",
                    "ALL",
                    f"{success_rate:.1f}%",
                    f"{avg_duration:.2f}",
                    f"{avg_length:.0f}",
                    "-",
                    "-",
                    "-"
                ]
                rows.append("| " + " | ".join(summary_row) + " |")
                rows.append(separator)
        
        return "\n".join([header_row, separator] + rows)

    def _generate_speed_ranking(self, all_results: Dict[str, List[TestResult]]) -> str:
        """Generate a speed ranking summary for all models.
        
        Args:
            all_results: Dictionary mapping model names to their test results
            
        Returns:
            Markdown formatted speed ranking table
        """
        # Calculate speed metrics for each model
        speed_metrics = []
        for model, results in all_results.items():
            metrics = {
                "model": model,
                "avg_duration": sum(r.duration for r in results) / len(results),
                "min_duration": min(r.duration for r in results),
                "max_duration": max(r.duration for r in results),
                "total_duration": sum(r.duration for r in results)
            }
            speed_metrics.append(metrics)
        
        # Sort by average duration (faster first)
        speed_metrics.sort(key=lambda x: x["avg_duration"])
        
        # Generate table
        headers = [
            "Rank",
            "Model",
            "Avg Time (s)",
            "Min Time (s)",
            "Max Time (s)",
            "Total Time (s)",
            "Relative Speed"
        ]
        
        header_row = "| " + " | ".join(headers) + " |"
        separator = "|" + "|".join("---" for _ in range(len(headers))) + "|"
        
        # Calculate relative speed compared to slowest
        slowest_avg = max(m["avg_duration"] for m in speed_metrics)
        
        rows = []
        for rank, metrics in enumerate(speed_metrics, 1):
            relative_speed = slowest_avg / metrics["avg_duration"]
            row = [
                str(rank),
                metrics["model"],
                f"{metrics['avg_duration']:.2f}",
                f"{metrics['min_duration']:.2f}",
                f"{metrics['max_duration']:.2f}",
                f"{metrics['total_duration']:.2f}",
                f"{relative_speed:.1f}x faster"
            ]
            rows.append("| " + " | ".join(row) + " |")
        
        return "\n".join([
            "\n## Speed Rankings (Lower is Better)",
            header_row,
            separator
        ] + rows)

    def save_test_summary(self, all_results: Dict[str, List[TestResult]], timestamp: str) -> str:
        """Save test results summary to a markdown file.
        
        Args:
            all_results: Dictionary mapping model names to their test results
            timestamp: Timestamp for the filename
            
        Returns:
            Path to the created markdown file
        """
        # Create markdown directory if it doesn't exist
        markdown_dir = Path("test_results/markdown")
        markdown_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp
        filename = f"model_test_summary_{timestamp}.md"
        filepath = markdown_dir / filename
        
        with open(filepath, "w") as f:
            # Write header
            f.write("# Model Test Results Summary\n\n")
            f.write(f"Test run: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
            
            # Write metrics table
            f.write("## Detailed Metrics\n\n")
            f.write(self._generate_metrics_table(all_results))
            f.write("\n\n")
            
            # Write speed rankings
            f.write("## Speed Rankings (Lower is Better)\n\n")
            f.write(self._generate_speed_ranking(all_results))
        
        return str(filepath)

    async def run_all_tests(self, failed_only: bool = False):
        """Run tests for all available models concurrently while tracking individual progress."""
        # Check provider availability first
        self._check_provider_availability()
        
        if not self.available_providers:
            print("\n❌ Cannot proceed with testing - no API keys available.")
            return
            
        # Get latest models from each provider
        latest_models = self._get_latest_models()
        
        if not latest_models:
            print("\n❌ No models available for testing with current API keys.")
            return
        
        print(f"\nPreparing to test {len(latest_models)} models:")
        for model in latest_models:
            print(f"  • {model}")
        
        # Group models by provider for clearer output
        models_info = []  # Store model info for table generation
        for model in sorted(latest_models):
            model_info = get_model_info(model)
            models_info.append((model, model_info))
        
        # Print capability table
        print("\nModel Capabilities:")
        print(self._generate_capability_table(models_info))
        
        print("\nStarting concurrent model testing...")
        print("=" * 80)
        
        # Run all tests concurrently
        test_tasks = [
            self.test_model(model)
            for model in sorted(latest_models)
        ]
        
        # Wait for all tests to complete
        results = await asyncio.gather(*test_tasks, return_exceptions=True)
        
        # Collect all results
        all_results = {}
        for model, model_results in zip(latest_models, results):
            if isinstance(model_results, Exception):
                print(f"\nError testing {model}: {str(model_results)}")
                continue
            all_results[model] = model_results
            # Save results for each model
            self.save_results(model, model_results)
        
        print("\n" + "=" * 80)
        print("Testing completed. Detailed Metrics:\n")
        print(self._generate_metrics_table(all_results))
        
        # Add speed ranking
        print("\nSpeed Performance Summary:")
        print(self._generate_speed_ranking(all_results))
        
        # Save updated history
        self._save_history()

        # Generate timestamp for filename
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        
        # Save results to markdown file
        summary_file = self.save_test_summary(all_results, timestamp)
        print(f"\nTest summary saved to: {summary_file}")


def get_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser.
    
    Returns:
        ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Test LLM models and track results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Show available providers and their status
    python model_test.py --list-providers
    
    # Run tests with all available models
    python model_test.py --run-tests
    
    # Run tests with specific providers
    python model_test.py --run-tests --providers anthropic openai
    
    # Show test history for all models
    python model_test.py --show-history
    
    # Run only failed tests
    python model_test.py --run-tests --failed-only
    
    # Run specific test scenario
    python model_test.py --run-tests --scenario multi-file
    """
    )
    
    # Create mutually exclusive group for main commands
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run-tests",
        action="store_true",
        help="Run model tests"
    )
    group.add_argument(
        "--list-providers",
        action="store_true",
        help="List available providers and their status"
    )
    group.add_argument(
        "--show-history",
        action="store_true",
        help="Show test history for all models"
    )
    group.add_argument(
        "--help-verbose",
        action="store_true",
        help="Show detailed help information"
    )
    
    # Optional arguments
    parser.add_argument(
        "--providers",
        nargs="+",
        choices=["anthropic", "openai", "google-gla", "google-vertex", 
                "mistral", "fireworks", "groq", "cohere", "openrouter"],
        help="Specific providers to test (default: all available)"
    )
    parser.add_argument(
        "--failed-only",
        action="store_true",
        help="Only test models that have failed before"
    )
    parser.add_argument(
        "--scenario",
        type=TestScenario,
        choices=list(TestScenario),
        default=TestScenario.STANDARD,
        help="Test scenario to run (default: standard)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="test_results",
        help="Directory for test results (default: test_results)"
    )
    parser.add_argument(
        "--concurrent",
        action="store_true",
        help="Run tests concurrently across models"
    )
    
    return parser

def show_verbose_help():
    """Show detailed help information about the script."""
    print("""
Model Test Script - Detailed Help
===============================

Description:
-----------
This script provides a framework for testing different LLM models with standardized
test cases. It supports multiple providers and can track test results over time.

Dependencies:
------------
- Python 3.9+
- Required packages: see requirements.txt
- API keys: see .env-template for required environment variables

Test Scenarios:
-------------
1. Standard:
   - Basic markdown formatting
   - Reasoning capabilities
   - Code generation
   - Mathematical problem solving

2. Multi-file:
   - Complex code generation
   - Multiple file handling
   - Interface/implementation patterns

Provider Support:
---------------
Major Providers:
- Anthropic (Claude models)
- OpenAI (GPT models)
- Google (Gemini models)

Additional Providers:
- Mistral
- Fireworks
- Groq
- Cohere

Meta Providers:
- OpenRouter (access to multiple models)

Configuration:
------------
1. Copy .env-template to .env
2. Add your API keys
3. (Optional) Configure custom API endpoints

Results:
-------
Test results are saved in:
- JSON format (for programmatic analysis)
- Markdown format (for human reading)
- Historical tracking (for performance over time)

Examples:
--------
# Run standard tests with all available providers:
python model_test.py --run-tests

# Test specific providers:
python model_test.py --run-tests --providers anthropic openai

# Run multi-file test scenario:
python model_test.py --run-tests --scenario multi-file

# Show test history:
python model_test.py --show-history
""")

async def main():
    """Main entry point for model testing."""
    parser = get_parser()
    args = parser.parse_args()
    
    if args.help_verbose:
        show_verbose_help()
        return
    
    # Initialize tester with scenario and output directory
    tester = ModelTester(
        scenario=args.scenario
    )
    
    if args.list_providers:
        tester._check_provider_availability()
        return
        
    if args.show_history:
        print("\nTest History:")
        for model, history in sorted(tester.test_history.items()):
            print(f"\n{model}:")
            print(f"  Provider: {history.provider}")
            print(f"  Base Name: {history.base_name}")
            print("  Capabilities:")
            for cap, supported in history.capabilities.dict().items():
                print(f"    • {cap}: {'✓' if supported else '✗'}")
            print(f"  Success Rate: {history.success_count}/{history.success_count + history.failure_count}")
            if history.last_success:
                print(f"  Last Success: {history.last_success}")
            if history.last_failure:
                print(f"  Last Failure: {history.last_failure}")
            if history.known_issues:
                print("  Known Issues:")
                for issue in history.known_issues[-3:]:  # Show last 3 issues
                    print(f"    • {issue}")
        return
    
    if args.run_tests:
        # Filter providers if specified
        if args.providers:
            tester.available_providers = {p for p in args.providers if p in tester.available_providers}
        
        await tester.run_all_tests(failed_only=args.failed_only)

if __name__ == "__main__":
    asyncio.run(main()) 