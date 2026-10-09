# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [v3.0.0] - 09/10/2026

### Added

- `src/` layout, with `pyproject.toml` as the single source of truth: full `[project]` section,
  `[dependency-groups]` (PEP 735) with a `test` group, `setuptools_scm` with a fallback version, and the
  ruff, pytest and coverage configuration
- `[tool.uv]` configuration: `required-environments`, `prerelease` and `exclude-newer`
- CI from `dessia/sdk/ci-templates`: changelog, pre-commit, test and wheel jobs are now `extends:` of shared
  templates

### Changed

- New defaults: Python `>=3.12`, `dessia_common>=1.0.11`, `volmdlr>=0.22.5`, `plot_data>=0.27.8`, and current
  pre-commit hooks. Ruff's `target-version` is derived from `python_version` instead of being hardcoded
- `test.py` is the runner from `dessia/sdk/experimental/templates/package-template`, minus the doc build: unit
  tests run through `pytest`, execution is selective (`--unittests`, `--scripts`, `--modified-scripts`,
  `--coverage`), and JUnit reports feed the merge request test widget
- **Coverage measures the unit tests only.** Scripts run without the coverage tracer, so the code they exercise
  no longer counts; default thresholds drop to `min_global_coverage = 70` / `min_module_coverage = 65`
- The merge request job runs `test.py --unittests --coverage --scripts`: every test and every script, on every
  push, blocking
- `create_package.py` follows the src layout and formats dependencies as a TOML array
- READMEs brought back in line with the template, and `tests/test_exemple.py` renamed to `tests/test_example.py`

### Fixed

- An empty `required_packages` falls back to the default dependencies, instead of generating a package with none
- Generated files end with exactly one newline, so `check_pre_commit` no longer fails on a generated project's
  first merge request
- `test.py --modified-scripts` skips, and names, a script that is in the diff but absent from the working tree
- Binary files are skipped when replacing placeholders

### Removed

- `setup.py`: `pyproject.toml` alone builds and installs the package
- `[[tool.uv.index]]` and `[tool.uv.exclude-newer-package]` from the generated `pyproject.toml`: both describe the
  Dessia infrastructure and come from the CI, or from the developer's own `uv` configuration, so a generated
  package stays usable without access to the private registry
- The `check_mr_approval` CI job: approval is enforced by the project's own GitLab settings


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
