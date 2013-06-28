# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

VERSION = '1.0.0'
AUTHORS = u'Alejandro Galindo García, Roberto Abdelkader Martínez Pérez'
EMAILS = 'galindo.garcia.alejandro@gmail.com, robertomartinezp@gmail.com'

setup(name='cpe',
      version=VERSION,
      summary="""\
              Implementation of Common Platform Enumeration (CPE)
              specification""",
      description="""\
              Package to create and operate with CPE names of 1.1, 2.2 and 2.3
              versions of CPE (Common Platform Enumeration) specification""",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7"],
      keywords='cpe identification naming matching standard specification mitre nist',
      author=AUTHORS,
      author_email=EMAILS,
      maintainer=AUTHORS,
      maintainer_email=EMAILS,
      license='GPLv3',
      url="https://github.com/galindale/cpe",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      )
