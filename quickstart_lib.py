import os
import shutil

from typing import Tuple
from pathlib import Path

from setup_template import get_version
from templates import (
    manifest_template,
    readme_template,
    default_module_content,
    drone_template,
    test_template,
    code_quality_template,
    code_pep8_template,
    code_pylint_template,
    setup_template,
)


def has_special_char(string: str) -> Tuple[bool, str]:
    # fmt: off
    for char in ['&', 'é', '~', '"', ',', "'", '{', '(', '£',
                 ',', '-', '|', 'è', "`", 'ç', '^', ';', '$',
                 'à', '@', ')', ']', '°', '=', '}', ':', 'µ'
                 '+', '*', '/', '.', '\\', '?', '!', '%', 'ù']:  # fmt: on
        if char in string:
            return True, char
    return False, ""


def enter_valid_name(target: str, default: str = None):
    valid_name = False
    n_retries = 0
    while not valid_name and n_retries < 10:
        if default is None:
            prompt = f"Enter {target} name : "
        else:
            prompt = f"Enter {target} name (default : {default}) : "
        name = input(prompt)
        has_special, special_char = has_special_char(name)
        if not name and default is not None:
            name = default

        valid_name = len(name) > 3 and name.islower() and not has_special
        if not valid_name:
            n_retries += 1
            msg = f"{target} name is not valid.\n"
            msg += 'It must not contain caps nor special characters apart from "_"'
            msg += "and must be longer than 3 characters.\n"
            msg += f"Please retry. ({n_retries}/10)"
            print(msg)
    if not valid_name:
        msg = f"Maximum retries exceeded, {target} name is not valid"
        raise ValueError(msg)
    return name


def check_git_use(git_use, package_name, parent_folder):
    if git_use:
        input(
            "Create a repository on your service (Github, Gitlab, Gitea, Gogs) and clone it on your computer. "
            "Press enter when done"
        )
        git_detected = False
        while not git_detected:
            project_path = input(
                f"Where is the git repo folder? current folder: {parent_folder}: "
            )
            if not os.path.isabs(project_path):
                project_path = os.path.join(parent_folder, project_path)
            git_folder = os.path.join(project_path, ".git")
            if os.path.isdir(git_folder):
                print(f"{project_path} is a valid git repo")
                git_detected = True
            else:
                print(f"No .git subfolder found in {project_path} Please retry.")
    else:
        base_folder = input(
            f"Select parent folder in which the project will be generated "
            f"(default: {parent_folder}): "
        )
        if not base_folder:
            base_folder = parent_folder
        else:
            if not os.path.exists(base_folder):
                print("Creating base folder as it does not exists")
                os.makedirs(base_folder)
        print(f"Project will be created in folder {base_folder}")
        project_path = os.path.join(base_folder, package_name)

        if os.path.exists(project_path):
            confirm = input(
                f"The folder {project_path} already exists. Confirm to use existing folder (y/N): "
            )
            if confirm.lower() not in ["y", "yes"]:
                raise ValueError("Aborting in using existing folder")
        else:
            os.mkdir(project_path)
    return project_path


def create_base(project_path, package_name, module_name):
    package_path = os.path.join(project_path, package_name)

    if not os.path.exists(package_path):
        os.mkdir(package_path)

    assets_path = os.path.join(package_path, "assets")
    if not os.path.exists(assets_path):
        os.mkdir(assets_path)

    shutil.copyfile(
        os.path.join(Path(__file__).parent.resolve(), "logo.png"),
        os.path.join(assets_path, f"{package_name}.png"),
    )

    setup_path = os.path.join(package_path, "setup.py")
    scripts_path = os.path.join(package_path, "scripts")

    if not module_name:
        module_name = "core"

    # shutil.copyfile('setup_template.py', setup_path)

    if not os.path.exists(scripts_path):
        os.mkdir(scripts_path)

    init_path = os.path.join(package_path, "__init__.py")
    if not os.path.exists(init_path):
        init_file = open(init_path, "x+")
        init_file.writelines(
            [
                f"import pkg_resources\n",
                f"from .{module_name} import *\n",
                f'__version__ = pkg_resources.require("{package_name}")[0].version\n',
            ]
        )
    else:
        print("__init__.py already exists, skipping creation")

    module_path = os.path.join(package_path, f"{module_name}.py")
    if not os.path.exists(module_path):
        module_file = open(module_path, "x+")
        module_file.write(default_module_content)
    else:
        print("base python module already exists, skipping creation")
    return setup_path, module_path


