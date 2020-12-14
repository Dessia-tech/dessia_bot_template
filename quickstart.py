import os
import string
import sys
from typing import Tuple
import shutil
import subprocess

from pathlib import Path
parent_folder = Path(os.getcwd()).parent


manifest_template = string.Template('''recursive-include $package_name/assets *.html *.js *ts *jpg *png
recursive-include scripts *py
recursive-include $package_name/models *py
prune .git
''')

readme_template = string.Template('''# $package_name

$package_name is a Python package using DessiA SDK and DessiA coding guidelines (https://documentation.dessia.tech)

$short_description

author: $author

## Installation

Move to the folder to next to setup.py and 
```bash
python setup.py install
```

## Usage

''')


default_module_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Documentation of module goes here
"""

import dessia_common as dc
import volmdlr as vm
import volmdlr.primitives3d as p3d

'''

print('=======================')
print(' DessiA Bot quickstart')
print('=======================\n')
print('This script will generate for you the files needed to create a python package respecting DessiA guidelines.')
print("If you don't understand a question or have no preference just type enter to have the default choice selected.\n")
input('Type any key to begin the process...')
print('')

base_folder = input("Select folder in which the project will be generated (default: {}): ".format(parent_folder))
if not base_folder:
    base_folder = parent_folder
else:
    if not os.exists(base_folder):
        print('Creating base folder as it does not exists')
        os.makedirs(base_folder)
print('Project will be created in folder {}'.format(base_folder))


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


package_name = enter_valid_name('Package')
project_path = os.path.join(base_folder, package_name)
if os.path.exists(project_path):
    confirm = input('the folder {} already exists. Confirm to use existing folder (y/N): '.format(project_path))
    if confirm.lower() not in ['y', 'yes']:
        raise ValueError('Aborting in using existing folder')
else:
    os.mkdir(project_path)

package_path = os.path.join(project_path, package_name)

if not os.path.exists(package_path):
    os.mkdir(package_path)

assets_path = os.path.join(package_path, 'assets')
if not os.path.exists(assets_path):
    os.mkdir(assets_path)

shutil.copyfile('logo.png', os.path.join(assets_path, '{}.png'.format(package_name)))


setup_path = os.path.join(project_path, 'setup.py')
scripts_path = os.path.join(project_path, 'scripts')

module_name = enter_valid_name('Module', 'core')
if not module_name:
    module_name = 'core'


shutil.copyfile('setup_template.py', setup_path)

if not os.path.exists(scripts_path):
    os.mkdir(scripts_path)

init_path = os.path.join(package_path, '__init__.py')
if not os.path.exists(init_path):
    init_file = open(init_path, 'x+')
    init_file.writelines(["import pkg_ressources\n", 
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

short_description = input('Enter a short description : ')
author_name = input('Enter your name : ')
author_mail = input('Enter your e-mail : ')
default_requirements = ['dessia_common>=0.4.0', 'volmdlr>=0.2.0']
requirements = input("Enter required packages, separated by a coma (default : {})".format(default_requirements))
python_version = input('Enter Python version (default : >=3.8) : ')
if not requirements:
    requirements = default_requirements
else:
    requirements = requirements.split(',')

if not python_version:
    python_version = ">=3.8"

from_git_tags = input('Do you want to enable version from git tags? (Y/n): ')

# Gitignore
create_gitignore = input('Do you want to create a python gitignore file? (Y/n): ')
create_gitignore = create_gitignore.lower() != 'n'

gitignore_path = os.path.join(project_path, '.gitignore')
if create_gitignore:
    shutil.copyfile('python.gitignore', gitignore_path)

# README
create_readme = input('Do you want to create a README file? It will be used as long description. (Y/n): ')
create_readme = create_readme.lower() != 'n'

readme_path = os.path.join(project_path, 'README.md')
if create_readme:
    with open(readme_path, 'w') as f:
        f.write(readme_template.substitute(
            package_name=package_name,
            author='{} ({})'.format(author_name, author_mail),
            short_description=short_description,
            ))



# Writing file
setup_str = "\n\nsetup(\n"
if from_git_tags.lower() == 'n':
    setup_str += "\tversion='0.0.1',\n"
else:
    setup_str += "\tversion=get_version(),\n"

setup_str += "\tname='{}',\n".format(package_name)
setup_str += "\tdescription='{}',\n".format(short_description)
if create_readme:
    setup_str += "\tlong_description=readme(),\n"
else:
    setup_str += "\tlong_description='',\n"

setup_str += "\tauthor='{}',\n".format(author_name)
setup_str += "\tauthor_email='{}',\n".format(author_mail)
setup_str += "\tinstall_requires={},\n".format(requirements)
setup_str += "\tpython_requires='{}',\n".format(python_version)
setup_str += "\tpackages=find_packages(),\n"
setup_str += ")"

setup_file = open(setup_path, 'a+')
setup_file.write(setup_str)


manifest_path = os.path.join(project_path, 'MANIFEST.in')
if not os.path.exists(manifest_path):
    with open(manifest_path, 'w') as f:
        f.write(manifest_template.substitute(package_name=package_name))


print('Project generated to {}'.format(project_path))
