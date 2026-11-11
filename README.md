# Software Quality Assurance Final Project - Fall 2026

[![SQA checks](https://github.com/nicolasarmientor/TEAM7-FALL2026-SQA/actions/workflows/sqa.yml/badge.svg)](https://github.com/nicolasarmientor/TEAM7-FALL2026-SQA/actions/workflows/sqa.yml)

**Course:** COMP 5710
**Team Name:** Team 7
**GitHub Repository Name:** `TEAM7-FALL2026-SQA`

## Team Member

| Name | Email |
| --- | --- |
| Nicolas Sarmiento | nzs0102@auburn.edu |

---
## Current SQA results

- Fuzzing: 10 methods, 1004 cases.
- Findings: 226 failing cases failing under three documented bugs.
- Forensic logging: 10 methods applied.
- CI: Parsing tests, fuzzing, baseline validation, and evidence

See [bug findings](KubeSec-master/BUGS.md)

## Run the SQA check locally

Create and activate a Conda environment:

```bash
conda create --name team7-sqa python=3.11
conda activate team7-sqa
```

From the repository root, enter the source directory and install the necessary dependencies:

```bash
cd KubeSec-master
python -m pip install "ruamel.yaml==0.17.21"
```

Run the existing parsing tests, fuzzing, and validation:

```bash
python TEST_PARSING.py
python fuzz.py
python check_fuzz_results.py
```

Expected results after bash execution:

- 23 passing parsing tests
- 1,004 test cases executed across all 10 methods
- 226 failing cases corresponding to 3 distinct bug cases
- Baseline validation logs 0 unexpected failures.

## Report and evidence

- [Project report](SQA-REPO.md)
- [Bug findings](KubeSec-master/BUGS.md)
- [Execution screenshots](KubeSec-master/evidence/screenshots)
- [GitHub Actions](https://github.com/nicolasarmientor/TEAM7-FALL2026-SQA/actions)