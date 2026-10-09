# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [v3.0.0] - Unreleased

### Added

- Adopt `src/` layout: package source code moved to `src/<package_name>/`
- Add full `[project]` section in `pyproject.toml` (name, version, description, authors, dependencies)
- Add `[dependency-groups]` (PEP 735) with `test` group (`pytest`, `coverage`, `tomli`) in generated `pyproject.toml`
- Add `[tool.pytest.ini_options]` (`testpaths`, `addopts`) and `core = "sysmon"` in `[tool.coverage.run]`
- Add `fallback_version = "0.0.1"` in `[tool.setuptools_scm]` for environments without git or setuptools_scm
- Add `[tool.setuptools.packages.find]` with `where = ["src"]` for src layout support
- Add `[tool.uv]` configuration: `required-environments`, `prerelease`, `exclude-newer`, `[tool.uv.exclude-newer-package]`
- Integrate CI templates from `dessia/sdk/ci-templates` in generated `.gitlab-ci.yml`
- Update `package_folder/.pre-commit-config.yaml`: ruff `v0.15.0` (`ruff-check` hook), codespell `v2.4.1`, pre-commit-hooks `v6.0.0`
- Add `{{EXCLUDE_NEWER_PACKAGES_TOML}}` placeholder: auto-generates `[tool.uv.exclude-newer-package]` from input dependencies
- Update default dependencies: `dessia_common>=1.0.3`, `volmdlr>=0.21.1`, `plot_data>=0.27.6`
- Update default `python_version` to `>=3.12`
- Add `{{RUFF_TARGET_VERSION}}` placeholder: ruff `target-version` is now derived from `python_version`

### Changed

- Replace inline CI jobs with `extends:` from ci-templates (verify changelog, pre-commit, dist wheel, install/test)
- Rename `install_run_scripts_and_unittests` to `mr_tests` and extend `.mr_test`, with an explicit
  `TEST_SCRIPT: "test.py --unittests --coverage --scripts"`: every script runs on every push, rather than
  the `--modified-scripts` default of the upstream template
- Migrate `test.py` to the runner from `dessia/sdk/experimental/templates/package-template` (doc build excluded,
  since generated packages have no `doc/` folder): unit tests now run through `pytest`, with selective execution
  (`--unittests`, `--scripts`, `--modified-scripts`, `--coverage`), JUnit reports (`report.xml`,
  `scripts-report.xml`) for the CI test widget, and glob matching for `untracked_scripts`
- Scripts no longer contribute to coverage: `test.py` runs them without the coverage tracer
- `test.py --modified-scripts` skips a script that is in the diff but absent from the working tree, naming it,
  instead of failing on an opaque `No such file or directory` (ported from the `ci-templates` fixture runner)
- Lower default coverage thresholds to `min_global_coverage = 70` / `min_module_coverage = 65`, aligned with
  `package-template`
- Update `README.md`: document that coverage measures the unit tests only, fix the example test file name and
  the `.gitlab/` tree; the generated `README.md` example tree now shows the `src/` layout
- `{{REQUIRED_PACKAGES}}` replaced by `{{REQUIRED_PACKAGES_TOML}}`: dependencies formatted as proper TOML array
- `create_package.py` updated for src layout: renames `src/folder` → `src/<package_name>`
- Skip binary files in `replace_placeholders` to avoid `UnicodeDecodeError`

### Removed

- Remove `setup.py`: `pyproject.toml` alone is enough to build and install the package
- Remove `[[tool.uv.index]]` blocks from the generated `pyproject.toml`: indexes come from the CI (`UV_DEFAULT_INDEX`/`UV_INDEX`), keeping generated packages usable without access to the private registry
- Remove the `check_mr_approval` CI job: no ci-templates job replaces it, so a generated project now relies on
  its own GitLab settings (approval rules and "Pipelines must succeed") to gate merges


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
