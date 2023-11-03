#!/usr/bin/env python
# pylint: disable=missing-docstring
import os
from setuptools import setup, find_packages


def get_version():
    """Get version from __init__.py file."""
    filename = os.path.join(
        os.path.dirname(__file__), "src", "sh_copilot", "__init__.py"
    )
    with open(filename, encoding="UTF-8") as file:
        for line in file:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])  # pylint: disable=eval-used

    raise ValueError(f"No __version__ defined in {filename}")


setup(
    name="sh-copilot",
    version=get_version(),
    description="Copilot for shell",
    long_description=open(  # pylint: disable=consider-using-with
        "README.md", encoding="UTF-8"
    ).read(),
    long_description_content_type="text/markdown",
    author="Guillaume MARTINEZ",
    author_email="lunik@tiwabbit.fr",
    maintainer="Guillaume MARTINEZ",
    maintainer_email="lunik@tiwabbit.fr",
    url="https://github.com/Lunik/sh-copilot",
    download_url="https://pypi.org/project/sh-copilot/",
    license_files=("LICENSE",),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    entry_points={
        "console_scripts": ["sc = sh_copilot:main", "sh_copilot = sh_copilot:main"],
    },
    python_requires=">=3.11.0",
    install_requires=[
        "pydantic==2.*",
        "pyyaml==6.*",
    ],
    extras_require={
        "dev": [
            "pylint",
            "black",
            "twine",
            "build",
            "pytest",
            "pytest-cov",
            "pytest-html",
            "pytest-xdist",
            "pytest-helpers-namespace",
            "pytest-order",
            "wheel",
        ],
        "openai": [
            "openai==0.*",
        ],
        "azure": [
            "azure-identity==1.*",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
