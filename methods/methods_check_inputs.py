"""This module contains functions to check the validity of the inputs provided by the user."""

import re
from http import HTTPStatus
from urllib.parse import urlparse

import requests


def validate_package_name(name: str) -> None:
    """Check if the package name follows Python naming conventions."""
    if not name:
        raise ValueError("\nYou need to add a 'Package name'")

    if not re.match(r"^[a-z_][a-z0-9_]*$", name):
        raise ValueError(
            f"Invalid package name '{name}'. Package names must start with a letter or underscore and contain only lowercase letters, numbers, and underscores. Single and double quotes and double are not authorized."
        )


def check_pypi_package_name(name: str) -> None:
    """Check if the package name already exists on PyPI."""
    response = requests.get(f"https://pypi.org/pypi/{name}/json")

    if response.status_code == HTTPStatus.OK:
        print(f"Warning: The package name '{name}' already exists on PyPI. Consider choosing a different name.")


def validate_email(email: str) -> None:
    """Validate the email format."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError(f"Invalid email address '{email}'.")


def validate_url(url: str) -> None:
    """Validate the URL format."""
    # if not url:
    #     raise ValueError("\nYou need to add a 'Package URL'")

    # if not re.match(r'^gitlab\.com:', url):
    #     raise ValueError(f"\nAre you sure about your 'Package URL' = {url} ? " +\
    #                      "The package must be sorted in Dessia Organization (as: gitlab.com/dessia/XX)")

    if not ("gitlab" in url.lower() or "github" in url.lower()):
        raise ValueError(
            f"\nAre you sure about your 'Package URL' = {url} ? It is not a Git URL\n"
            + "If you do not need to use Git, leave an empty cell."
        )


def transform_url(url: str) -> str:
    """Transform the given URL to be used for Gitlab pusing."""
    # Remove 'www.' if present
    url = url.replace("www.", "", 1)

    # # Replace the first '/' with ':'
    # return url.replace("/", ":", 1)

    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    new_url = f"{parsed.netloc}:{parsed.path.lstrip('/')}"
    new_url = new_url.rstrip("/")

    return new_url


def validate_python_version(version: str) -> None:
    """Validate the Python version format."""
    if not re.match(r"^>=?(\d+\.\d+)$", version):
        raise ValueError(f"Invalid Python version '{version}'. Example of a valid version: >=3.8.")


def validate_required_packages(packages: str) -> None:
    """Validate the format of required packages and versions."""
    if packages:
        for package in packages.split(","):
            if not re.match(r"^[a-zA-Z0-9_-]+(==|>=|<=|~=)?[0-9.]*$", package.strip()):
                raise ValueError(f"Invalid package requirement '{package}'. Ensure correct formatting.")
