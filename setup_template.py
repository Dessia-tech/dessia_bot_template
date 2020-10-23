from setuptools import setup
import re
from os.path import dirname, isdir, join

tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b')
version_re = re.compile('^Version: (.+)$', re.M)


def readme():
    with open('README.md') as f:
        return f.read()



