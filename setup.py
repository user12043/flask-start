#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by me60338 on 11/28/21 - 9:17 AM
# part of project flask-start

from setuptools import setup, find_packages

setup(
    name="app",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask"
    ]
)
