"""
Test runner with selective execution: unit tests, scripts, coverage.

Usage:
    python test.py                                        # run everything (unittests + coverage + scripts)
    python test.py --unittests --coverage                 # unit tests with coverage
    python test.py --unittests --coverage --modified-scripts  # MR mode (tests + coverage + modified scripts)
    python test.py --unittests                            # unit tests only (no coverage)
    python test.py --scripts                              # all scripts
    python test.py --modified-scripts                     # modified/added scripts only
    python test.py --modified-scripts --diff-base staging # modified scripts vs explicit base branch

Short aliases: -t (--unittests), -s (--scripts), -m (--modified-scripts), -c (--coverage)

--modified-scripts base branch resolution:
    1. --diff-base argument (explicit)
    2. CI_MERGE_REQUEST_TARGET_BRANCH env var (set automatically by GitLab CI on MR pipelines)
    3. Auto-detect main/master from local git refs (local fallback)

Coverage thresholds and untracked scripts are read from [coverage] in pyproject.toml.

JUnit XML reports are written for GitLab CI test reporting: report.xml (unit tests)
and scripts-report.xml (one testcase per script).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

try:
    import tomllib
except ImportError:
    import tomli as tomllib

PROJECT_ROOT = Path(__file__).parent.resolve()
COVERAGE_FILE = str(PROJECT_ROOT / ".coverage")
UNITTEST_REPORT_FILE = str(PROJECT_ROOT / "report.xml")
SCRIPTS_REPORT_FILE = str(PROJECT_ROOT / "scripts-report.xml")
STDERR_TAIL_LINES = 50
INVALID_XML_CHARS = re.compile(r"[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]")


def load_config() -> dict[str, Any]:
    """Load [coverage] section from pyproject.toml."""
    with open(PROJECT_ROOT / "pyproject.toml", "rb") as file:
        config = tomllib.load(file)
    return config.get("coverage", {})


def run_unittests(with_coverage: bool) -> int:
    """Run unit tests, optionally with coverage."""
    print("\n> RUNNING UNIT TESTS")
    junit_option = f"--junitxml={UNITTEST_REPORT_FILE}"
    if with_coverage:
        cmd = ["coverage", "run", f"--data-file={COVERAGE_FILE}", "-m", "pytest", junit_option]
    else:
        cmd = [sys.executable, "-m", "pytest", junit_option]
    result = subprocess.run(cmd, check=False)
    return result.returncode


def is_script_excluded(script_path: Path, untracked_scripts: list[str]) -> bool:
    """Check if a script matches any untracked pattern (glob matching)."""
    return any(script_path.match(pattern) for pattern in untracked_scripts)


def _write_scripts_junit_report(results: list[tuple[Path, float, int, str]], suite_name: str) -> None:
    """Write a JUnit XML report (one testcase per script) for GitLab CI test reporting."""
    failures = sum(1 for _, _, returncode, _ in results if returncode != 0)
    total_time = sum(duration for _, duration, _, _ in results)
    testsuite = ElementTree.Element(
        "testsuite",
        name=suite_name,
        tests=str(len(results)),
        failures=str(failures),
        errors="0",
        time=f"{total_time:.3f}",
    )
    for script_path, duration, returncode, stderr in results:
        # Stable classname across suites so GitLab matches testcases between pipelines
        testcase = ElementTree.SubElement(
            testsuite,
            "testcase",
            classname="scripts",
            name=str(script_path),
            time=f"{duration:.3f}",
        )
        if returncode != 0:
            failure = ElementTree.SubElement(testcase, "failure", message=f"Script exited with code {returncode}")
            if stderr:
                tail = "\n".join(stderr.strip().splitlines()[-STDERR_TAIL_LINES:])
                failure.text = INVALID_XML_CHARS.sub("", tail)
    ElementTree.ElementTree(testsuite).write(SCRIPTS_REPORT_FILE, encoding="utf-8", xml_declaration=True)


def _run_script_suite(scripts: list[Path], suite_name: str, label: str = "") -> int:
    """
    Run scripts sequentially and write the JUnit report.

    :param scripts: script paths relative to repo root (e.g. scripts/foo/bar.py).
    :param suite_name: JUnit testsuite name.
    :param label: suffix appended to per-script log lines.
    """
    scripts_dir = Path("scripts")
    results = []
    returncode = 0
    for script in scripts:
        script_path = script.relative_to(scripts_dir)
        print(f"\n  * Running {script_path}{label}")
        start = time.perf_counter()
        # Capture stderr only (stdout streams live) so tracebacks land in the JUnit failure body
        result = subprocess.run(
            [sys.executable, script.name],
            cwd=script.parent,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            check=False,
        )
        duration = time.perf_counter() - start
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        results.append((script_path, duration, result.returncode, result.stderr))
        if result.returncode != 0:
            print(f"  ERROR: Script {script_path} failed")
            returncode = 1
        else:
            print(f"  OK: {script_path} ran in {duration:.2f}s")
    _write_scripts_junit_report(results, suite_name)
    return returncode


def run_scripts(untracked_scripts: list[str] | None = None) -> int:
    """Run all scripts in scripts/ directory (without coverage)."""
    print("\n> RUNNING SCRIPTS")
    if untracked_scripts is None:
        untracked_scripts = []
    scripts_dir = Path("scripts")
    if not scripts_dir.exists():
        print("  No scripts/ directory found, skipping.")
        return 0

    scripts = [
        script
        for script in sorted(scripts_dir.rglob("*.py"))
        if not is_script_excluded(script.relative_to(scripts_dir), untracked_scripts)
    ]
    return _run_script_suite(scripts, suite_name="scripts")


def _detect_default_branch() -> str | None:
    """Detect the default branch (main or master) from local refs."""
    for branch in ("main", "master"):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"origin/{branch}"],
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return branch
    return None


def get_modified_scripts(diff_base: str | None = None) -> list[Path]:
    """
    Get scripts added or modified compared to a base branch.

    :param diff_base: base branch name. Falls back to CI_MERGE_REQUEST_TARGET_BRANCH,
        then auto-detects main/master.
    :return: list of script paths relative to repo root (e.g. scripts/foo/bar.py).
    """
    base = diff_base or os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH") or _detect_default_branch()
    if not base:
        print("  WARNING: could not determine base branch, skipping modified scripts.")
        return []

    fetch = subprocess.run(
        ["git", "fetch", "origin", base, "--depth=1"],
        check=False,
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        print(f"  WARNING: git fetch origin {base} failed: {fetch.stderr.strip()}")
        return []

    # Two-endpoint diff (no merge-base needed, works with shallow clones)
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AM", f"origin/{base}", "HEAD", "--", "scripts/"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"  WARNING: git diff failed: {result.stderr.strip()}")
        return []

    modified = [Path(line) for line in result.stdout.strip().splitlines() if line.endswith(".py")]

    # The diff is computed against a branch, the run happens in the working tree, and the two can
    # disagree - a partial checkout, or a job that rewrites the workspace. Running a path that is
    # not there fails with a confusing "No such file or directory" instead of naming the mismatch.
    present = [script for script in modified if script.is_file()]
    for script in modified:
        if script not in present:
            print(f"  WARNING: {script} is in the diff but not in the working tree, skipping.")
    return present


def run_modified_scripts(
    untracked_scripts: list[str] | None = None,
    diff_base: str | None = None,
) -> int:
    """Run only scripts that were added or modified in the current branch."""
    print("\n> RUNNING MODIFIED SCRIPTS")
    if untracked_scripts is None:
        untracked_scripts = []

    modified = get_modified_scripts(diff_base)
    if not modified:
        print("  No modified scripts found.")
        return 0

    scripts_dir = Path("scripts")
    scripts = [
        script for script in modified if not is_script_excluded(script.relative_to(scripts_dir), untracked_scripts)
    ]
    return _run_script_suite(scripts, suite_name="modified_scripts", label=" (modified)")


def check_coverage(config: dict[str, Any]) -> int:
    """Generate coverage reports and check thresholds."""
    print("\n> CHECKING COVERAGE")
    subprocess.run(["coverage", "report", f"--data-file={COVERAGE_FILE}", "-m"], check=False)
    subprocess.run(["coverage", "html", f"--data-file={COVERAGE_FILE}", "-d", "htmlcov", "-q"], check=False)
    subprocess.run(["coverage", "xml", f"--data-file={COVERAGE_FILE}", "-o", "coverage.xml", "-q"], check=False)
    result = subprocess.run(["coverage", "json", f"--data-file={COVERAGE_FILE}"], check=False)
    if result.returncode != 0:
        print("ERROR: No coverage data collected (tests may have failed).")
        return 1

    with open("coverage.json", encoding="utf-8") as file:
        report = json.load(file)

    returncode = 0
    global_coverage = report["totals"]["percent_covered"]

    threshold = config.get("min_global_coverage", 0)
    if global_coverage < threshold:
        print(f"ERROR: Global coverage {global_coverage:.2f}% < {threshold}%")
        returncode = 1

    threshold = config.get("min_module_coverage", 0)
    for module_name, data in report["files"].items():
        module_coverage = data["summary"]["percent_covered"]
        if module_coverage < threshold:
            print(f"ERROR: Module {module_name} coverage {module_coverage:.2f}% < {threshold}%")
            returncode = 1

    return returncode


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run unit tests and scripts.")
    parser.add_argument("-t", "--unittests", action="store_true", help="Run unit tests")
    parser.add_argument("-s", "--scripts", action="store_true", help="Run all scripts")
    parser.add_argument("-m", "--modified-scripts", action="store_true", help="Run only modified/added scripts")
    parser.add_argument(
        "--diff-base",
        type=str,
        default=None,
        help="Base branch for -m/--modified-scripts (default: CI_MERGE_REQUEST_TARGET_BRANCH)",
    )
    parser.add_argument("-c", "--coverage", action="store_true", help="Enable coverage on unit tests")
    return parser.parse_args()


def main() -> None:
    """Run selected tasks (default: all)."""
    args = parse_args()

    # No selection flags = run everything
    run_all = not (args.unittests or args.scripts or args.modified_scripts)
    do_unittests = run_all or args.unittests
    do_scripts = run_all or args.scripts
    do_modified_scripts = args.modified_scripts
    do_coverage = run_all or args.coverage

    os.environ["COVERAGE_FILE"] = COVERAGE_FILE
    config = load_config()
    untracked = config.get("untracked_scripts", [])

    returncodes = {}

    if do_unittests:
        returncodes["unittests"] = run_unittests(with_coverage=do_coverage)

    if do_scripts:
        returncodes["scripts"] = run_scripts(untracked)

    if do_modified_scripts:
        returncodes["modified_scripts"] = run_modified_scripts(untracked, args.diff_base)

    if do_coverage and do_unittests:
        returncodes["coverage"] = check_coverage(config)

    # Summary
    print()
    failed = {k: v for k, v in returncodes.items() if v != 0}
    if not failed:
        print("SUCCESS: All tasks passed.")
    else:
        for task in failed:
            print(f"ERROR: {task} failed.")

    sys.exit(sum(returncodes.values()))


if __name__ == "__main__":
    main()
