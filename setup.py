#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import os

EMAILS = "{0}, {1}".format(
    'galindo.garcia.alejandro@gmail.com',
    'robertomartinezp@gmail.com')
KEYWORDS = u'cpe identification naming matching standard specification mitre nist'
MAINTAINER = u'Roberto Abdelkader Martínez Pérez'
MAINTAINER_EMAIL = u'robertomartinezp@gmail.com'
LICENSE = u'LGPLv3'
PACKAGE_URL = "https://github.com/nilp0inter/cpe"

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()
news = open(os.path.join(here, 'NEWS.txt')).read()

PACKAGE_STR = 'cpe'
version = __import__(PACKAGE_STR).get_version()
package_name = __import__(PACKAGE_STR).PACKAGE_NAME
description = __import__(PACKAGE_STR).DESCRIPTION
authors = __import__(PACKAGE_STR).AUTHORS

long_description = readme

packages = [
    'cpe',
    'cpe.comp',
]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7"
]

setup(
    name=package_name,
    version=version,
    description=description,
    long_description=long_description,
    classifiers=classifiers,
    keywords=KEYWORDS,
    author=authors,
    author_email=EMAILS,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    url=PACKAGE_URL,
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
