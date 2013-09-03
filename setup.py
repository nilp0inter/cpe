# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = '1.0.4'
AUTHORS = u'Alejandro Galindo García, Roberto Abdelkader Martínez Pérez'
EMAILS = 'galindo.garcia.alejandro@gmail.com, robertomartinezp@gmail.com'

setup(name='cpe',
      version=VERSION,
      description='Implementation of versions 1.1, 2.2 and 2.3 of CPE specification.',
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
      maintainer=u'Alejandro Galindo García',
      maintainer_email='galindo.garcia.alejandro@gmail.com',
      license='GPLv3',
      url="https://github.com/galindale/cpe",
      packages=['cpe'],
      long_description=open("README.md").read(),
      include_package_data=True,
      zip_safe=False,
      )
