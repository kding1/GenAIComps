# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import re
import subprocess
from io import open

from setuptools import find_packages, setup


def fetch_requirements(path):
    with open(path, "r") as fd:
        return [r.strip() for r in fd.readlines()]


def is_commit_on_tag():
    try:
        result = subprocess.run(
            ["git", "describe", "--exact-match", "--tags"], capture_output=True, text=True, check=True
        )
        tag_name = result.stdout.strip()
        return tag_name
    except subprocess.CalledProcessError:
        return False


def get_build_version():
    if is_commit_on_tag():
        return __version__
    try:
        result = subprocess.run(["git", "describe", "--tags"], capture_output=True, text=True, check=True)
        _, distance, commit = result.stdout.strip().split("-")
        return f"{__version__}.dev{distance}+{commit}"
    except subprocess.CalledProcessError:
        return __version__


try:
    filepath = "./comps/version.py"
    with open(filepath) as version_file:
        (__version__,) = re.findall('__version__ = "(.*)"', version_file.read())
except Exception as error:
    assert False, "Error: Could not open '%s' due %s\n" % (filepath, error)


if __name__ == "__main__":

    setup(
        name="opea-comps",
        author="Intel DCAI Software",
        version=get_build_version(),
        author_email="liang1.lv@intel.com, haihao.shen@intel.com, suyue.chen@intel.com",
        description="Generative AI components",
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        keywords="GenAI",
        license="Apache 2.0",
        url="https://github.com/opea-project/GenAIComps",
        packages=find_packages(
            include=[
                "comps.cores",
                "comps.cores.*",
            ],
        ),
        package_data={"": ["*.yaml", "../*.py"]},
        include_package_data=True,
        install_requires=fetch_requirements("requirements.txt"),
        python_requires=">=3.8.0",
        classifiers=[
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "License :: OSI Approved :: Apache Software License",
        ],
    )
