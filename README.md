# Model Test Framework

A framework for testing and comparing different LLM models across providers. Tests models for capabilities, speed, and quality of responses.

## Latest Test Results

From [model_test_summary_20250220_202740.md](test_results/markdown/model_test_summary_20250220_202740.md):

### Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 2.64 | 400 | ✗ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 7.67 | 2093 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 4.70 | 1078 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 2.67 | 475 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 4.42 | 1012 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 1.44 | 657 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.44 | 6592 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.83 | 2460 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.84 | 2356 | ✓ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 1.14 | 3016 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 1.40 | 590 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 2.91 | 4496 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.12 | 1214 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 1.02 | 903 | ✓ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.61 | 1801 | - | - | - |

### Speed Rankings (Lower is Better)

| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 1.14 | 0.83 | 1.44 | 4.55 | 3.9x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.61 | 1.02 | 2.91 | 6.45 | 2.7x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 4.42 | 2.64 | 7.67 | 17.67 | 1.0x faster |

## Features

- Test multiple LLM providers and models
- Standardized test scenarios
- Speed and capability comparisons
- Detailed metrics and history tracking
- Markdown and JSON result output

## Supported Providers

### Major Providers
- Anthropic (Claude models)
- OpenAI (GPT models)
- Google (Gemini models)

### Additional Providers
- Mistral
- Fireworks
- Groq
- Cohere

### Meta Providers
- OpenRouter

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy env.example to .env and add your API keys:
```bash
cp env.example .env
```

## Usage

### Command Line Options
```
usage: model_test.py [-h] [--providers {anthropic,openai,google-gla,google-vertex,mistral,fireworks,groq,cohere,openrouter} [{anthropic,openai,google-gla,google-vertex,mistral,fireworks,groq,cohere,openrouter} ...]]
                     [--failed-only] [--scenario {standard,multi-file}] [--output-dir OUTPUT_DIR] [--concurrent]
                     (--run-tests | --list-providers | --show-history | --help-verbose)

Test LLM models and track results

options:
  -h, --help            show this help message and exit
  --run-tests           Run model tests
  --list-providers      List available providers and their status
  --show-history        Show test history for all models
  --help-verbose        Show detailed help information

  --providers {anthropic,openai,google-gla,google-vertex,mistral,fireworks,groq,cohere,openrouter}
                        Specific providers to test (default: all available)
  --failed-only         Only test models that have failed before
  --scenario {standard,multi-file}
                        Test scenario to run (default: standard)
  --output-dir OUTPUT_DIR
                        Directory for test results (default: test_results)
  --concurrent          Run tests concurrently across models

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
```

## Test Scenarios

### Standard Tests
- Basic markdown formatting
- Reasoning capabilities
- Code generation
- Mathematical problem solving

### Multi-file Tests
- Complex code generation
- Multiple file handling
- Interface/implementation patterns

## Output

Results are saved in:
- `test_results/markdown/` - Human-readable markdown files
- `test_results/*.json` - Machine-readable JSON files
- `test_results/test_history.json` - Historical test data

## License

MIT