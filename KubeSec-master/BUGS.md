# Fuzzing results and findings

## Bug-001: Empty list document produces an IndexError

- Method: parser.getSingleDict4MultiDocs
- Reproducing input: [[]]
- Actual behavior: IndexError at dic = dic[0]
- Expected behavior: Handle an empty list doc or reject it with a validation error
- Status: Not fixed

Manual evidence: evidence/empty-list-crash.txt

## Fuzzing summary

Seed: 5710
Methods tested: 2/10
Cases run: 204
Cases failed: 26

- getSingleDict4MultiDocs: 104 cases
- getValuesRecursively: 100 cases

Report: evidence/fuzz-results.json