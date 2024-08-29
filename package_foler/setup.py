"""
Setup script for the package.
"""

import re

from setuptools import find_packages, setup

tag_re = re.compile(r"\btag: %s([0-9][^,]*)\b")
version_re = re.compile("^Version: (.+)$", re.M)


def readme():
    with open("README.md") as f:
        return f.read()


install_requires = ["{{REQUIRED_PACKAGES}}"][0].split(",")

setup(
    name="{{PACKAGE_NAME}}",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="{{SHORT_DESCRIPTION}}",
    long_description=readme(),
    author="{{AUTHOR}}",
    author_email="{{CONTACT}}",
    install_requires=install_requires,
    python_requires="{{VERSION}}",
    packages=find_packages(),
)
