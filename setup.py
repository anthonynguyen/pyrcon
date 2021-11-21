#!/usr/bin/env python
from distutils.core import setup

setup(
    name="pyrcon",
    version="1.0.0",
    author="Anthony Nguyen",
    author_email="anknguyen@gmail.com",
    packages=["pyrcon"],
    url="https://github.com/clearskies/pyrcon",
    license="MIT",
    description="A stupidly simple RCON library (for UDP servers)",
    long_description=open("README.rst").read(),
    python_requires=">=3.7",
)
