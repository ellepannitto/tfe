#!/usr/bin/env python3
"""thematic-fit-estimation setup.py.

This file details modalities for packaging the thematic-fit-estimation package.
"""

from setuptools import setup

with open('README.md', 'r',) as fh:
    long_description = fh.read()

setup(
    name='thematic-fit-estimation',
    description='Estimation of thematic fit performances',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
    license='MIT',
    platforms=['any'],
    packages=['tfe', 'tfe.logging', 'tfe.exceptions',
              'tfe.utils', 'tfe.core'],
    package_data={'tfe': ['logging/*.yml']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tfe = tfe.main:main'
        ],
    },
    install_requires=['pyyaml>=4.2b1','numpy','scipy>=0.19'],
    zip_safe=False,
)
