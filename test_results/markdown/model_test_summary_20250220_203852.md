# Model Test Results Summary

Test run: 2025-02-20 20:38:52 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 3.80 | 381 | ✗ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 7.25 | 2109 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 4.38 | 1071 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 3.24 | 532 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 4.67 | 1023 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.72 | 561 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.56 | 7209 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 1.18 | 2360 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.76 | 2435 | ✓ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 1.05 | 3141 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 1.29 | 1237 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 2.08 | 2778 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.03 | 1163 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 0.83 | 731 | ✓ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.31 | 1477 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 1.05 | 0.72 | 1.56 | 4.21 | 4.4x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.31 | 0.83 | 2.08 | 5.23 | 3.6x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 4.67 | 3.24 | 7.25 | 18.66 | 1.0x faster |