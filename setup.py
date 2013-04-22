from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='cpe',
      version=version,
      description="Contains classes for treatment of CPE identifiers",
      long_description="""\
This package validates CPE identifiers and platforms (set of CPE ids) and comparisons between them.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='CPE platform standard',
      author='Alejandro Galindo',
      author_email='alejandro.galindo.contractor@bbva.com',
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
