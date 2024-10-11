## dessia_bot_template

This repository provides a template for creating new Python packages. It includes all the necessary boilerplate code and directory structure to help you get started quickly and maintain consistency across your projects.


## Table of Contents

   - [Overview](#overview)
   - [Features](#features)
   - [Getting Started](#getting-started)
   - [Usage](#usage)
   - [Directory Structure](#directory-structure)
   - [Troubleshooting](#troubleshooting)
   - [Contact](#contact)


## Overview

**dessia_bot_template** is a streamlined tool designed to help developers quickly generate new Python packages by providing a pre-configured project structure. By simply filling out a configuration .ini file with essential package metadata, users can create a new package with all the necessary structure, including essential files like setup.py, README.md, and tests, initialize a Git repository, and push it to a remote Git repository.

This template simplifies the process of starting a new Python project, allowing you to focus more on coding and less on setup.


## Features

   - **Standardized Directory Structure for Python Packages:**
Automatically creates a well-organized directory structure, including directories for your package's modules, tests, and additional resources. This ensures your project is easy to navigate and adheres to Python best practices.

   - **Pre-configured setup.py and pyproject.toml for Easy Package Installation and Distribution:**
    Provides a ready-to-use setup.py and pyproject.toml files tailored to your package's metadata. These files simplifie the installation process and make your package easily distributable via PyPI or other distribution platforms.

   - **Example Test Cases Using pytest:**
    Includes a set of example test cases to get you started with testing your package using pytest. This helps ensure your package is robust and reliable, encouraging best practices in test-driven development.

   - **Automated Git Initialization and Remote Repository Setup:**
    Automatically initializes a Git repository for your package, commits the initial setup, and pushes it to a remote repository specified by you. This feature helps you manage your code from the very beginning with version control.

   - **Customizable Package Metadata:**
    Easily customize your package's name, version, author information, descriptions, and more through a configuration .ini inputs file. This flexibility allows you to tailor the package to your specific project requirements.

   - **Python Version and Dependency Management:**
    Specify the required Python version and manage package dependencies directly from the configuration .ini inputs file. This ensures your package is compatible with the intended Python environment and has all necessary dependencies.

   - **Cross-Platform Compatibility:**
    Designed to work seamlessly on Windows, macOS, and Linux, making it accessible to developers across different platforms.

   - **Error Handling and Validation:**
    Built-in checks validate your inputs data, such as checking for valid package names, correctly formatted email addresses, and non-conflicting dependencies. This reduces the likelihood of common errors and saves you time.

   - **Expandable and Customizable:**
    The template can be easily modified to include additional files, directories, or configurations. You can extend the template to suit more complex project requirements or specific use cases.

   - **Built-in Documentation Support:**
    Automatically generates a basic README.md file based on your inputs, providing a starting point for your project documentation. This ensures your package is well-documented from the outset.

   - **Continuous integration (CI) configuration examples:**
    The template is pre-configured for easy integration with CI/CD Gitlab tools. This feature allows you to automate testing, deployment, and other processes, streamlining your development workflow.


## Getting Started

1. **Prerequisites**

Before using this template, ensure you have the following installed:

- Python: Version 3.9 or later.
- Git: Version control system to manage your codebase - Optional.


2. **Installation**


Clone this template repository to your local machine:
```
git clone https://github.com/Dessia-tech/dessia_bot_template.git
cd dessia_bot_template
```


This template includes some Python dependencies for the script, install them:

```
pip install -r requirements.txt
```

## Usage

1. **Fill in the .ini Inputs File**

Open the file template_inputs.ini, and fill in the following fields:

   - **package_name**: This is the unique name of your Python package. It should be all lowercase and use underscores to separate words (e.g., my_package).
   - **short_description**: A concise summary of what your package does. This will appear in package listings and should be clear and to the point. Aim for one sentence.
   - **long_description**: A more detailed description of your package. This can be a few paragraphs long and should explain the package’s features, use cases, and any important details. This will typically be included in the README.md file which can be updated after.
   - **required_packages**: A list of other Python packages that your package depends on. These dependencies will be automatically installed when your package is installed. List each package separated by a comma.
   - **python_version**: The minimum version of Python that your package is compatible with. Specify the version in the format >= followed by the version number.
   - **author**: The name of the person or team responsible for maintaining the package. This should be the operations-team that will handle updates, support, and maintenance of the package.
   - **email**: The contact email of the person or team responsible of the package. This email should be monitored for any support requests, questions, or issues related to the package.
   - **package_url**: This URL where the package's source code will be created. Typically, this will be the URL of the repository hosting the package (e.g., a GitLab, GitHub repository) - Optional. Like: gitlab.com/Organisation


**Example:**

```
| Item             | Example                                                    |
├──────────────────├────────────────────────────────────────────────────────────|
| package_name     | my_package                                                 |
| short_description| A package that does awesome things                         |
| long_description | This package provides awesome features for awesome people. |
| required_packages| dessia_common>=0.18.0, plot_data>=0.26.0                   |
| python_version   | >=3.9                                                      |
| author           | Operations-Team                                            |
| email            | support@dessia.io                                          |
| package_url      | gitlab.com/Organisation/ClientFolder                       |
```

2. **Run the Script**

After filling in the .ini inputs file, run the create_package.py script to generate your new package. However, if you want to push your new package to GitHub instead of GitLab, you will need to create an empty repository on GitHub before running the script.

   - Log in to your GitHub account
   - Click the "+" icon in the top-right corner and select "New repository"
   - Choose a project name for your repository (the directory containing your package): The project name is the CamelCase version of the package name choosen in the .ini inputs file
   - Do not initialize the repository with a README, .gitignore, or license
   - Click "Create repository"

Then,

   - Run the create_package.py script

```
python3 create_package.py
```

The script will:

   - Create a new directory for your package.
   - Populate it with the necessary files (e.g., setup.py, README.md, gitlab-ci.yml, etc.).
   - Initialize a local Git repository.
   - Add and commit all the files.
   - Push the initial commit to the remote repository specified in the inputs file.

3. **Push to Git**

If the script hasn't automatically pushed to the remote repository, you can manually push your changes:

```
git push -u origin master
```


## Directory Structure

Here's an overview of the directory structure provided by this template:

```
MyPackage/
├── my_package/                   # Main source code directory
│   ├── __init__.py               # Initialize your package
│   ├── module_1.py               # Example module 1
│   └── module_2.py               # Example module 2
├── scripts/                      # Directory for utility scripts related to the package
│   ├── script_1.py               # Utility script 1
│   ├── script_2.py               # Utility script 2
├── tests/                        # Directory for unit tests
│   ├── __init__.py               # Initialize test package
│   └── test_example.py           # Example test file
├── CHANGELOG.md                  # Changelog for tracking changes
├── README.md                     # Main documentation file
├── setup.py                      # Installation and package metadata
├── pyproject.toml                # Configuration file defining project metadata, dependencies, and tool-specific settings
├── test.py                       # Test script for running unittests and scripts with coverage
├── .gitlab/                      # GitLab configuration files and templates
│   ├── issue_template.md         # Template for submitting issues
│   └── merge_request_template.md # Template for merge requests
├── .gitlab-ci.yml                # GitLab CI/CD pipeline configuration
├── .gitignore                    # Git ignore rules
└── .pre-commit-config.yaml       # Pre-commit hooks configuration
```


## Troubleshooting

   - Git Push Failures:
     Ensure you have push access to the remote repository. If you encounter authentication issues, check your Git credentials and SSH keys.

   - Package Name Conflicts:
     Be sure that the chosen package name does not already exist in your organization or on PyPI. So, consider choosing a different name to avoid conflicts.


## Contact

For any questions or issues, please contact the Operations-Team.
