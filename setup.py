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
    name='fflinter',
    version='0.1.0',
    description="fflinter cli",
    long_description="fflinter py-cli",
    author="Antoine Legrand",
    author_email='2t.antoine@gmail.com',
    url='https://github.com/ant31/fflinter',
    packages=[
        'fflinter',
        'fflinter.commands',
    ],
    scripts=[
        'bin/fflinter'
    ],
    package_dir={'fflinter':
                 'fflinter'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License version 2",
    zip_safe=False,
    keywords=['fflinter', 'fflinterpy', 'kubernetes'],
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
