"""
Coverage Analysis.
"""

import json

MIN_FILE_COVERAGE = 60
MIN_PROJECT_COVERAGE = 74

untracked_modules = []

print("untracked modules:", untracked_modules)

with open("coverage.json", "r", encoding="utf-8") as file:
    d = json.load(file)

project_coverage = d["totals"]["percent_covered"]

print(f"total covered: {project_coverage} %")
assert project_coverage > MIN_PROJECT_COVERAGE
print(
    f"[Coverage] You can increase MIN_PROJECT_COVERAGE to maximum {project_coverage}%"
    f" (actual {MIN_PROJECT_COVERAGE}%)"
)

MIN_ACTUAL_COVERAGE = 100
for file_name, data in d["files"].items():
    print(file_name, data["summary"]["percent_covered"], "%")
    if "/".join(file_name.split("/")[-2:]) in untracked_modules:
        print(file_name, "-> in untrack list")
    else:
        file_coverage = data["summary"]["percent_covered"]
        if file_coverage < MIN_FILE_COVERAGE:
            raise RuntimeError(f"File {file_name} is not covered enough: {file_coverage} % / {MIN_FILE_COVERAGE} %")
        MIN_ACTUAL_COVERAGE = min(MIN_ACTUAL_COVERAGE, data["summary"]["percent_covered"])

print(f"[Coverage] You can increase MIN_FILE_COVERAGE to maximum {MIN_ACTUAL_COVERAGE}% (actual:{MIN_FILE_COVERAGE})%")
