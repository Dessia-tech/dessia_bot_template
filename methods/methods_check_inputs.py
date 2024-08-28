
import re
import requests

def validate_package_name(name):
    """
    Check if the package name follows Python naming conventions.
    """
    if not name:
        raise ValueError("\nYou need to add a 'Package name'")

    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
        raise ValueError(f"Invalid package name '{name}'. Package names must start with a letter or underscore and contain only lowercase letters, numbers, and underscores. Single and double quotes and double are not authorized.")

def check_pypi_package_name(name):
    """
    Check if the package name already exists on PyPI.
    """
    response = requests.get(f"https://pypi.org/pypi/{name}/json")
    if response.status_code == 200:
        print(f"Warning: The package name '{name}' already exists on PyPI. Consider choosing a different name.")

def validate_email(email):
    """
    Validate the email format.
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError(f"Invalid email address '{email}'.")

def validate_url(url):
    """
    Validate the URL format.
    """
    if not url:
        raise ValueError("\nYou need to add a 'Package URL'")

    if not re.match(r'^gitlab\.com:', url):
        raise ValueError(f"\nAre you sure about your 'Package URL' = {url} ? " +\
                         "The package must be sorted in Dessia Organization (as: git@gitlab.com:dessia/XX)")

def validate_python_version(version):
    """
    Validate the Python version format.
    """
    if not re.match(r'^>=?(\d+\.\d+)$', version):
        raise ValueError(f"Invalid Python version '{version}'. Example of a valid version: '>=3.8'.")

def validate_required_packages(packages):
    """
    Validate the format of required packages and versions.
    """
    if packages:
        for package in packages.split(','):
            if not re.match(r'^[a-zA-Z0-9_-]+(==|>=|<=|~=)?[0-9.]*$', package.strip()):
                raise ValueError(f"Invalid package requirement '{package}'. Ensure correct formatting.")