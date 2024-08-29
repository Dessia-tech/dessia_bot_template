"""
This file is used to configure the package and its dependencies.
"""

import re

from setuptools import find_packages, setup

tag_re = re.compile(r"\btag: %s([0-9][^,]*)\b")
version_re = re.compile("^Version: (.+)$", re.M)


def readme():
    """Get the README content."""
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="dessia_bot_template",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="This repository provides a template for creating new Python packages.",
    long_description=readme(),
    author="Dessia-Operations-Team",
    author_email="support@dessia.io",
    install_requires=[],
    python_requires=">=3.9",
    packages=find_packages(),
)
