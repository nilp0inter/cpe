#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='cpe',
      version=version,
      description="Contains classes for treatment of CPE names of 1.1, 2.2 and 2.3 versions of CPE (Common Platform Enumeration) specification",
      long_description="""\
This package implement the validation of both CPE names and platforms (set of
CPE names), and the comparisons between them.\
The versions of CPE implemented are: 1.1, 2.2 and 2.3.\
The functionality offered of each version is associated
with CPE naming, CPE name matching and CPE language matching""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='CPE naming matching language platform standard specification',
      author='Alejandro Galindo',
      author_email='alejandro.galindo@innovation4security.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
