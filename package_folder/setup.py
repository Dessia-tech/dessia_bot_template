"""Minimal setup file for platform < 3.1 compatibility."""

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from setuptools import setup

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

project = pyproject.get("project", {})

setup(
    name=project.get("name"),
    description=project.get("description"),
)
