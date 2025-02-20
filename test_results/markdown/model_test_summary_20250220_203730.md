# Model Test Results Summary

Test run: 2025-02-20 20:37:30 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 2.38 | 311 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 8.58 | 2175 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 3.85 | 973 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 2.39 | 455 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 4.30 | 978 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.85 | 561 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.36 | 6592 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.89 | 1669 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.90 | 2435 | ✓ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 1.00 | 2814 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 1.17 | 631 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 2.43 | 3390 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.29 | 1572 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 0.78 | 631 | ✓ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.42 | 1556 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 1.00 | 0.85 | 1.36 | 4.01 | 4.3x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.42 | 0.78 | 2.43 | 5.67 | 3.0x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 4.30 | 2.38 | 8.58 | 17.20 | 1.0x faster |