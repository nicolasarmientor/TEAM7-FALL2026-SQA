# Import libraries
import json
import traceback
import random
from pathlib import Path
import parser
import tempfile

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

    miner_case_count = 100

    for case_id in range(miner_case_count):
        target = f"needle_{case_id}"
        branch = f"branch_{rng.randint(0, 9)}"
        position = rng.randint(0, 5)

        items = [None] * position
        items.append({"leaf": target})
        data = {branch: items}

        if rng.choice([True, False]):
            search = target
            expected = [branch, str(position), "leaf", target]
        else:
            search = f"missing_{case_id}"
            expected = None

        try:
            actual = parser.keyMiner(data, search)
            if actual != expected:
                raise AssertionError(f"Expected {expected!r}, got {actual!r}")
        except Exception as error:
            failures.append({
                "method": "keyMiner",
                "seed": seed,
                "case_id": case_id,
                "input": data,
                "search": search,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

    read_case_count = 100

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "generated.yaml"

        for case_id in range(read_case_count):
            content = "".join(
                rng.choice(["a", " ", "\n", "\t", "é", "中", ":", "#"])
                for _ in range(rng.randint(0, 200))
            )

            file_path.write_text(content, encoding="utf-8")

            try:
                actual = parser.readYAMLAsStr(str(file_path))
                if actual != content:
                    raise AssertionError(f"Expected {content!r}, got {actual!r}")
            except Exception as error:
                failures.append({
                    "method": "readYAMLAsStr",
                    "seed": seed,
                    "case_id": case_id,
                    "input": content,
                    "exception": type(error).__name__,
                    "message": str(error),
                    "traceback": traceback.format_exc()
                })

    parse_case_count = 100

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "parse-case.yaml"

        for case_id in range(parse_case_count):
            number = rng.randint(-1000, 1000)

            if case_id % 2 == 0:
                content = f"name: example_{number}\nitems: [{number}]\n"
                expected = True
            else:
                content = f"items: [{number}\n"
                expected = False

            file_path.write_text(content, encoding="utf-8")

            try:
                actual = parser.checkParseError(str(file_path))
                if actual is not expected:
                    raise AssertionError(f"Expected {expected!r}, got {actual!r}")
            except Exception as error:
                failures.append({
                    "method": "checkParseError",
                    "seed": seed,
                    "case_id": case_id,
                    "input": content,
                    "expected": expected,
                    "exception": type(error).__name__,
                    "message": str(error),
                    "traceback": traceback.format_exc()
                })

    multi_case_count = 100

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "multi-case.yaml"

        for case_id in range(multi_case_count):
            expected = []
            documents = []

            for index in range(rng.randint(1, 5)):
                number = rng.randint(-1000, 1000)
                name = f"example_{index}"

                expected.append({"name": name, "number": number})
                documents.append(f"name: {name}\nnumber: {number}\n")

            content = "---\n".join(documents)
            file_path.write_text(content, encoding="utf-8")

            try:
                actual = parser.loadMultiYAML(str(file_path))
                if actual != expected:
                    raise AssertionError(f"Expected {expected!r}, got {actual!r}")
            except Exception as error:
                failures.append({
                    "method": "loadMultiYAML",
                    "seed": seed,
                    "case_id": case_id,
                    "input": content,
                    "expected": expected,
                    "exception": type(error).__name__,
                    "message": str(error),
                    "traceback": traceback.format_exc()
                })

    path_case_count = 100

    for case_id in range(path_case_count):
        folder = f"project_{rng.randint(0, 1000)}"
        file_name = f"config_{rng.randint(0, 1000)}.yaml"

        if case_id % 2 == 0:
            marker = rng.choice([
                "github/workflows/",
                ".github/",
                ".travis.yml"
            ])
            path = f"{folder}/{marker}{file_name}"
            expected = True
        else:
            path = f"{folder}/manifests/{file_name}"
            expected = False

        try:
            actual = parser.checkIfWeirdYAML(path)
            if actual is not expected:
                raise AssertionError(f"Expected {expected!r}, got {actual!r}")
        except Exception as error:
            failures.append({
                "method": "checkIfWeirdYAML",
                "seed": seed,
                "case_id": case_id,
                "input": path,
                "expected": expected,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

    helm_case_count = 100

    for case_id in range(helm_case_count):
        folder = f"project_{rng.randint(0, 1000)}"
        marker = rng.choice([
            "helm", "chart", "services", "k8s-ingress", 
            "deploy", "configuration"
        ])

        combination = case_id % 4

        match combination:
            case 0:
                path = f"{folder}/{marker}/values.yaml"
                expected = True
            case 1:
                path = f"{folder}/{marker}/settings.yaml"
                expected = False
            case 2:
                path = f"{folder}/manifests/values.yaml"
                expected = False
            case _:
                path = f"{folder}/manifests/settings.yaml"
                expected = False

        try:
            actual = parser.checkIfValidHelm(path)
            if actual is not expected:
                raise AssertionError(f"Expected {expected!r}, got {actual!r}")
        except Exception as error:
            failures.append({
                "method": "checkIfValidHelm",
                "seed": seed,
                "case_id": case_id,
                "input": path,
                "expected": expected,
                "exception": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })


    total_cases = (
        len(cases) + 
        value_case_count + 
        key_case_count +
        target_case_count +
        miner_case_count +
        read_case_count +
        parse_case_count +
        multi_case_count +
        path_case_count +
        helm_case_count    
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

    print("Methods tested: 10/10")
    print(f"Cases executed: {total_cases}")
    print(f"Failing cases: {len(failures)}")
    print(f"Report: {report_path}")


# Execution code
if __name__ == "__main__":
    main()