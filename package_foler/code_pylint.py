"""
Package code quality analysis script with pylint.
"""

import os
import sys

from pylint.lint import Run

MIN_SCORE = 10.0

UNWATCHED_ERRORS = []

MAX_ERRORS_BY_TYPE = {
    "line-too-long": 0,
    "consider-using-f-string": 0,
    "implicit-str-concat": 0,
    "consider-using-in": 0,
    "used-before-assignment": 0,
    "missing-docstring": 0,
    "too-many-arguments": 0,
    "too-many-locals": 0,
    "too-many-return-statements": 0,
    "unused-variable": 0,
    "import-error": 0,
    "abstract-method": 0,
    "access-member-before-definition": 0,
    "arguments-differ": 0,
    "bare-except": 0,
    "blacklisted-name": 0,
    "breaking-import": 0,
    "const-righteous": 0,
    "deprecated-module": 0,
    "duplicate-argument-name": 0,
    "duplicate-key": 0,
    "eval-used": 0,
    "global-statement": 0,
    "import-outside-toplevel": 0,
    "invalid-unary-operand-type": 0,
    "length-of-docstring": 0,
    "no-attribute": 0,
    "no-self-use": 0,
    "not-supported-yet": 0,
    "redundant-unittest-assert": 0,
    "reimported": 0,
    "too-many-branches": 0,
    "too-many-function-args": 0,
    "too-many-function-attributes": 0,
    "too-many-instance-attributes": 0,
    "too-many-public-methods": 0,
    "unexpected-keyword-arg": 0,
    "unidiomatic-typecheck": 0,
    "unnecessary-comprehension": 0,
    "unused-import": 0,
    "wrong-import-position": 0,
    "missing-module-docstring": 0,
    "missing-class-docstring": 0,
    "missing-function-docstring": 0,
    "no-qa": 0,
    "no-else-continue": 0,
    "not-context-manager": 0,
    "too-few-public-methods": 0,
    "unnecessary-pass": 0,
    "invalid-sequence-index": 0,
    "logging-format-interpolation": 0,
    "no-method-argument": 0,
    "too-many-nested-blocks": 0,
    "no-else-return": 0,
    "redefined-builtin": 0,
    "superfluous-parens": 0,
    "useless-object-inheritance": 0,
    "no-member": 0,
    "not-callable": 0,
    "trailing-whitespace": 0,
    "invalid-name": 0,
    "duplicate-code": 0,
    "bad-continuation": 0,
    "fixme": 0,
    "redefined-outer-name": 0,
}


# Redirect stdout to suppress pylint's output, keeping it in a variable
sys.stdout = open(os.devnull, "w", encoding="utf-8")
results = Run(["my_package", "--output-format=json", "--reports=no"], exit=False)
sys.stdout = sys.__stdout__  # Restore stdout

pylint_score = (
    results.linter.stats.global_note
    if hasattr(results.linter.stats, "global_note")
    else results.linter.stats["global_note"]
)
print(f"Pylint score: {pylint_score}")
assert pylint_score >= MIN_SCORE, f"Pylint score is below the minimum required: {MIN_SCORE}."

error_detected = False
stats_by_msg = (
    results.linter.stats.by_msg if hasattr(results.linter.stats, "by_msg") else results.linter.stats["by_msg"]
)

for error_type, number_errors in stats_by_msg.items():
    max_errors = MAX_ERRORS_BY_TYPE.get(error_type, 0)
    if number_errors > max_errors:
        error_detected = True
        print(f"Fix {number_errors} {error_type} errors (maximum allowed: {max_errors})")
        for message in (m for m in results.linter.reporter.messages if m.symbol == error_type):
            print(f"{message.path}, line {message.line}: {message.msg}")

    elif number_errors < max_errors:
        print(
            f"""
You can reduce the maximum allowed {error_type} errors to {number_errors} (current limit: {max_errors})"""
        )

if error_detected:
    raise RuntimeError(f"Too many errors. Run 'pylint {{PACKAGE_NAME}}' to see details.")
