#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import json

MIN_FILE_COVERAGE = 50.
MIN_MODULE_COVERAGE = 50.

untracked_modules = [
]

print("untracked modules:", untracked_modules)

with open("coverage.json", "r") as file:
    d = json.load(file)

print('total covered', d['totals']['percent_covered'], '%')
if d['totals']['percent_covered'] < MIN_MODULE_COVERAGE:
    raise RuntimeError('Package is not covered enough by tests: {}% expected minimum {}%'.format(
        d['totals']['percent_covered'], MIN_MODULE_COVERAGE))

print('[Coverage] You can increase MIN_MODULE_COVERAGE to maximum {}% (actual {}%)'.format(
    d['totals']['percent_covered'], MIN_MODULE_COVERAGE))

min_actual_coverage = 100
for file_name, data in d['files'].items():
    print(file_name, data['summary']['percent_covered'], '%')
    # print('/'.join(file_name.split('/')[-2:]))
    if '/'.join(file_name.split('/')[-2:]) in untracked_modules:
        print(file_name, '-> in untrack list')
    else:
        # print('Testing if {} is above {}'.format(file_name, MIN_FILE_COVERAGE))
        if data['summary']['percent_covered'] < MIN_FILE_COVERAGE:
            raise RuntimeError('Module {} is not covered enough by tests: {}% expected minimum {}%'.format(
                file_name, data['summary']['percent_covered'], MIN_FILE_COVERAGE))
        min_actual_coverage = min(
            min_actual_coverage, data['summary']['percent_covered'])

print('[Coverage] You can increase MIN_FILE_COVERAGE to maximum {}% (actual:{})%'.format(
    min_actual_coverage, MIN_FILE_COVERAGE))
