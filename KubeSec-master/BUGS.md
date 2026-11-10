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

## Bug-003: Nested keys skipped

- Method: parser.getValsFromKey
- Reproducing input: {"target": {"target": "inner"}}
- Target key: "target"
- Actual behavior: [{"target": "inner"}]
- Expected behavior: [{"target": "inner"}, "inner"]
- Status: Not fixed

Automated evidence: evidence/fuzz-results.json

## Fuzzing summary

- Seed: 5710
- Methods tested: 8/10
- Cases run: 804
- Cases failed: 226

|Method|Cases|Failures|
|---|---|---|
|getSingleDict4MultiDocs|104|26|
|getValuesRecursively|100|0|
|getKeyRecursively|100|100|
|getValsFromKey|100|100|
|keyMiner|100|0|
|readYAMLAsStr|100|0|
|checkParseError|100|0|
|loadMultiYAML|100|0|

Report: evidence/fuzz-results.json