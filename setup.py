#!/usr/bin/env python3
import setuptools

name='photonics'

packages=[f'{name}.{package}'
        for package
        in setuptools.find_packages(where='src')]

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version="0.0.1",
    author="Mike Taverne",
    author_email="Mike.Taverne@bristol.ac.uk",
    description="Useful scripts for MEEP, MPB, Bristol FDTD, Nanoscribe, FIB and other photonics-related tools.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://mtav.github.io/script_inception_public",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={
        name: 'src',
    },
    python_requires='>=3.6',
    install_requires=[
        "numpy",
    ],
)
