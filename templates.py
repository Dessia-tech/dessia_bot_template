import string

manifest_template = string.Template('''recursive-include $package_name/assets *.html *.js *ts *.jpg *.png
recursive-include scripts *.py
recursive-include $package_name/models *.py
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

test_template = string.Template('''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic test
"""

import $package_name

''')



drone_template = string.Template('''---
kind: pipeline
type: docker
name: default

steps:
- name: check code complexity, docs & code quality
  image: python:3.9
  commands:
  - pip install radon pydocstyle pylint
  - ./code_quality.sh
  - python code_pylint.py

- name: check pep8 formatting
  image: python:3.9
  when:
    branch: master
  commands:
    - git fetch --tags
    - pip3 install -U pip autopep8
    - bash code_pep8.sh
        
- name: install, run scripts and build doc
  image: python:3.9
  commands:
  - git fetch --tags
  - python setup.py install
  - pip install coverage
  - cd tests
  - coverage run --source $package_name ci_tests.py
  - coverage json
  - python coverage.py 
  - coverage report

- name: develop
  image: python:3.9
  commands:
  - python setup.py develop

''')

code_quality_template = string.Template('''
#!/bin/bash

max_pydoc_errors=10

cq_result=$$(radon cc --min E -e *pyx $package_name)
echo $$cq_result
if [[ "$$cq_result" ]];
  then 
	  echo "Error in code quality check, run radon to simplify functions">&2;
	  exit 64;
	
fi;

nb_pydoc_errors=$$(pydocstyle --count --ignore D400,D415,D404,D212,D205,D200,D203,D401,D210 $package_name *.py | tail -1)
echo "$$nb_pydoc_errors pydoc errors, limit is $$max_pydoc_errors"
if [[ "$$nb_pydoc_errors" -gt "$$max_pydoc_errors" ]];
  then 
	  echo "Error in doc quality check, run pydocstyle to correct docstrings">&2;
	  exit 64;
  else
	  echo "You can lower number of pydoc errors to $$nb_pydoc_errors (actual $$max_pydoc_errors)"
fi;
''')

code_pylint_template = string.Template('''

"""
Read pylint errors to see if number of errors does not exceed specified limits
v1.0
"""

from pylint.lint import Run

MIN_NOTE = 8.85

UNWATCHED_ERRORS = ['fixme',
                    'trailing-whitespace',
                    'import-error'
                    ]


MAX_ERROR_BY_TYPE = {
                     # No tolerance errors
                     'consider-using-f-string': 0,
                     'no-else-return': 0,
                     'arguments-differ': 0,
                     'no-member': 0,
                     'too-many-locals': 0,
                     'wrong-import-order': 0,
                     'too-many-branches': 0,
                     'unused-import': 0,
                     'unused-argument': 0,
                     'cyclic-import': 0,
                     'no-self-use': 0,
                     'unused-variable': 0,
                     'too-many-arguments': 0,
                     'unnecessary-comprehension': 0,
                     'no-value-for-parameter': 0,
                     'too-many-return-statements': 0,
                     'raise-missing-from': 0,
                     'consider-merging-isinstance': 0,
                     'abstract-method': 0,
                     'import-outside-toplevel': 0,
                     'too-many-instance-attributes': 0,
                     'consider-iterating-dictionary': 0,
                     'attribute-defined-outside-init': 0,
                     'simplifiable-if-expression': 0,
                     'redefined-builtin': 0,
                     'broad-except': 0,
                     'unspecified-encoding': 0,
                     'consider-using-get': 0,
                     'undefined-loop-variable': 0,
                     'consider-using-with': 0,
                     'eval-used': 0,
                     'too-many-nested-blocks': 0,
                     'bad-staticmethod-argument': 0,
                     'too-many-public-methods': 0,
                     'consider-using-generator': 0,
                     'too-many-statements': 0,
                     'chained-comparison': 0,
                     'wildcard-import': 0,
                     'use-maxsplit-arg': 0,
                     'arguments-renamed': 0,
                     'ungrouped-imports': 0,
                     'super-init-not-called': 0,
                     'superfluous-parens': 0,
                     'unused-wildcard-import': 0,
                     'consider-using-enumerate': 0,
                     'undefined-variable': 0,
                     'function-redefined': 0,
                     'inconsistent-return-statements': 0,
                     'unexpected-special-method-signature': 0,
                     'too-many-lines': 0,
                     'bare-except': 0,
                     }

import os
import sys
f = open(os.devnull, 'w')

old_stdout = sys.stdout
sys.stdout = f

results = Run(['$package_name', '--output-format=json', '--reports=no'], do_exit=False)
# `exit` is deprecated, use `do_exit` instead
sys.stdout = old_stdout

PYLINT_OBJECTS = True
if hasattr(results.linter.stats,'global_note'):
    pylint_note = results.linter.stats.global_note
    PYLINT_OBJECT_STATS = True
else:
    pylint_note = results.linter.stats['global_note']
    PYLINT_OBJECT_STATS = False

print('Pylint note: ', pylint_note)
assert pylint_note >= MIN_NOTE
print('You can increase MIN_NOTE in pylint to {} (actual: {})'.format(pylint_note,
                                                                      MIN_NOTE))


def extract_messages_by_type(type_):
    return [m for m in results.linter.reporter.messages if m.symbol == type_]


# uncontrolled_errors = {}
error_detected = False

if PYLINT_OBJECT_STATS:
    stats_by_msg = results.linter.stats.by_msg
else:
    stats_by_msg = results.linter.stats['by_msg']

for error_type, number_errors in stats_by_msg.items():
    if error_type not in UNWATCHED_ERRORS:
        if error_type in MAX_ERROR_BY_TYPE:
            max_errors = MAX_ERROR_BY_TYPE[error_type]
        else:
            max_errors = 0

        if number_errors > max_errors:
            error_detected = True
            print('Fix some {} errors: {}/{}'.format(error_type,
                                                     number_errors,
                                                     max_errors))
            for message in extract_messages_by_type(error_type):
                print('{} line {}: {}'.format(message.path, message.line, message.msg))
        elif number_errors < max_errors:
            print('You can lower number of {} to {} (actual {})'.format(
                error_type, number_errors, max_errors))


if error_detected:
    raise RuntimeError('Too many errors. Run pylint $package_name to get the errors')

''')

code_pep8_template = string.Template('''#!/bin/bash
# check pep8 formatting for all files

PEP8_CMD_TO_RUN='python3 -m autopep8 -i $package_name *.py'

DETECTED_CHANGES=$$(python3 -m autopep8 -d $package_name *.py)
if [[ -n "$$DETECTED_CHANGES" ]]
  then
  echo -e "\npep8 non conforming changes detected, please run :\n"
  echo -e "\t$$PEP8_CMD_TO_RUN\n"
  echo -e "& stage your changes before pushing"
  exit 1
fi

exit 0
''')


setup_template = string.Template('''
from setuptools import setup, find_packages
import re
from os.path import dirname, isdir, join, exists
from subprocess import CalledProcessError, check_output

tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b')
version_re = re.compile('^Version: (.+)$$', re.M)


def readme():
    with open('README.md') as f:
        return f.read()

def version_from_git_describe(version):
    if version[0]=='v':
            version = version[1:]

    # PEP 440 compatibility
    number_commits_ahead = 0
    if '-' in version:
        version, number_commits_ahead, commit_hash = version.split('-')
        number_commits_ahead = int(number_commits_ahead)

    # print('number_commits_ahead', number_commits_ahead)

    split_versions = version.split('.')
    if 'post' in split_versions[-1]:
        suffix = split_versions[-1]
        split_versions = split_versions[:-1]
    else:
        suffix = None

    for pre_release_segment in ['a', 'b', 'rc']:
        if pre_release_segment in split_versions[-1]:
            if number_commits_ahead > 0:
                split_versions[-1] = str(split_versions[-1].split(pre_release_segment)[0])
                if len(split_versions) == 2:
                    split_versions.append('0')
                if len(split_versions) == 1:
                    split_versions.extend(['0', '0'])

                split_versions[-1] = str(int(split_versions[-1])+1)
                future_version = '.'.join(split_versions)
                return '{}.dev{}'.format(future_version, number_commits_ahead)
            else:
                return '.'.join(split_versions)

    if number_commits_ahead > 0:
        if len(split_versions) == 2:
            split_versions.append('0')
        if len(split_versions) == 1:
            split_versions.extend(['0', '0'])
        split_versions[-1] = str(int(split_versions[-1])+1)
        split_versions = '.'.join(split_versions)
        return '{}.dev{}'.format(split_versions, number_commits_ahead)
    else:
        if suffix is not None:
            split_versions.append(suffix)

        return '.'.join(split_versions)

# Just testing if get_version works well
assert version_from_git_describe('v0.1.7.post2') == '0.1.7.post2'
assert version_from_git_describe('v0.0.1-25-gaf0bf53') == '0.0.2.dev25'
assert version_from_git_describe('v0.1-15-zsdgaz') == '0.1.1.dev15'
assert version_from_git_describe('v1') == '1'
assert version_from_git_describe('v1-3-aqsfjbo') == '1.0.1.dev3'

def get_version():
    # Return the version if it has been injected into the file by git-archive
    version = tag_re.search('$$Format:%D$$')
    if version:
        return version.group(1)

    d = dirname(__file__)
    pkg_info_path = join(d, 'PKG-INFO')

    if isdir(join(d, '.git')):
        cmd = 'git describe --tags'
        try:
            version = check_output(cmd.split()).decode().strip()[:]

        except CalledProcessError:
            raise RuntimeError('Unable to get version number from git tags: create a first v0.0.1 version to start!')

        return version_from_git_describe(version)
    
    elif exists(pkg_info_path):
        # try to extract the version from the PKG-INFO file.
        with open(pkg_info_path, 'r') as f:
            version = version_re.search(f.read()).group(1)
    else:
        print('No version found from git tags nor from PKGINFO. defaulting to 0.0.1') 
        version='0.0.1'

    return version

setup(version='$version',
      name='$package_name',
      description='$short_description',
      long_description=readme(),
      long_description_content_type='text/markdown',
      author='$author_name',
      author_email='$author_mail',
      install_requires=$requirements,
      python_requires='$python_version',
      packages=find_packages()
)

''')
