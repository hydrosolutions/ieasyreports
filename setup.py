#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Babel==2.12.1', 'Click>=7.0', 'openpyxl==3.1.2', 'pydantic==2.1.1', 'pydantic-settings==2.0.2']

test_requirements = ['pytest>=3', ]

setup(
    author="Davor Škalec",
    author_email='davor.skalec@encode.hr',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="Reports template system for generating reports from templates.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ieasyreports',
    name='ieasyreports',
    packages=find_packages(include=['ieasyreports', 'ieasyreports.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hydrosolutions/ieasyreports',
    version='0.1.0',
    zip_safe=False,
)
