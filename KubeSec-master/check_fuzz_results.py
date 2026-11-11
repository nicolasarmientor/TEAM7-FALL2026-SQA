import json
from collections import Counter
from pathlib import Path

FAILURE_FIELDS = (
    "method", "case_id", "input", "target", 
    "search", "exception", "message"
)


def signature(failure):
    details = {
        key: failure[key] 
        for key in FAILURE_FIELDS if key in failure
    }

    return json.dumps(details, sort_keys=True)


def main():
    baseline = json.loads(
        Path("fuzz-baseline.json").read_text(encoding="utf-8")
    )
    report = json.loads(
        Path("evidence/fuzz-results.json").read_text(encoding="utf-8")
    )

    expected_counts = baseline["method_cases"]
    actual_counts = report["method_cases"]

    if len(expected_counts) != 10:
        raise SystemExit("FAILURE: Baseline must cover 10 methods.")

    if actual_counts != expected_counts:
        raise SystemExit("FAILURE: Method case counts changed.")

    if report["methods_tested"] != 10:
        raise SystemExit("FAILURE: Expected 10 tested methods.")

    if report["seed"] != baseline["seed"]:
        raise SystemExit("FAILURE: Random seed changed.")

    if report["total_cases"] != sum(actual_counts.values()):
        raise SystemExit("FAILURE: Total case count inconsistent.")

    failures = report["failures"]

    if report["failure_count"] != len(failures):
        raise SystemExit("FAILURES: Failure count inconsistent.")

    known = Counter(
        signature(failure)
        for failure in baseline["known_failures"]
    )

    current = Counter(signature(failure) for failure in failures)
    unexpected = current - known

    if unexpected:
        print("Unexpected failures:")
        for details, count in unexpected.items():
            print(f"{count} occurrence(s): {details}")
        raise SystemExit(1)

    print("PASS: All 10 methods have the expected case counts.")
    print(f"Known failing cases still present: {len(failures)}")
    print(f"Known failing cases no longer present: {sum((known - current).values())}")
    print("Unexpected failures: 0")


if __name__ == "__main__":
    main()