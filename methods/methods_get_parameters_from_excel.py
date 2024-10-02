import pandas as pd

from .methods_check_inputs import *


def get_parameters_from_excel(excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    df = df.fillna("")

    parameters = {}

    # %% Package name

    package_name = df["Package name *"][0]
    validate_package_name(package_name)
    check_pypi_package_name(package_name)
    project_package_name = "".join(x.title() for x in package_name.split("_"))

    parameters["package_name"] = package_name
    parameters["project_package_name"] = project_package_name

    # %% Package URL

    remote_url = df["Package URL"][0]
    if remote_url:
        validate_url(remote_url)
    parameters["remote_url"] = remote_url

    # %% Short description

    description = df["Short description"][0]
    if not description:
        description = "A Specific package for a technological issue."
    parameters["description"] = description

    # %% Long description

    long_description = df["Long description"][0]
    if not long_description:
        long_description = (
            "A Python package using DessiA SDK and DessiA coding guidelines (https://documentation.dessia.io)"
        )
    parameters["long_description"] = long_description

    # %% Python version

    version = df["Python version"][0]
    if not version:
        version = ">=3.9"
    else:
        validate_python_version(version)
    parameters["version"] = version

    # %% Author

    author = df["Author"][0]
    if not author:
        author = "Operations-Team"
    parameters["author"] = author

    # %% E-mail

    contact = df["E-mail"][0]
    if not contact:
        contact = "support@dessia.io"
    else:
        validate_email(contact)
    parameters["contact"] = contact

    # %% Required packages

    required_packages = df["Required packages"][0].replace("\n", "")
    if not required_packages:
        required_packages = ["dessia_common>=0.18.0, plot_data>=0.26.0"]
    else:
        validate_required_packages(required_packages)
    parameters["required_packages"] = required_packages

    return parameters
