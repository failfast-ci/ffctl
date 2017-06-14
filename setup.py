#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requirements = [
    'futures',
    'pyyaml',
    'jinja2>=2.8',
    'jsonnet>=0.9.0',
]


test_requirements = [
    "flake8",
    "pytest",
    "pytest-cov",
    "yapf"
]

setup(
    name='ffctl',
    version='0.1.2',
    description="ffctl cli",
    long_description="ffctl py-cli",
    author="Antoine Legrand",
    author_email='2t.antoine@gmail.com',
    url='https://github.com/ant31/ffctl',
    packages=[
        'ffctl',
        'ffctl.commands',
    ],
    scripts=[
        'bin/ffctl'
    ],
    package_dir={'ffctl':
                 'ffctl'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License version 2",
    zip_safe=False,
    keywords=['ffctl', 'ffctlpy', 'kubernetes'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,

)
