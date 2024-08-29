"""
PyDocStrings Analysis.
"""

import os
import random
from glob import glob

import pydocstyle

exclude_folders = {""}


def should_exclude_folder(path):
    # Vérifie si le chemin contient un des dossiers à exclure
    return any(ex in path for ex in exclude_folders)


file_list = filter(
    lambda z: not z.endswith("__init__.py") and not should_exclude_folder(z),
    [y for x in os.walk("./{{PACKAGE_NAME}}") for y in glob(os.path.join(x[0], "*.py"))],
)


UNWATCHED_ERRORS = [
    # Do not watch these errors
    # General Format and Content Issues
    "D100",
    "D104",
    "D105",
    "D107",
    # Docstring Formatting
    "D200",
    "D202",
    "D203",
    "D204",
    "D206",
    "D210",
    "D212",
    # Docstring Content and Structure
    "D301",
    "D302",
    "D401",
    "D402",
    "D407",
    "D408",
    "D409",
    "D412",
    "D415",
    "D418",
]

MAX_ERROR_BY_TYPE = {
    # If the error code is not in this dict, then there is no tolerance on the error.
    # http://www.pydocstyle.org/en/stable/error_codes.html
}

error_detected = False
error_over_ratchet_limit = False
ratchet_limit = 9

code_to_errors = {}
for error in pydocstyle.check(file_list, ignore=UNWATCHED_ERRORS):
    code_to_errors.setdefault(error.code, [])
    code_to_errors[error.code].append(error)

code_to_number = {code: len(errors) for code, errors in code_to_errors.items()}

for error_code, number_errors in code_to_number.items():
    if error_code not in UNWATCHED_ERRORS:
        max_errors = max(MAX_ERROR_BY_TYPE.get(error_code, 0), 0)

        if number_errors > max_errors:
            error_detected = True
            print(f"\nFix some {error_code} errors: {number_errors}/{max_errors}")

            errors = code_to_errors[error_code]
            errors_to_show = sorted(random.sample(errors, min(30, len(errors))), key=lambda m: (m.filename, m.line))
            for error in errors_to_show:
                print(f"{error.filename} line {error.line}: {error.message}")
        elif max_errors - ratchet_limit <= number_errors < max_errors:
            print(f"\nYou can lower number of {error_code} to {number_errors} (actual {max_errors})")
        elif number_errors < max_errors - ratchet_limit:
            error_over_ratchet_limit = True
            print(f"\nYou MUST lower number of {error_code} to {number_errors} (actual {max_errors})")

if error_detected:
    raise RuntimeError("Too many errors\nRun pydocstyle {{PACKAGE_NAME}} to get the errors")

if error_over_ratchet_limit:
    raise RuntimeError(
        "Please lower the error limits in code_pydocstyle.py MAX_ERROR_BY_TYPE according to warnings above"
    )
