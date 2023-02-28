# /usr/bin/env python
import os
import re
from setuptools import setup

version = ""
with open(os.path.join("play_lichess", "__init__.py"), "r", encoding="utf-8") as f:
    version_match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    )
    version = version_match.group(1) if version_match else ""

if not version:
    raise RuntimeError("version is not set")

long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as f:
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
    package_data={"play_lichess": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[requirements],
)
