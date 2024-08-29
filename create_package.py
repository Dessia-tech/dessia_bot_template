"""
This script creates a new Python package from a template directory, using the user inputs.
"""
import os
import shutil
import subprocess
from datetime import date

from methods.methods_get_parameters_from_excel import get_parameters_from_excel

# %% Inputs

parameters = get_parameters_from_excel(excel_file="Template_Inputs.xlsx")

# %% New Directory

# Path to the template directory
TEMPLATE_DIR = "package_foler"
NEW_PACKAGE_DIR = os.path.join('..', parameters["project_package_name"])

# Copy the template directory to a new location
shutil.copytree(TEMPLATE_DIR, NEW_PACKAGE_DIR)

# Rename the package folder
old_folder = os.path.join('..', parameters["project_package_name"], 'folder')
new_folder = os.path.join('..', parameters["project_package_name"], parameters["package_name"])
os.rename(old_folder, new_folder)

# %% Updates the files


# Function to replace placeholders in a file
def replace_placeholders(_file_path, _placeholders):
    """Replace placeholders in a file with the corresponding values."""
    with open(_file_path, "r", encoding="utf-8") as file:
        content = file.read()
    for placeholder, value in _placeholders.items():
        content = content.replace(placeholder, value)
    with open(_file_path, "w", encoding="utf-8") as file:
        file.write(content)


# Dictionary of placeholders to replace
placeholders = {
    "{{PACKAGE_NAME}}": parameters["package_name"],
    "{{PROJECT_NAME}}": parameters["project_package_name"],
    "{{LONG_DESCRIPTION}}": parameters["long_description"],
    "{{SHORT_DESCRIPTION}}": parameters["description"],
    "{{AUTHOR}}": parameters["author"],
    "{{CONTACT}}": parameters["contact"],
    "{{VERSION}}": parameters["version"],
    "{{DATE}}": date.today().strftime("%d/%m/%Y") + " (Initialization)",
    "{{REQUIRED_PACKAGES}}": parameters["required_packages"],
}


# Recursively find and update all files in the new package directory
for root, dirs, files in os.walk(NEW_PACKAGE_DIR):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        replace_placeholders(file_path, placeholders)

print(f"\nThe package '{parameters['package_name']}' has been successfully generated in {NEW_PACKAGE_DIR}.\n")

# %% Git Repository

# Initialize a new Git repository
os.chdir(NEW_PACKAGE_DIR)  # Change directory to the new package directory
subprocess.run(["git", "init"], check=True)  # Initialize a new git repository
subprocess.run(["git", "add", "."], check=True)  # Add all files to staging
subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)  # Commit the changes

# Rename the default branch to 'master'
subprocess.run(["git", "branch", "-M", "master"], check=True)

if parameters["remote_url"]:
    # Set up the upstream repository and push
    push_command = (
        f"git push --set-upstream git@{parameters['remote_url']}/"
        f"$(git rev-parse --show-toplevel | xargs basename).git "
        f"$(git rev-parse --abbrev-ref HEAD)"
    )
    subprocess.run(push_command, shell=True, check=True)

    print(f"\nA new Git repository has been initialized in {NEW_PACKAGE_DIR}.")

else:
    print(f"\nA new local Git repository has been initialized in {NEW_PACKAGE_DIR}.")
