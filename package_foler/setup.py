import re
from os.path import dirname, isdir, join
from subprocess import CalledProcessError, check_output

from setuptools import find_packages, setup

tag_re = re.compile(r"\btag: %s([0-9][^,]*)\b")
version_re = re.compile("^Version: (.+)$", re.M)


def readme():
    with open("README.md") as f:
        return f.read()


def version_from_git_describe(version):
    if version[0] == "v":
        version = version[1:]

    # PEP 440 compatibility
    number_commits_ahead = 0
    if "-" in version:
        version, number_commits_ahead, commit_hash = version.split("-")
        number_commits_ahead = int(number_commits_ahead)

    # print('number_commits_ahead', number_commits_ahead)

    split_versions = version.split(".")
    if "post" in split_versions[-1]:
        suffix = split_versions[-1]
        split_versions = split_versions[:-1]
    else:
        suffix = None

    for pre_release_segment in ["a", "b", "rc"]:
        if pre_release_segment in split_versions[-1]:
            if number_commits_ahead > 0:
                split_versions[-1] = str(split_versions[-1].split(pre_release_segment)[0])
                if len(split_versions) == 2:
                    split_versions.append("0")
                if len(split_versions) == 1:
                    split_versions.extend(["0", "0"])

                split_versions[-1] = str(int(split_versions[-1]) + 1)
                future_version = ".".join(split_versions)
                return "{}.dev{}".format(future_version, number_commits_ahead)
            else:
                return ".".join(split_versions)

    if number_commits_ahead > 0:
        if len(split_versions) == 2:
            split_versions.append("0")
        if len(split_versions) == 1:
            split_versions.extend(["0", "0"])
        split_versions[-1] = str(int(split_versions[-1]) + 1)
        split_versions = ".".join(split_versions)
        return "{}.dev{}+{}".format(split_versions, number_commits_ahead, commit_hash)
    else:
        if suffix is not None:
            split_versions.append(suffix)

        return ".".join(split_versions)


def get_version():
    # Return the version if it has been injected into the file by git-archive
    version = tag_re.search("$Format:%D$")
    if version:
        return version.group(1)

    d = dirname(__file__)

    if isdir(join(d, ".git")):
        cmd = "git describe --tags"
        try:
            version = check_output(cmd.split()).decode().strip()[:]

        except CalledProcessError:
            # raise RuntimeError("Unable to get version number from git tags")
            return "0.0.1"

        return version_from_git_describe(version)
    else:
        # Extract the version from the PKG-INFO file.
        with open(join(d, "PKG-INFO")) as f:
            version = version_re.search(f.read()).group(1)

    # print('version', version)
    return version

install_requires = ["{{REQUIRED_PACKAGES}}"][0].split(',')

setup(
    version=get_version(),
    name="{{PACKAGE_NAME}}",
    description="{{SHORT_DESCRIPTION}}",
    long_description=readme(),
    author="{{AUTHOR}}",
    author_email="{{CONTACT}}",
    install_requires=install_requires,
    python_requires="{{VERSION}}",
    packages=find_packages(),
)
