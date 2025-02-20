# Model Test Results Summary

Test run: 2025-02-20 21:01:21 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 3.70 | 375 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 10.11 | 2018 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 5.92 | 960 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 3.39 | 544 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 5.78 | 974 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.76 | 561 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.36 | 6592 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.68 | 2460 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.75 | 2435 | ✓ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 0.89 | 3012 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 0.86 | 746 | ✗ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 3.02 | 3919 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.13 | 1316 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 0.85 | 662 | ✓ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.47 | 1661 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 0.89 | 0.68 | 1.36 | 3.55 | 6.5x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.47 | 0.85 | 3.02 | 5.86 | 3.9x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 5.78 | 3.39 | 10.11 | 23.12 | 1.0x faster |