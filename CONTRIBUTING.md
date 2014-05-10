How to contribute
=================

Getting started
---------------

* Check for open issues or open a fresh issue to start a discussion around a feature, idea or a bug.
* Fork the repository on GitHub.
* Clone your fork on your computer.


Installing dependencies
-----------------------

* Run the following command to install the developer dendencies:

    pip install -r requirements/develop.txt


Developer workflow
------------------

* Create a topic branch from the develop branch.

    git checkout -b my_new_feature develop

* Run the test-suite and verify everything is fine:

    tox

* Write your code and a test that the bug was fixed or that the feature works as expected.
* Make sure to add yourself to AUTHORS. ;)
* Run the tests again. 
* Send a pull request and bug the maintainer until it gets merged and published.

