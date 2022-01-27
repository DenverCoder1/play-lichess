# /usr/bin/env python
import os
import re
from typing import List
from setuptools import setup
from setuptools.command.test import Command


class LintCommand(Command):
    """
    A copy of flake8's Flake8Command
    """

    description = "Run flake8 on modules registered in setuptools"
    user_options: List[str] = []

    def initialize_options(self):
        # must override
        pass

    def finalize_options(self):
        # must override
        pass

    def distribution_files(self):
        if self.distribution.packages:
            for package in self.distribution.packages:
                yield package.replace(".", os.path.sep)

        if self.distribution.py_modules:
            for filename in self.distribution.py_modules:
                yield "%s.py" % filename

    def run(self):
        from flake8.api.legacy import get_style_guide

        flake8_style = get_style_guide(config_file="setup.cfg")
        paths = self.distribution_files()
        report = flake8_style.check_files(paths)
        raise SystemExit(report.total_errors > 0)


version = ""
with open(os.path.join("play_lichess", "__init__.py")) as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()

requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()

setup(
    name="play-lichess",
    version=version,
    author="Jonah Lawrence",
    author_email="jonah@freshidea.com",
    description="Module for creating match links on Lichess that players can join",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DenverCoder1/play-lichess",
    project_urls={
        "Bug Tracker": "https://github.com/DenverCoder1/play-lichess/issues",
    },
    packages=["play_lichess"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[requirements],
    cmdclass={
        "lint": LintCommand,
    },
)
