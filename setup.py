#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Read version from version.py (currently "1.0.1")
version_file = os.path.join(os.path.dirname(__file__), 'src', 'enzywizard_conservation', 'version.py')
with open(version_file) as f:
    exec(f.read())          # defines __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enzywizard-conservation",
    version=__version__,                                    # e.g. "0.1.0"
    author="bioinfbrad",
    description=(
        "Calculate residue sequence conservation from a cleaned protein sequence "
        "and a user-provided multiple sequence alignment (MSA)."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bioinfbrad/enzywizard-conservation",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "biopython>=1.86",
        "numpy>=1.23.5",
        "packaging",
        # Note: hmmer is a system dependency (not a Python package). 
        # For Conda builds it must be listed in meta.yaml run requirements.
    ],
    entry_points={
        "console_scripts": [
            "enzywizard-conservation = enzywizard_conservation.cli:main",
        ],
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
