import os
import shutil

from typing import Tuple
from pathlib import Path

import setup_template as st
from templates import manifest_template, readme_template, default_module_content, drone_template, test_template,\
                        code_quality_template, code_pep8_template, code_pylint_template, setup_template


def has_special_char(string: str) -> Tuple[bool, str]:
    for char in ['&', 'é', '~', '"', ',', "'", '{', '(', '£',
                 ',', '-', '|', 'è', "`", 'ç', '^', ';', '$',
                 'à', '@', ')', ']', '°', '=', '}', ':', 'µ'
                 '+', '*', '/', '.', '\\', '?', '!', '%', 'ù']:
        if char in string:
            return True, char
    return False, ''


def enter_valid_name(target: str, default: str = None):
    valid_name = False
    n_retries = 0
    while not valid_name and n_retries < 10:
        if default is None:
            prompt = 'Enter {} name : '.format(target)
        else:
            prompt = 'Enter {} name (default : {}) : '.format(target, default)
        name = input(prompt)
        has_special, special_char = has_special_char(name)
        if not name and default is not None:
            name = default

        valid_name = (len(name) > 3 and name.islower() and not has_special)
        if not valid_name:
            n_retries += 1
            msg = '{} name is not valid.\n'.format(target)
            msg += 'It must not contain caps nor special characters apart from "_"'
            msg += 'and must be longer than 3 characters.\n'
            msg += 'Please retry. ({}/10)'.format(n_retries)
            print(msg)
    if not valid_name:
        msg = 'Maximum retries exceeded, {} name is not valid'.format(target)
        raise ValueError(msg)
    return name


def check_git_use(git_use, package_name, parent_folder):
    if git_use:
        input('Create a repository on your service (Github, Gitlab, Gitea, Gogs) and clone it on your computer. '
              'Press enter when done')
        git_detected = False
        while not git_detected:
            project_path = input('Where is the git repo folder? current folder: {}: '.format(parent_folder))
            if not os.path.isabs(project_path):
                project_path = os.path.join(parent_folder, project_path)
            git_folder = os.path.join(project_path, '.git')
            if os.path.isdir(git_folder):
                print('{} is a valid git repo'.format(project_path))
                git_detected = True
            else:
                print('No .git subfolder found in {} Please retry.'.format(project_path))
    else:
        base_folder = input("Select parent folder in which the project will be generated "
                            "(default: {}): ".format(parent_folder))
        if not base_folder:
            base_folder = parent_folder
        else:
            if not os.path.exists(base_folder):
                print('Creating base folder as it does not exists')
                os.makedirs(base_folder)
        print('Project will be created in folder {}'.format(base_folder))
        project_path = os.path.join(base_folder, package_name)

        if os.path.exists(project_path):
            confirm = input('the folder {} already exists. Confirm to use existing folder (y/N): '.format(project_path))
            if confirm.lower() not in ['y', 'yes']:
                raise ValueError('Aborting in using existing folder')
        else:
            os.mkdir(project_path)
    return project_path


def create_base(project_path, package_name, module_name):
    package_path = os.path.join(project_path, package_name)

    if not os.path.exists(package_path):
        os.mkdir(package_path)

    assets_path = os.path.join(package_path, 'assets')
    if not os.path.exists(assets_path):
        os.mkdir(assets_path)

    shutil.copyfile(os.path.join(Path(__file__).parent.resolve(), 'logo.png'),
                    os.path.join(assets_path, '{}.png'.format(package_name)))

    setup_path = os.path.join(project_path, 'setup.py')
    scripts_path = os.path.join(project_path, 'scripts')

    if not module_name:
        module_name = 'core'

    # shutil.copyfile('setup_template.py', setup_path)

    if not os.path.exists(scripts_path):
        os.mkdir(scripts_path)

    init_path = os.path.join(package_path, '__init__.py')
    if not os.path.exists(init_path):
        init_file = open(init_path, 'x+')
        init_file.writelines(["import pkg_resources\n",
                              "from .{} import *\n".format(module_name),
                              '__version__ = pkg_resources.require("{}")[0].version\n'.format(package_name)])
    else:
        print('__init__.py already exists, skipping creation')

    module_path = os.path.join(package_path, '{}.py'.format(module_name))
    if not os.path.exists(module_path):
        module_file = open(module_path, 'x+')
        module_file.write(default_module_content)
    else:
        print('base python module already exists, skipping creation')
    return setup_path, module_path


