import os
import shutil
from datetime import date
import subprocess
from methods.methods_get_parameters_from_excel import get_parameters_from_excel

# %% Inputs

parameters = get_parameters_from_excel(excel_file='PackageTemplate_Inputs.xlsx')

# %% New Directory

# Path to the template directory
template_dir = 'package_foler'
new_package_dir = f'../{parameters["project_package_name"]}'

# Copy the template directory to a new location
shutil.copytree(template_dir, new_package_dir)

# Rename the package folder
old_folder = f'../{parameters["project_package_name"]}/folder'
new_folder = f'../{parameters["project_package_name"]}/' + parameters["package_name"]
os.rename(old_folder, new_folder)

# %% Updates the files

# Function to replace placeholders in a file
def replace_placeholders(file_path, placeholders):
    with open(file_path, 'r') as file:
        content = file.read()
    for placeholder, value in placeholders.items():
        content = content.replace(placeholder, value)
    with open(file_path, 'w') as file:
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
    '{{REQUIRED_PACKAGES}}': parameters["required_packages"]}


# Recursively find and update all files in the new package directory
for root, dirs, files in os.walk(new_package_dir):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        replace_placeholders(file_path, placeholders)

print(f"The package '{parameters['package_name']}' has been successfully generated in {new_package_dir}.")

# %% Git Repository

# Initialize a new Git repository
os.chdir(new_package_dir)  # Change directory to the new package directory
subprocess.run(['git', 'init'])  # Initialize a new git repository
subprocess.run(['git', 'add', '.'])  # Add all files to staging
subprocess.run(['git', 'commit', '-m', 'Initial commit'])  # Commit the changes

# Rename the default branch to 'master'
subprocess.run(['git', 'branch', '-M', 'master'])


# Set up the upstream repository and push
push_command = (
    f"git push --set-upstream git@{parameters['remote_url']}/"
    f"$(git rev-parse --show-toplevel | xargs basename).git "
    f"$(git rev-parse --abbrev-ref HEAD)"
)
subprocess.run(push_command, shell=True)

print(f"A new Git repository has been initialized in {new_package_dir}.")
