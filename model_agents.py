"""
Model-specific agent implementations using pydantic_ai.

This module provides agent implementations for different LLM providers.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from datetime import datetime, UTC
import os

class TestResponse(BaseModel):
    """Structured response from test runs."""
    content: str = Field(..., description="The model's response")
    duration: float = Field(..., description="Time taken to generate response in seconds")

def create_test_agent(model_name: str, api_key: Optional[str] = None) -> Agent:
    """Create an agent for testing.
    
    Args:
        model_name: Full model name (e.g., 'groq:deepseek-r1-distill-llama-70b')
        api_key: Optional API key (will use environment variable if not provided)
        
    Returns:
        Configured Agent instance
    """
    # Set environment variable for the API key if provided
    if api_key:
        provider = model_name.split(':')[0]
        env_var = f"{provider.upper()}_API_KEY"
        os.environ[env_var] = api_key

    return Agent(
        model=model_name,
        result_type=str,  # We want raw string responses for tests
        system_prompt="You are a helpful assistant."  # Default system prompt
    )

async def run_test(agent: Agent, system_prompt: str, user_prompt: str) -> TestResponse:
    """Run a test with the agent.
    
    Args:
        agent: The agent to test with
        system_prompt: The system prompt to use
        user_prompt: The user prompt to test
        
    Returns:
        TestResponse containing the response and metrics
    """
    start_time = datetime.now(UTC)
    try:
        # Update system prompt for this test
        agent.system_prompt = system_prompt
        
        result = await agent.run(user_prompt)
        
        duration = (datetime.now(UTC) - start_time).total_seconds()
        if duration == 0:
            duration = 0.001  # Minimum duration to avoid division by zero
        
        return TestResponse(
            content=result.data,  # Using .data for run() response
            duration=duration
        )
    except Exception as e:
        duration = (datetime.now(UTC) - start_time).total_seconds()
        if duration == 0:
            duration = 0.001
        
        return TestResponse(
            content=f"Error: {str(e)}",
            duration=duration
        ) 