def change_requirements(requirements, default_requirements, python_version):
    if not requirements:
        requirements = default_requirements
    else:
        requirements = requirements.split(",")

    if not python_version:
        python_version = ">=3.8"
    return requirements, python_version


def create_gitignore(answer, project_path):
    gitignore_path = os.path.join(project_path, ".gitignore")
    if answer:
        shutil.copyfile(
            os.path.join(Path(__file__).parent.resolve(), "python.gitignore"),
            gitignore_path,
        )


def create_readme(
    answer, project_path, package_name, author_name, author_mail, short_description
):
    readme_path = os.path.join(project_path, "README.md")
    if answer:
        with open(readme_path, "w") as f:
            f.write(
                readme_template.substitute(
                    package_name=package_name,
                    author=f"{author_name} ({author_mail})",
                    short_description=short_description,
                )
            )


def create_tests(project_path, package_name):
    tests_dir = os.path.join(project_path, "tests")
    if not os.path.exists(tests_dir):
        os.mkdir(tests_dir)

    for test_filename in ["coverage.py", "ci_tests.py"]:
        test_file_path = os.path.join(tests_dir, test_filename)
        shutil.copyfile(
            os.path.join(Path(__file__).parent.resolve(), test_filename), test_file_path
        )

    test_path = os.path.join(tests_dir, "test.py")
    with open(test_path, "w") as f:
        f.write(
            test_template.substitute(
                package_name=package_name,
            )
        )


def code_quality(answer, project_path, package_name):
    if answer:
        for filename in [".pep8", ".pylintrc"]:
            cq_path = os.path.join(project_path, filename)
            shutil.copyfile(
                os.path.join(Path(__file__).parent.resolve(), filename), cq_path
            )

        for code_quality_filename, template_name in [
            ("code_pep8.sh", code_pep8_template),
            ("code_quality.sh", code_quality_template),
            ("code_pylint.py", code_pylint_template),
        ]:
            # cq_path = os.path.join(package_path, code_quality_filename)
            # shutil.copyfile(code_quality_filename, cq_path)
            with open(os.path.join(project_path, code_quality_filename), "w") as f:
                f.write(
                    template_name.substitute(
                        package_name=package_name,
                    )
                )


def create_drone(answer, project_path, package_name):
    if answer:
        drone_path = os.path.join(project_path, ".drone.yml")
        with open(drone_path, "w") as f:
            f.write(drone_template.substitute(package_name=package_name))


def change_from_git_tags(answer):
    # Writing setup file
    if not answer:
        version = "0.0.1"
    else:
        version = get_version()
    return version


def create_project(
    setup_path,
    project_path,
    package_name,
    version,
    short_description,
    author_name,
    author_mail,
    requirements,
    python_version,
):
    setup_str = setup_template.substitute(
        package_name=package_name,
        version=version,
        short_description=short_description,
        author_name=author_name,
        author_mail=author_mail,
        requirements=requirements,
        python_version=python_version,
    )

    with open(setup_path, "w") as setup_file:
        setup_file.write(setup_str)

    manifest_path = os.path.join(project_path, "MANIFEST.in")
    if not os.path.exists(manifest_path):
        with open(manifest_path, "w") as f:
            f.write(manifest_template.substitute(package_name=package_name))
