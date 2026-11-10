# Fuzzing results and findings

## Bug-001: Empty list document produces an IndexError

- Method: parser.getSingleDict4MultiDocs
- Reproducing input: [[]]
- Actual behavior: IndexError at dic = dic[0]
- Expected behavior: Handle an empty list doc or reject it with a validation error
- Status: Not fixed

Manual evidence: evidence/empty-list-crash.txt

## Bug-002: Incorrect nesting depths across neighboring branches

- Method: parser.getKeyRecursively
- Reproducing input: {"a": {"leaf": 1}, "b": {"leaf": 2}}
- Actual behavior: [("a", 0), ("leaf", 1), ("b", 1), ("leaf", 2)]
- Expected behavior: [("a", 0), ("leaf", 1), ("b", 0), ("leaf", 1)]
- Status: Not fixed

Automated evidence: evidence/fuzz-results.json

## Fuzzing summary

Seed: 5710
Methods tested: 3/10
Cases run: 304
Cases failed: 126

- getSingleDict4MultiDocs: 104 cases
- getValuesRecursively: 100 cases
- getKeyRecursively: 100 cases

Report: evidence/fuzz-results.json