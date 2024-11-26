"""Functions to get parameters from an ini file."""

import configparser

from .methods_check_inputs import (
    check_pypi_package_name,
    transform_url,
    validate_email,
    validate_package_name,
    validate_python_version,
    validate_required_packages,
    validate_url,
)


def read_config_to_dict(file_path: str) -> dict:
    """Read a configuration file and returns its contents as a dictionary, excluding the 'DOCUMENTATION' section."""
    config = configparser.ConfigParser()
    config.read(file_path)

    config_dict = {}

    for section in config.sections():
        if section != "DOCUMENTATION":
            for key, value in config[section].items():
                config_dict[key] = value.strip()

    return config_dict


def get_parameters_from_ini_file(ini_file: str) -> dict:
    """Get the parameters from an ini file."""
    parameters = read_config_to_dict(ini_file)

    # %% Package name

    package_name = parameters["package_name"]
    validate_package_name(package_name)
    check_pypi_package_name(package_name)

    project_package_name = "".join(x.title() for x in package_name.split("_"))
    parameters["project_package_name"] = project_package_name

    # %% Package URL

    package_url = parameters["package_url"]
    if package_url:
        validate_url(package_url)
        parameters["package_url"] = transform_url(package_url)

    # %% Short description

    if not parameters["short_description"]:
        parameters["short_description"] = "A Specific python package for a technological issue."

    # %% Long description

    if not parameters["long_description"]:
        parameters["long_description"] = (
            "A Python package using DessiA SDK tools and coding guidelines (https://documentation.dessia.io)"
        )

    # %% Python version

    version = parameters["python_version"]
    if not version:
        parameters["python_version"] = ">=3.9"
    else:
        validate_python_version(version)

    # %% Author

    if not parameters["author"]:
        parameters["author"] = "Operations-Team"

    # %% E-mail

    contact = parameters["email"]
    if not contact:
        parameters["email"] = "support@dessia.io"
    else:
        validate_email(contact)

    # %% Required packages

    required_packages = parameters["required_packages"]
    if not required_packages:
        required_packages = ["dessia_common>=0.18.0, plot_data>=0.26.0"]
    else:
        validate_required_packages(required_packages)

    return parameters
