# Model Test Results Summary

Test run: 2025-02-20 21:03:08 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 3.21 | 424 | ✗ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 7.68 | 2077 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 3.79 | 961 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 2.67 | 433 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 4.34 | 974 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.95 | 561 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.37 | 6592 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.70 | 2460 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.88 | 2770 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 0.98 | 3096 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 1.10 | 759 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 2.55 | 3698 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.40 | 1846 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 0.97 | 822 | ✓ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.50 | 1781 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 0.98 | 0.70 | 1.37 | 3.90 | 4.4x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.50 | 0.97 | 2.55 | 6.01 | 2.9x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 4.34 | 2.67 | 7.68 | 17.36 | 1.0x faster |