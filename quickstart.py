import os
import sys
from typing import Tuple
import shutil
import subprocess

if os.path.exists('setup.py') and not os.path.isdir('setup.py'):
    sys.exit('setup.py already exist in this directory. \nQuickstart aborted.')


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
            msg += ' It must not contain caps nor special characters '
            msg += 'and must be longer than 3 characters.\n'
            msg += 'Please retry. ({}/10)'.format(n_retries)
            print(msg)
    if not valid_name:
        msg = 'Maximum retries exceeded, {} name is not valid'.format(target)
        raise ValueError(msg)
    return name


package_name = enter_valid_name('Package')
module_name = enter_valid_name('Module', 'core')
if not module_name:
    module_name = 'core'

shutil.copyfile('setup_template.py', 'setup.py')

if not (os.path.exists(package_name) and os.path.isdir(package_name)):
    os.mkdir(package_name)
os.mkdir('scripts')

init_file = open('{}/__init__.py'.format(package_name), 'x+')
init_file.write("from .{} import *".format(module_name))
module_file = open('{}/{}.py'.format(package_name, module_name), 'x+')
module_file.write("is_created = True")
setup_file = open('setup.py'.format(package_name), 'a+')

short_description = input('Enter a short description : ')
author_name = input('Enter your name : ')
author_mail = input('Enter your e-mail : ')
requirements = input("Enter required packages, separated by a coma (default : ['dessia_common'])")
python_version = input('Enter Python version (default : >=3.8) : ')
if not requirements:
    requirements = ['dessia_common']
else:
    requirements = requirements.split(',')

if not python_version:
    python_version = ">=3.8"

setup_str = "\n\nsetup(\n"
setup_str += "\tversion='0.0.0',\n"
setup_str += "\tname='{}',\n".format(package_name)
setup_str += "\tdescription='{}',\n".format(short_description)
setup_str += "\tlong_description=readme(),\n"
setup_str += "\tauthor='{}',\n".format(author_name)
setup_str += "\tauthor_email='{}',\n".format(author_mail)
setup_str += "\tinstall_requires={},\n".format(requirements)
setup_str += "\tpython_requires='{}',\n".format(python_version)
setup_str += "\tpackages=find_packages(),\n"
setup_str += ")"

setup_file.write(setup_str)
