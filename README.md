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

**dessia_bot_template** is a streamlined tool designed to help developers quickly generate new Python packages by providing a pre-configured project structure. By simply filling out a configuration .ini file with essential package metadata, users can create a new package with all the necessary structure, including essential files like `pyproject.toml`, `README.md`, and tests.

This template simplifies the process of starting a new Python project, allowing you to focus more on coding and less on setup.


## Features

   - **Standardized `src/` Layout:**
    Automatically creates a well-organized directory structure following the modern Python `src` layout, ensuring your project is easy to navigate and adheres to Python best practices.

   - **`pyproject.toml` as Single Source of Truth:**
    All package metadata, dependencies, versioning, and tool configuration are defined in a single `pyproject.toml` file. No `setup.py` is needed.

   - **Automatic Versioning with Fallback:**
    Uses `setuptools_scm` to derive the package version from git tags. A `fallback_version` is configured to ensure wheel builds work even when git or `setuptools_scm` is unavailable (e.g. on client environments).

   - **`uv` Package Manager Support:**
    The generated package declares the `required-environments` the SDK wheels need, so `uv` resolves for Linux and Windows regardless of the machine it runs on.

    The resolution policy itself is deliberately kept out of the generated `pyproject.toml`, so the package stays usable by someone without access to the private registry: the package indexes, `prerelease` handling and the `exclude-newer` supply chain protection -- together with the exemptions that keep the internal SDK packages installable the day they are released -- come from the CI (`UV_DEFAULT_INDEX`/`UV_INDEX` and `.uv_setup` in the `ci-templates` `common.yml`), and locally from the developer's own `uv` configuration (`~/.config/uv/uv.toml`, or `%APPDATA%\uv` on Windows). That configuration is part of setting up a development machine, next to the GitLab token.

   - **Dependency Groups (PEP 735):**
    Development and test dependencies are managed via `[dependency-groups]`, natively supported by `uv`.

   - **Example Test Cases:**
    Includes a set of example test cases to get you started with testing your package. The `test.py` script runs unit tests through `pytest` and executes the scripts, with selective execution (`--unittests`, `--scripts`, `--modified-scripts`, `--coverage`), coverage reporting (text, HTML, XML, JSON) and JUnit reports for the CI test widget.

    Coverage measures the unit tests only. Scripts run without the coverage tracer, so the code they exercise does not count towards it — a script that fails still fails the job, but it contributes nothing to the percentage. The thresholds in `[coverage]` (`min_global_coverage`, `min_module_coverage`) default to 70 and 65 and should be read with that in mind.

   - **Customizable Package Metadata:**
    Easily customize your package's name, author information, descriptions, dependencies, and more through a configuration `.ini` inputs file.

   - **Python Version and Dependency Management:**
    Specify the required Python version and manage package dependencies directly from the configuration `.ini` inputs file. Dependencies are automatically formatted as a proper TOML array in `pyproject.toml`.

   - **Error Handling and Validation:**
    Built-in checks validate your input data, such as checking for valid package names, correctly formatted email addresses, and non-conflicting dependencies.

   - **CI/CD with `dessia/sdk/ci-templates`:**
    The generated `.gitlab-ci.yml` uses shared CI templates for changelog verification, pre-commit checks, test execution, and wheel distribution — keeping pipeline configuration minimal and consistent across projects.

   - **Built-in Documentation Support:**
    Automatically generates a basic `README.md` file based on your inputs, providing a starting point for your project documentation.


## Getting Started

1. **Prerequisites**

Before using this template, ensure you have the following installed:

- Python: Version 3.12 or later.
- Git: Version control system to manage your codebase — Optional.
- uv: Modern Python package manager — Optional but recommended (`pip install uv`).


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

