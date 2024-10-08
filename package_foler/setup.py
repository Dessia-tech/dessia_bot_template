import re
from os.path import dirname, isdir, join
from subprocess import CalledProcessError, check_output

from setuptools import find_packages, setup



def readme() -> str:
    """Read the README file."""
    with open("README.md", encoding="utf-8") as f:
        return f.read()


install_requires = ["{{REQUIRED_PACKAGES}}"][0].split(',')

setup(
    name="{{PACKAGE_NAME}}",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="{{SHORT_DESCRIPTION}}",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="{{AUTHOR}}",
    author_email="{{CONTACT}}",
    install_requires=install_requires,
    python_requires="{{VERSION}}",
    packages=find_packages(),
)
