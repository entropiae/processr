#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='processr',
    version='0.1.0',
    description="Compose your dictionary-processing pipeline",
    long_description=readme + '\n\n' + history,
    author="Riccardo Cirimelli",
    author_email='rcirimelli@gmail.com',
    url='https://github.com/entropiae/processr',
    packages=[
        'processr',
    ],
    package_dir={'processr':
                 'processr'},
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords='processr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=['pytest'],
    setup_requires=['pytest-runner']
)
