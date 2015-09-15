#!/usr/bin/env python
# encoding: utf-8

# Third Party Libs
from setuptools import setup


# Generate a Long Decription for the PyPi page which is the README.rst
# Plus the CHANGELOG.rst
long_description = open('./README.rst').read()
changelog = open('./CHANGELOG.rst').read()
long_description += '\n' + changelog

# Get Version
version = open('./VERSION.txt').read().strip()


setup(
    name='djangohmac',
    url='https://github.com/thisissoon/django-hmac',
    version=version,
    author='SOON_',
    author_email='dorks@thisissoon.com',
    description='Provides easy integration of the HMAC signatures for '
                'your REST Django Applications.',
    long_description=long_description,
    packages=[
        'djangohmac',
    ],
    install_requires=[
        'django',
        'six>=1.9.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: Public Domain'
    ],
    license='Public Domain',
    keywords=['Django', 'HMAC', 'REST', 'Views', 'middleware'],
    test_suite='tests',
)
