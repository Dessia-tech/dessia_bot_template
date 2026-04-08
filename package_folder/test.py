"""Test script for running unittests and scripts with coverage."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Optional

import tomli

PROJECT_ROOT = Path(__file__).parent.resolve()
COVERAGE_FILE = str(PROJECT_ROOT / ".coverage")
COVERAGE_RCFILE = str(PROJECT_ROOT / "pyproject.toml")
COVERAGE_SOURCE = str(PROJECT_ROOT / "src" / "{{PACKAGE_NAME}}")


def setup_environment() -> None:
    """Set up environment variables for coverage."""
    os.environ["COVERAGE_FILE"] = COVERAGE_FILE
    os.environ["COVERAGE_RCFILE"] = COVERAGE_RCFILE


def load_config() -> dict[str, Any]:
    """Load configuration file."""
    with open((PROJECT_ROOT / "pyproject.toml").as_posix(), "rb") as file:
        config = tomli.load(file)

    # Extract the [coverage] section
    coverage_config = config.get("coverage", {})
    return coverage_config


def run_unittests_coverage() -> int:
    """Run coverage on unittests."""
    result = subprocess.run(
        [
            "coverage",
            "run",
            f"--data-file={COVERAGE_FILE}",
            f"--source={COVERAGE_SOURCE}",
            "-m",
            "unittest",
            "discover",
            "-v",
        ],
        check=False,
    )
    return result.returncode


def run_scripts_coverage(untracked_scripts: Optional[list[str]] = None) -> int:
    """Run all scripts with coverage."""
    returncode = 0
    scripts_dir = Path("scripts")
    print(f"  Untracked scripts: {untracked_scripts}")

    for script in scripts_dir.rglob("*.py"):
        script_path = script.relative_to(scripts_dir)

        if script_path.as_posix() not in untracked_scripts:
            print(f"\n  * Running {script_path}")
            start = time.perf_counter()
            result = subprocess.run(
                ["coverage", "run", f"--data-file={COVERAGE_FILE}", f"--source={COVERAGE_SOURCE}", "-a", script.name],
                cwd=script.parent,
                check=False,
                text=True,
            )
            if result.returncode != 0:
                print(f"ERROR: Script {script_path} failed")
                returncode = 1
            else:
                print(f"  OK: {script_path} ran in {time.perf_counter() - start:.2f}s")

    return returncode


def check_coverage_thresholds(config: dict[str, Any]) -> int:
    """Check coverage thresholds using the JSON report."""
    returncode = 0

    # Generate JSON coverage report
    subprocess.run(["coverage", "json", f"--data-file={COVERAGE_FILE}"], check=True)

    # Load JSON coverage report
    with open("coverage.json", encoding="utf-8") as file:
        coverage_report = json.load(file)

    # Check global coverage threshold
    global_coverage = coverage_report["totals"]["percent_covered"]
    threshold = config.get("min_global_coverage", 0)
    if global_coverage < threshold:
        print(
            f"ERROR: Global coverage is below the threshold of {threshold}%. Current coverage: {global_coverage:.2f}%"
        )
        returncode = 1

    # Check per-module coverage thresholds
    threshold = config.get("min_module_coverage", 0)
    for module_name, data in coverage_report["files"].items():
        module_coverage = data["summary"]["percent_covered"]

        if module_coverage < threshold:
            print(
                f"""
ERROR: Module {module_name} coverage is below the threshold of {threshold}%. Current coverage: {module_coverage:.2f}%
"""
            )
            returncode = 1

    return returncode


def main() -> None:
    """Run all tests and check coverage."""
    setup_environment()
    config = load_config()

    print("\n> RUNNING UNITTESTS")
    unittests_returncode = run_unittests_coverage()

    print("\n> RUNNING SCRIPTS")
    scripts_returncode = run_scripts_coverage(untracked_scripts=config.get("untracked_scripts", []))

    print("\n> CHECKING COVERAGE")
    time.sleep(1)
    subprocess.run(["coverage", "report", f"--data-file={COVERAGE_FILE}", "-m"], check=False)
    subprocess.run(["coverage", "html", f"--data-file={COVERAGE_FILE}", "-d", "htmlcov", "-q"], check=False)
    subprocess.run(["coverage", "xml", f"--data-file={COVERAGE_FILE}", "-o", "coverage.xml", "-q"], check=False)

    coverage_returncode = check_coverage_thresholds(config)

    print()
    if unittests_returncode + scripts_returncode + coverage_returncode == 0:
        print("SUCCESS: All tests passed.")
    if unittests_returncode != 0:
        print("ERROR: Some unittests failed.")
    if scripts_returncode != 0:
        print("ERROR: Some scripts failed.")
    if coverage_returncode != 0:
        print("ERROR: Coverage is below the threshold.")

    sys.exit(unittests_returncode + scripts_returncode + coverage_returncode)


if __name__ == "__main__":
    main()
