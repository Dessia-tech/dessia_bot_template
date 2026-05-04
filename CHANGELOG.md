# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [v3.0.0] - Unreleased

### Added

- Adopt `src/` layout: package source code moved to `src/<package_name>/`
- Add full `[project]` section in `pyproject.toml` (name, version, description, authors, dependencies)
- Add `[dependency-groups]` (PEP 735) with `test` group (`coverage`, `tomli`) in generated `pyproject.toml`
- Add `fallback_version = "0.0.1"` in `[tool.setuptools_scm]` for environments without git or setuptools_scm
- Add `[tool.setuptools.packages.find]` with `where = ["src"]` for src layout support
- Add `[tool.uv]` configuration: `required-environments`, `prerelease`, `exclude-newer`, `[tool.uv.exclude-newer-package]`
- Add GitLab and PyPI index configuration via `[[tool.uv.index]]` in generated `pyproject.toml`
- Integrate CI templates from `dessia/sdk/ci-templates` in generated `.gitlab-ci.yml`
- Update `package_folder/.pre-commit-config.yaml`: ruff `v0.15.0` (`ruff-check` hook), codespell `v2.4.1`, pre-commit-hooks `v6.0.0`
- Add `coverage xml` output in `test.py`
- Add module-level constants in `test.py` (`PROJECT_ROOT`, `COVERAGE_FILE`, `COVERAGE_RCFILE`, `COVERAGE_SOURCE`)
- Add `{{EXCLUDE_NEWER_PACKAGES_TOML}}` placeholder: auto-generates `[tool.uv.exclude-newer-package]` from input dependencies
- Update default dependencies: `dessia_common>=1.0.3`, `volmdlr>=0.21.1`, `plot_data>=0.27.6`
- Update default `python_version` to `>=3.12`

### Changed

- Replace `setup.py` with a minimal compatibility wrapper reading metadata from `pyproject.toml`
- Replace inline CI jobs with `extends:` from ci-templates (verify changelog, pre-commit, dist wheel, install/test)
- All `coverage` commands now use explicit `--data-file` and `--source` arguments in `test.py`
- Script path comparison in `test.py` uses `.as_posix()` for cross-platform consistency
- `{{REQUIRED_PACKAGES}}` replaced by `{{REQUIRED_PACKAGES_TOML}}`: dependencies formatted as proper TOML array
- `create_package.py` updated for src layout: renames `src/folder` → `src/<package_name>`
- Skip binary files in `replace_placeholders` to avoid `UnicodeDecodeError`


## [v2.0.0] - 04/05/2026

### Added

- Add error handling for Git repository initialization and push operations, providing clearer feedback on GitLab access and permission issues
- Check merge request approvals during CI

### Changed

- Use modern PEP 517-compliant commands for building wheels
- Add guidance comments to README template sections

### Fixed

- Enhance URL handling to support various formats and types


## [v2.0.0-rc.2] - 26/11/2024

### Added

- Set up the remote repository to the new local Git repository
- Add CI trigger on tag push for dist build
- Update files extensions to skip in codespell

### Fixed

- Remove numpy dependency in unit tests


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

- Update README.md

## [v0.1.0] - 07/01/2021

### Added

- Add quickstart.py


## [v0.0.1] - 22/10/2020 (Initialization)
