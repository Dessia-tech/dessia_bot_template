"""Script to generate a new Python package from a template directory."""

import os
import shutil
import subprocess
from datetime import date

from methods.methods_get_parameters_from_ini_file import get_parameters_from_ini_file

# %% Inputs

parameters = get_parameters_from_ini_file(ini_file="template_inputs.ini")

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
    "{{SHORT_DESCRIPTION}}": parameters["short_description"],
    "{{AUTHOR}}": parameters["author"],
    "{{CONTACT}}": parameters["email"],
    "{{VERSION}}": parameters["python_version"],
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
subprocess.run(["git", "init"], check=True)  # Initialize a new git repository
subprocess.run(["git", "add", "."], check=True)  # Add all files to staging
subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)  # Commit the changes

# Rename the default branch to 'master'
subprocess.run(["git", "branch", "-M", "master"], check=True)

if parameters["package_url"]:
    try:
        # Set up the remote repository
        remote_url = f"git@{parameters['package_url']}/{parameters['project_package_name']}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

        # Push to the remote repository
        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)

        print(f"\nA new Git repository has been initialized in {new_package_dir}.")

    except:
        print("\nAn error occurred")
        print("Please check your GitLab access and permissions.")

        if not ("gitlab" in parameters["package_url"].lower() or "github" in parameters["package_url"].lower()):
            print(
                "\nAre you sure about your 'Package URL' ? It seems that is not a Git URL\n"
                + "If you do not need to use Git, leave an empty cell."
            )

else:
    print(f"\nA new local Git repository has been initialized in {new_package_dir}.")
