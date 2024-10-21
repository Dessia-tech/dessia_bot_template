# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - Unreleased

### Added

- Set up the remote repository to the new local Git repository

### Changed

### Deprecated

### Removed

### Fixed

### Security

### Performance

### Other


## [v2.0.0-rc.1] - 11/10/2024

### Added

- `template_inputs.ini` file for configuring new package inputs
- `create_package.py` script to generate new Python packages from a template directory
- `pyproject.toml` file for project metadata, dependencies, and tool-specific settings
- New directory structure:
    -  `my_package/`: Main source code directory
    -  `scripts/`: Directory for utility scripts
    -  `tests/`: Directory for unit tests
    -  `CHANGELOG.md` File for tracking changes
    -  `README.md`: Main documentation file
    -  `setup.py`: Installation and package metadata
    -  `pyproject.toml`: Configuration file defining project metadata, dependencies, and tool-specific settings
    -  `test.py`: Script for running unittests and scripts with coverage
    -  `.gitlab/`: GitLab configuration files and templates
    -  `.gitlab-ci.yml`: File for GitLab CI/CD pipeline configuration
    -  `.gitignore`: File for Git ignore rules
    -  `.pre-commit-config.yaml`: File for pre-commit hooks configuration
- New tools for code quality checking and improving

### Changed

- Updated `README.md` with new project information and structure
- Reorganized project structure for better maintainability

### Removed

- Delete unused files that are no longer needed for the project:
    - pep8, .pylintrc, ci_tests.py, coverage.py, python.gitignore, quickstart.py, setup_template.py, templates.py


## [v1.0.0] - 02/10/2023

### Changed

- ‎Update README.md

## [v0.1.0] - 07/01/2021

### Added

- Add quickstart.py


## [v0.0.1] - 22/10/2020 (Initialization)


