#!/usr/bin/env python3
"""thematic-fit-estimation setup.py.

This file details modalities for packaging the thematic-fit-estimation package.
"""

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='thematic-fit-estimation',
    description='Estimation of thematic fit performances',
    author='Ludovica Pannitto',
    author_email='ludovica.pannitto@unitn.it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
#    url='https://github.com/akb89/entropix',
#    download_url='https://github.com/akb89/entropix',
    license='MIT',
#    keywords=['entropy', 'distributional semantics'],
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
    install_requires=['pyyaml>=4.2b1'],
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Software Development :: Libraries :: Python Modules'],
    zip_safe=False,
)
