# coding: utf-8

from setuptools import setup, find_packages

NAME = "ts-task-script-utils"
VERSION = "1.0.1"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "numpy>=1.20.1",
    "arrow>=1.0.2",
    "dateparser>=1.0.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Python utility functions for Tetra Task Scripts",
    author="tetrascience",
    author_email="developers@tetrascience.com",
    url="https://github.com/tetrascience/ts-task-script-utils",
    project_urls={
        "Tetra Developer Site": "https://developers.tetrascience.com",
    },
    keywords=[],
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
