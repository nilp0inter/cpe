#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

version = '0.1'

setup(name='cpe',
      version=version,
      summary="""\
              Implementation of Common Platform Enumeration (CPE)
              specification""",
      description="""\
              Package to create and operate with CPE names of 1.1, 2.2 and 2.3
              versions of CPE (Common Platform Enumeration) specification""",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Information Technology",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7"],
      keywords='cpe identification naming matching standard specification',
      author='Alejandro Galindo',
      author_email='galindo.garcia.alejandro@gmail.com',
      maintainer='Alejandro Galindo',
      maintainer_email='galindo.garcia.alejandro@gmail.com',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      )
