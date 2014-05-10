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
```bash
    $ pip install -r requirements/develop.txt
```

Developer workflow
------------------

1 Create a topic branch from the develop branch.
```bash
    $ git checkout -b my_new_feature develop
```
* Run the test-suite and verify everything is fine:
```bash
    tox
```

2 Write your code and a test that the bug was fixed or that the feature works as expected.

3 Make sure to add yourself to AUTHORS. ;)

4 Run the tests again. 

5 Send a pull request and bug the maintainer until it gets merged and published.