Open the file `template_inputs.ini`, and fill in the following fields:

   - **package_name**: This is the unique name of your Python package. It should be all lowercase and use underscores to separate words (e.g., my_package).
   - **short_description**: A concise summary of what your package does. This will appear in package listings and should be clear and to the point. Aim for one sentence.
   - **long_description**: A more detailed description of your package. This can be a few paragraphs long and should explain the package's features, use cases, and any important details. This will typically be included in the README.md file which can be updated after.
   - **required_packages**: A list of other Python packages that your package depends on. These dependencies will be automatically installed when your package is installed. List each package separated by a comma.
   - **python_version**: The minimum version of Python that your package is compatible with. Specify the version in the format >= followed by the version number.
   - **author**: The name of the person or team responsible for maintaining the package. This should be the operations-team that will handle updates, support, and maintenance of the package.
   - **email**: The contact email of the person or team responsible of the package. This email should be monitored for any support requests, questions, or issues related to the package.
   - **package_url**: This URL where the package's source code will be created. Typically, this will be the URL of the repository hosting the package (e.g., a GitLab, GitHub repository) - Optional. Like: gitlab.com/Organisation


**Example:**

```
| Item             | Example                                                                         |
├──────────────────├─────────────────────────────────────────────────────────────────────────────|
| package_name     | my_package                                                                      |
| short_description| A package that does awesome things                                              |
| long_description | This package provides awesome features for awesome people.                      |
| required_packages| dessia_common>=1.0.11, volmdlr>=0.22.5, plot_data>=0.27.8                        |
| python_version   | >=3.12                                                                          |
| author           | Operations-Team                                                                 |
| email            | support@dessia.io                                                               |
| package_url      | gitlab.com/Organisation/ClientFolder                                            |
```

2. **Run the Script**

After filling in the `.ini` inputs file, run the `create_package.py` script to generate your new package:

```
python3 create_package.py
```

The script will:

   - Create a new directory for your package.
   - Populate it with the necessary files (e.g., `pyproject.toml`, `README.md`, `.gitlab-ci.yml`, etc.).
   - Format your dependencies as a proper TOML array in `pyproject.toml`.

3. **After Generation**

Once the package directory is created, install the dependencies with `uv`:

```bash
cd ../MyPackage
uv sync
```


## Directory Structure

Here's an overview of the directory structure provided by this template:

```
MyPackage/
├── src/
│   └── my_package/               # Main source code directory
│       ├── __init__.py           # Initialize your package
│       ├── module_1.py           # Example module 1
│       └── module_2.py           # Example module 2
├── scripts/                      # Directory for utility scripts related to the package
│   ├── script_1.py               # Utility script 1
│   └── script_2.py               # Utility script 2
├── tests/                        # Directory for unit tests
│   ├── __init__.py               # Initialize test package
│   └── test_example.py           # Example test file
├── CHANGELOG.md                  # Changelog for tracking changes
├── README.md                     # Main documentation file
├── pyproject.toml                # Single source of truth: metadata, dependencies, tools, uv config
├── test.py                       # Test runner: unit tests, scripts, coverage, JUnit reports
├── .gitlab/                      # GitLab configuration files and templates
│   ├── issue_templates/          # Template for submitting issues
│   └── merge_request_templates/  # Template for merge requests
├── .gitlab-ci.yml                # GitLab CI/CD pipeline configuration (uses ci-templates)
├── .gitignore                    # Git ignore rules
└── .pre-commit-config.yaml       # Pre-commit hooks configuration
```


## Troubleshooting

   - Git Push Failures:
     Ensure you have push access to the remote repository. If you encounter authentication issues, check your Git credentials and SSH keys.

   - Package Name Conflicts:
     Be sure that the chosen package name does not already exist in your organization or on PyPI. So, consider choosing a different name to avoid conflicts.

   - Wheel Build Without Git:
     If `setuptools_scm` cannot detect the git version (e.g. on a client machine), the `fallback_version = "0.0.1"` defined in `pyproject.toml` will be used automatically.


## Contact

For any questions or issues, please contact the Operations-Team.
