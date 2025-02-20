# Model Test Results Summary

Test run: 2025-02-20 21:21:36 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 1.81 | 243 | ✗ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 7.84 | 2264 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 3.73 | 968 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 2.14 | 334 | ✓ | ✓ | ✗ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 3.88 | 952 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.98 | 475 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.62 | 7712 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.56 | 1899 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.54 | 744 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 0.92 | 2708 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 0.89 | 137 | ✗ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 2.35 | 3335 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.22 | 1259 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 1.11 | 836 | ✗ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 1.40 | 1392 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 0.92 | 0.54 | 1.62 | 3.69 | 4.2x faster |
| 2 | groq:qwen-2.5-coder-32b | 1.40 | 0.89 | 2.35 | 5.58 | 2.8x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 3.88 | 1.81 | 7.84 | 15.52 | 1.0x faster |