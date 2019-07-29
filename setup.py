import os
from setuptools import setup, find_packages

NAME = "gz_matcher"
VERSION = os.environ.get("GZ_MATCHER_VERSION", "0.0.1")

with open("README.rst", "r") as fh:
    readme = fh.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    name=NAME,
    version=VERSION,
    keywords='gz-matcher',
    url='https://github.com/tilaboy/gazetteer-matcher',
    description="Python tool to match phrases listed in the gazetteer",
    author="Chao Li",
    author_email="chaoli.job@gmail.com",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/rst",
    test_suite="tests",
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    packages=[
        "gz_matcher",
        "gz_matcher.match_patterns"
    ],
    options={
        "build_scripts": {
            "executable": "/usr/bin/env python",
        },
    },
    license="MIT license",
    zip_safe=False
)
