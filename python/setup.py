#!/usr/bin/env python
# encoding: utf-8
"""
Python module setup file
"""

from setuptools import find_packages, setup

version = '0.1.0'

base = None

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='hedge',
    version=version,
    author='Kevin S Kirkup',
    author_email='kevin.kirkup@gmail.com',
    url='http://teaRoomStdio.com',
    license='LICENSE.txt',
    description='Finance Tools and scripts',
    long_description=open('README.txt').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    scripts=[
        'bin/snp500_download.py',
        'bin/key_financial.py',
        'bin/refresh_snp500.py',
        'bin/stock_data.py',
    ],
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=requirements,
    entry_points="""
    # -*- Entry points: -*-
    """,
)
