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

    report = {
        "seed": seed,
        "total_cases": len(cases),
        "failure_count": len(failures),
        "failures": failures,
    }

    report_path = output / "fuzz-results.json"
    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print(f"Cases executed: {len(cases)}")
    print(f"Crashing cases: {len(failures)}")
    print(f"Report: {report_path}")


# Execution code
if __name__ == "__main__":
    main()