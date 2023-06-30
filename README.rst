.. image:: http://cpe.mitre.org/images/cpe_logo.gif
   :alt: CPE Logo

Common Platform Enumeration for Python
--------------------------------------

*CPE* (this code) is a LGPL licensed Python package, implementing the
CPE standards.


About the CPE standard
----------------------

Common Platform Enumeration (CPE) is a standardized method of describing
and identifying classes of applications, operating systems, and hardware
devices present among an enterprise's computing assets.

For more information, please visit the official website of CPE,
developed by `MITRE`_ and maintained by `NIST`_.


Features
--------

- CPE rich comparison.
- CPE cross-version conversion.
- CPE Language parsing and evaluation.
- LGPL Licensed.
- Semantic versioning.
- Tests.


Installation |Version| |TravisCI_master|
----------------------------------------

To install `CPE` execute:

.. code-block:: bash

    $ pip install cpe

The latest stable version is always in `PyPI`_.


Documentation
-------------

Documentation is available at `ReadTheDocs`_.


Compatibility
-------------

- Python: 2.7, 3.4
- CPE: 1.1, 2.2, 2.3
- CPE Formats: WFN, URI, FS.


Contribute |Coverage| |TravisCI_develop| |Waffle.IO_ready|
----------------------------------------------------------

Follow the steps on the `how to contribute`_ document.

.. _PyPI: https://pypi.python.org/pypi/cpe/
.. _MITRE: http://cpe.mitre.org/
.. _NIST: http://nvd.nist.gov/cpe.cfm
.. _ReadTheDocs: https://cpe.readthedocs.org/en/latest/
.. _GitHub: https://github.com/nilp0inter/cpe
.. _How to contribute: https://github.com/nilp0inter/cpe/blob/develop/CONTRIBUTING.md


.. |TravisCI_master| image:: https://travis-ci.org/nilp0inter/cpe.svg?branch=master
   :target: https://travis-ci.org/nilp0inter/cpe
   :alt: Build Status (master)
   

.. |TravisCI_develop| image:: https://travis-ci.org/nilp0inter/cpe.svg?branch=develop
   :target: https://travis-ci.org/nilp0inter/cpe
   :alt: Build Status (develop)

.. |Waffle.IO_ready| image:: https://badge.waffle.io/nilp0inter/cpe.png?label=ready&title=Ready
   :target: https://waffle.io/nilp0inter/cpe
   :alt: Stories in Ready

.. |Coverage| image:: https://coveralls.io/repos/nilp0inter/cpe/badge.png?branch=develop
   :target: https://coveralls.io/r/nilp0inter/cpe?branch=develop
   :alt: Coverage Status
   
.. |Downloads| image:: https://pypip.in/d/cpe/badge.png
   :target: https://crate.io/packages/cpe
   :alt: Downloads

.. |Version| image:: https://camo.githubusercontent.com/8369bedde5c3455e907e9ddf9b06751af7cbbc28/68747470733a2f2f62616467652e667572792e696f2f70792f6370652e706e67
   :target: http://badge.fury.io/py/cpe
   :alt: Version