def change_requirements(requirements, default_requirements, python_version):
    if not requirements:
        requirements = default_requirements
    else:
        requirements = requirements.split(',')

    if not python_version:
        python_version = ">=3.8"
    return requirements, python_version


def create_gitignore(answer, project_path):
    gitignore_path = os.path.join(project_path, '.gitignore')
    if answer:
        shutil.copyfile(os.path.join(Path(__file__).parent.resolve(), 'python.gitignore'), gitignore_path)


def create_readme(answer, project_path, package_name, author_name, author_mail, short_description):
    readme_path = os.path.join(project_path, 'README.md')
    if answer:
        with open(readme_path, 'w') as f:
            f.write(readme_template.substitute(
                package_name=package_name,
                author='{} ({})'.format(author_name, author_mail),
                short_description=short_description,
                ))


def create_tests(project_path, package_name):
    tests_dir = os.path.join(project_path, 'tests')
    if not os.path.exists(tests_dir):
        os.mkdir(tests_dir)

    for test_filename in ['coverage.py', 'ci_tests.py']:
        test_file_path = os.path.join(tests_dir, test_filename)
        shutil.copyfile(os.path.join(Path(__file__).parent.resolve(), test_filename), test_file_path)

    test_path = os.path.join(tests_dir, 'test.py')
    with open(test_path, 'w') as f:
        f.write(test_template.substitute(package_name=package_name,))


def code_quality(answer, project_path, package_name):
    if answer:
        for filename in ['.pep8', '.pylintrc']:
            cq_path = os.path.join(project_path, filename)
            shutil.copyfile(os.path.join(Path(__file__).parent.resolve(), filename), cq_path)

        for code_quality_filename, template_name in [('code_pep8.sh', code_pep8_template),
                                                     ('code_quality.sh', code_quality_template),
                                                     ('code_pylint.py', code_pylint_template)]:
            # cq_path = os.path.join(package_path, code_quality_filename)
            # shutil.copyfile(code_quality_filename, cq_path)
            with open(os.path.join(project_path, code_quality_filename), 'w') as f:
                f.write(template_name.substitute(
                    package_name=package_name,
                    ))


def create_drone(answer, project_path, package_name):
    if answer:
        drone_path = os.path.join(project_path, '.drone.yml')
        with open(drone_path, 'w') as f:
            f.write(drone_template.substitute(
                package_name=package_name))


def change_from_git_tags(answer):
    # Writing setup file
    if not answer:
        version = '0.0.1'
    else:
        version = st.get_version()
    return version

# setup_str += "\tname='{}',\n".format(package_name)
# setup_str += "\tdescription='{}',\n".format(short_description)
# if create_readme:
#     setup_str += "\tlong_description=readme(),\n"
#     setup_str += "\tlong_description_content_type='text/markdown',\n"
# else:
#     setup_str += "\tlong_description='',\n"

# setup_str += "\tauthor='{}',\n".format(author_name)
# setup_str += "\tauthor_email='{}',\n".format(author_mail)
# setup_str += "\tinstall_requires={},\n".format(requirements)
# setup_str += "\tpython_requires='{}',\n".format(python_version)
# setup_str += "\tpackages=find_packages(),\n"
# setup_str += ")"


def create_project(setup_path, project_path, package_name, version, short_description, author_name, author_mail,
                   requirements, python_version):
    setup_str = setup_template.substitute(package_name=package_name,
                                          version=version,
                                          short_description=short_description,
                                          author_name=author_name,
                                          author_mail=author_mail,
                                          requirements=requirements,
                                          python_version=python_version)

    with open(setup_path, 'w') as setup_file:
        setup_file.write(setup_str)

    manifest_path = os.path.join(project_path, 'MANIFEST.in')
    if not os.path.exists(manifest_path):
        with open(manifest_path, 'w') as f:
            f.write(manifest_template.substitute(package_name=package_name))
