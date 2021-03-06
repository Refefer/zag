#!/usr/bin/env python
import os

from setuptools import setup, find_packages
from distutils.core import setup

BASE = os.path.dirname(os.path.abspath(__file__))

#with open(os.path.join(BASE, "README.md")) as f:
#    long_description = f.read()

long_description = ""

setup(
    name='zag',
    version="0.0.1",
    description="Simple workflow manager",
    long_description=long_description,
    url="https://www.github.com/Refefer/zag",
    packages=find_packages(BASE),
    test_suite="tests",
    author='Andrew Stanton',
    author_email="refefer@gmail.com",
    scripts=[
        "bin/zag"
    ],
    classifiers=[
       "Development Status :: 3 - Alpha",
       "License :: OSI Approved :: Apache Software License",
       "Programming Language :: Python :: 2",
       "Programming Language :: Python :: 3",
       "Operating System :: OS Independent"
      ]
    )
