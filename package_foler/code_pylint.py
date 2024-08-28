"""
Pylint Analysis.
"""

from pylint.lint import Run

MIN_NOTE = 8

UNWATCHED_ERRORS = []

MAX_ERROR_BY_TYPE = {
    "line-too-long": 0,
    "consider-using-f-string": 0,
    "no-else-return": 0,
    "implicit-str-concat": 0,
    "consider-using-in": 0,
    "used-before-assignment": 0,
    "missing-docstring": 0,
    "too-many-arguments": 0,
    "too-many-locals": 0,
    "too-many-return-statements": 0,
    "invalid-name": 0,
    "redefined-outer-name": 0,
    "unused-variable": 0,
    "import-error": 0,
    "duplicate-code": 0,
    "bad-continuation": 0,
    "no-member": 0,
    "logging-format-interpolation": 0,
    "too-many-nested-blocks": 0,
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
    "fixme": 0,
    "global-statement": 0,
    "import-outside-toplevel": 0,
    "invalid-unary-operand-type": 0,
    "length-of-docstring": 0,
    "no-attribute": 0,
    "no-else-continue": 0,
    "no-self-use": 0,
    "not-callable": 0,
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
    "fixme": 0,
    "global-statement": 0,
    "import-outside-toplevel": 0,
    "invalid-unary-operand-type": 0,
    "length-of-docstring": 0,
    "no-attribute": 0,
    "no-else-continue": 0,
    "no-self-use": 0,
    "not-callable": 0,
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
    "invalid-name": 0,
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

import os
import sys

f = open(os.devnull, "w")

old_stdout = sys.stdout
sys.stdout = f

results = Run(["{{PACKAGE_NAME}}", "--output-format=json", "--reports=no"], do_exit=False)
# `exit` is deprecated, use `do_exit` instead
sys.stdout = old_stdout

PYLINT_OBJECTS = True
if hasattr(results.linter.stats, "global_note"):
    pylint_note = results.linter.stats.global_note
    PYLINT_OBJECT_STATS = True
else:
    pylint_note = results.linter.stats["global_note"]
    PYLINT_OBJECT_STATS = False

print("Pylint note: ", pylint_note)
assert pylint_note >= MIN_NOTE
print("You can increase MIN_NOTE in pylint to {} (actual: {})".format(pylint_note, MIN_NOTE))


def extract_messages_by_type(type_):
    return [m for m in results.linter.reporter.messages if m.symbol == type_]


# uncontrolled_errors = {}
error_detected = False

if PYLINT_OBJECT_STATS:
    stats_by_msg = results.linter.stats.by_msg
else:
    stats_by_msg = results.linter.stats["by_msg"]

for error_type, number_errors in stats_by_msg.items():
    if error_type not in UNWATCHED_ERRORS:
        if error_type in MAX_ERROR_BY_TYPE:
            max_errors = MAX_ERROR_BY_TYPE[error_type]
        else:
            max_errors = 0

        if number_errors > max_errors:
            error_detected = True
            print("Fix some {} errors: {}/{}".format(error_type, number_errors, max_errors))
            for message in extract_messages_by_type(error_type):
                print("{} line {}: {}".format(message.path, message.line, message.msg))
        elif number_errors < max_errors:
            print("You can lower number of {} to {} (actual {})".format(error_type, number_errors, max_errors))


if error_detected:
    raise RuntimeError("Too many errors. Run pylint {{PACKAGE_NAME}} to get the errors")
