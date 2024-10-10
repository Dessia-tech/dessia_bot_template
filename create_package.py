"""Script to generate a new Python package from a template directory."""

import os
import shutil
import subprocess
from datetime import date

from methods.methods_get_parameters_from_excel import get_parameters_from_excel

# %% Inputs

parameters = get_parameters_from_excel(excel_file="Template_Inputs.xlsx")

# %% New Directory

# Path to the template directory
template_dir = "package_folder"
new_package_dir = f'../{parameters["project_package_name"]}'

# Copy the template directory to a new location
shutil.copytree(template_dir, new_package_dir)

# Rename the package folder
old_folder = f'../{parameters["project_package_name"]}/folder'
new_folder = f'../{parameters["project_package_name"]}/' + parameters["package_name"]
os.rename(old_folder, new_folder)

# %% Updates the files


# Function to replace placeholders in a file
def replace_placeholders(_file_path: str, _placeholders: dict) -> None:
    """Replace placeholders in a file with the corresponding values."""
    with open(_file_path, encoding="utf-8") as file:
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
for root, _dirs, files in os.walk(new_package_dir):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        replace_placeholders(file_path, placeholders)

print(f"\nThe package '{parameters['package_name']}' has been successfully generated in {new_package_dir}.\n")

# %% Git Repository

# Initialize a new Git repository
os.chdir(new_package_dir)  # Change directory to the new package directory
subprocess.run(["git", "init"], check=False)  # Initialize a new git repository
subprocess.run(["git", "add", "."], check=False)  # Add all files to staging
subprocess.run(["git", "commit", "-m", "Initial commit"], check=False)  # Commit the changes

# Rename the default branch to 'master'
subprocess.run(["git", "branch", "-M", "master"], check=False)

if parameters["remote_url"]:
    # Set up the upstream repository and push
    push_command = (
        f"git push --set-upstream git@{parameters['remote_url']}/"
        f"$(git rev-parse --show-toplevel | xargs basename).git "
        f"$(git rev-parse --abbrev-ref HEAD)"
    )
    subprocess.run(push_command, shell=True, check=False)

    print(f"\nA new Git repository has been initialized in {new_package_dir}.")

else:
    print(f"\nA new local Git repository has been initialized in {new_package_dir}.")
