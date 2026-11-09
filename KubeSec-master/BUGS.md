# Fuzzing results and findings

## Bug-001: Empty list document produces an IndexError

- Method: parser.getSingleDict4MultiDocs
- Reproducing input: [[]]
- Actual behavior: IndexError at dic = dic[0]
- Expected behavior: Handle an empty list doc or reject it with a validation error
- Status: Not fixed

Seed: 5710
Cases run: 104
Cases crashed: 26

Report: evidence/fuzz-results.json
Manual terminal output: evidence/empty-list-crash.txt

Fuzzing coverage: 1/10