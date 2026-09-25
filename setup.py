#!/usr/bin/env python3
"""
Setup script for nature-office - Alberta's premium mobile office solution.

This setup script configures the nature-office package for distribution
and installation using pip.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
def read_readme():
    readme_path = Path(__file__).parent / "README.md"
    return readme_path.read_text(encoding="utf-8")

def read_requirements():
    req_path = Path(__file__).parent / "requirements.txt"
    return req_path.read_text(encoding="utf-8").splitlines()

setup(
    name="nature-office",
    version="0.1.0",
    description="Alberta's premium mobile office solution for AI professionals.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Alberta AI Mobile Office Team",
    author_email="contact@nature-office.com",
    url="https://github.com/nature-office/nature-office",
    packages=find_packages(),
    package_dir={
        "": "core",
        "nature_office": ".",
    },
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: AI",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    keywords="mobile office, ai, vehicle assessment, office-ready, certification",
    project_urls={
        "Documentation": "https://docs.nature-office.com",
        "Source": "https://github.com/nature-office/nature-office",
        "Tracker": "https://github.com/nature-office/nature-office/issues",
    },
    entry_points={
        "console_scripts": [
            "nature-assess=nature_office.core.agy_bridge:assess_vehicle",
            "nature-cli=nature_office.core.agy_bridge:main",
            "vehicle-assess=nature_office.core.agy_bridge:assess_vehicle",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)