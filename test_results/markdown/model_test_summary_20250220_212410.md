# Model Test Results Summary

Test run: 2025-02-20 21:24:10 UTC

## Detailed Metrics

| Model | Test Case | Success | Duration (s) | Response Length | Has Headers | Has Lists | Has Code Blocks |
|---|---|---|---|---|---|---|---|
| anthropic:claude-3-5-sonnet-latest | basic_response | ✓ | 1.75 | 181 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | markdown_structure | ✓ | 8.82 | 2466 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | code_generation | ✓ | 3.52 | 1037 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | reasoning | ✓ | 1.92 | 265 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | complex_code | ✓ | 10.65 | 3978 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | system_design | ✓ | 14.11 | 3342 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest | problem_solving | ✓ | 10.73 | 2800 | ✓ | ✓ | ✓ |
| anthropic:claude-3-5-sonnet-latest (Summary) | ALL | 100.0% | 7.36 | 2010 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:deepseek-r1-distill-llama-70b-specdec | basic_response | ✓ | 0.91 | 569 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | markdown_structure | ✓ | 1.44 | 7073 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | code_generation | ✓ | 0.65 | 1899 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | reasoning | ✓ | 0.57 | 744 | ✗ | ✓ | ✗ |
| groq:deepseek-r1-distill-llama-70b-specdec | complex_code | ✓ | 1.60 | 9172 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | system_design | ✓ | 2.03 | 11686 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec | problem_solving | ✓ | 1.65 | 7844 | ✓ | ✓ | ✓ |
| groq:deepseek-r1-distill-llama-70b-specdec (Summary) | ALL | 100.0% | 1.26 | 5570 | - | - | - |
|---|---|---|---|---|---|---|---|
| groq:qwen-2.5-coder-32b | basic_response | ✓ | 0.72 | 161 | ✗ | ✗ | ✓ |
| groq:qwen-2.5-coder-32b | markdown_structure | ✓ | 1.96 | 2709 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | code_generation | ✓ | 1.08 | 1200 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | reasoning | ✓ | 0.84 | 591 | ✗ | ✓ | ✗ |
| groq:qwen-2.5-coder-32b | complex_code | ✓ | 3.60 | 5612 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | system_design | ✓ | 3.78 | 7936 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b | problem_solving | ✓ | 2.47 | 3363 | ✓ | ✓ | ✓ |
| groq:qwen-2.5-coder-32b (Summary) | ALL | 100.0% | 2.06 | 3082 | - | - | - |
|---|---|---|---|---|---|---|---|

## Speed Rankings (Lower is Better)


## Speed Rankings (Lower is Better)
| Rank | Model | Avg Time (s) | Min Time (s) | Max Time (s) | Total Time (s) | Relative Speed |
|---|---|---|---|---|---|---|
| 1 | groq:deepseek-r1-distill-llama-70b-specdec | 1.26 | 0.57 | 2.03 | 8.85 | 5.8x faster |
| 2 | groq:qwen-2.5-coder-32b | 2.06 | 0.72 | 3.78 | 14.45 | 3.6x faster |
| 3 | anthropic:claude-3-5-sonnet-latest | 7.36 | 1.75 | 14.11 | 51.50 | 1.0x faster |