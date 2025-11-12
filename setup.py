#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

requirements = [
    "Click>=8.0.1,<9.0.0",
]

setup(
    author="Sergey Chudakov",
    author_email="csredrat@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    description="Linux bash aliases generator",
    entry_points={
        "console_scripts": [
            "topalias=topalias.cli:cli",
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="top bash zsh alias aliases linux python shell cli console terminal utility tool history sysadmin",
    name="topalias",
    packages=find_packages(include=["topalias", "topalias.*"]),
    url="https://github.com/CSRedRat/topalias",
    version="4.0.0",
    zip_safe=False,
)
