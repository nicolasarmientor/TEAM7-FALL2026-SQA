# Import libraries
import json
import traceback
import random
from pathlib import Path
import parser

# Main code
def main():
    seed = 5710
    rng = random.Random(seed)
    output = Path("evidence")
    output.mkdir(exist_ok=True)

    cases = [[], [[]], [None], [{}]]
    for _ in range(100):
        document = rng.choice([
            [],
            {},
            None,
            {"name": rng.choice(["example", "", None, 42])}
        ])
        cases.append([document])

    failures = []

    for case_id, documents in enumerate(cases):
        try:
            parser.getSingleDict4MultiDocs(documents)
        except Exception as error:
            failures.append({
                "method": "getSingleDict4MultiDocs",
                "seed": seed,
                "case_id": case_id,
                "input": documents,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

    value_case_count = 100

    for case_id in range(value_case_count):
        leaves = [
            rng.choice([None, True, False, 0, 42, "", "example"])
            for _ in range(rng.randint(0, 20))
        ]

        nested = []
        for value in leaves:
            shape = rng.randrange(3)
            if shape == 0:
                nested.append(value)
            elif shape == 1:
                nested.append({"value": value})
            else:
                nested.append([{"inner": [value]}])

        try:
            actual = list(parser.getValuesRecursively(nested))
            if actual != leaves:
                raise AssertionError(f"Expected {leaves!r}, got {actual!r}")
        except Exception as error:
            failures.append({
                "method": "getValuesRecursively",
                "seed": seed,
                "case_id": case_id,
                "input": nested,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

    key_case_count = 100

    for case_id in range(key_case_count):
        data = {}
        expected = []

        for index in range(rng.randint(2, 8)):
            key = f"branch_{index}"
            data[key] = {"leaf": rng.randint(-100, 100)}
            expected.extend([(key, 0), ("leaf", 1)])

        actual = []

        try:
            parser.getKeyRecursively(data, actual)
            if actual != expected:
                raise AssertionError(f"Expected {expected!r}, got {actual!r}")
        except Exception as error:
            failures.append({
                "method": "getKeyRecursively",
                "seed": seed,
                "case_id": case_id,
                "input": data,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

    target_case_count = 100

    for case_id in range(target_case_count):
        target = rng.choice(["target", "name", "value"])
        value = rng.choice([None, True, 0, 42, "", "example"])
        inner = {target: value}
        data = {target: inner}
        expected = [inner, value]
        actual = []

        try:
            parser.getValsFromKey(data, target, actual)
            if actual != expected:
                raise AssertionError(f"Expected {expected!r}, got {actual!r}")
        except Exception as error:
            failures.append({
                "method": "getValsFromKey",
                "seed": seed,
                "case_id": case_id,
                "input": data,
                "target": target,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

    total_cases = (
        len(cases) + 
        value_case_count + 
        key_case_count +
        target_case_count       
    )
    
    report = {
        "seed": seed,
        "total_cases": total_cases,
        "failure_count": len(failures),
        "failures": failures,
    }

    report_path = output / "fuzz-results.json"
    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("Methods tested: 4/10")
    print(f"Cases executed: {total_cases}")
    print(f"Failing cases: {len(failures)}")
    print(f"Report: {report_path}")


# Execution code
if __name__ == "__main__":
    main()