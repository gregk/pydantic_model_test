# Model Test Results Summary

Test run: 2025-02-20 20:40:21 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 2.93 | 384 | ✗ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 7.12 | 1901 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 4.89 | 1238 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 3.88 | 463 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 4.70 | 996 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.73 | 561 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.42 | 6592 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.82 | 2460 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 1.14 | 2435 | ✓ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 1.03 | 3012 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 0.84 | 401 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 3.13 | 4762 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.28 | 1619 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 1.50 | 1369 | ✓ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.69 | 2038 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 1.03 | 0.73 | 1.42 | 4.11 | 4.6x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.69 | 0.84 | 3.13 | 6.74 | 2.8x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 4.70 | 2.93 | 7.12 | 18.81 | 1.0x faster |