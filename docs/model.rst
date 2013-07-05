Model
=====

This section shows the diagrams of model parts of cpe package. These diagrams have been generated with the PyNSource tool version 1.61 (`https://code.google.com/p/pynsource/ <https://code.google.com/p/pynsource/>`_). Each model class is stored in a different file. The model parts are as follows.

.. toctree::
    :maxdepth: 2

    model/cpehierarchy
    model/cpesethierarchy
    model/cpelanghierarchy
    model/cpecomphierarchy

Categories of main classes
--------------------------

The main classes of model can be grouped in four categories:

* Auto version (classes to create CPE Names without setting their version of CPE specification associated):

  * **cpe.py** (generic auto version class)
  * **cpe2\_3.py** (auto version class of version 2.3)

* Manual version (classes to create CPE Names of particular version of CPE specification):

  * **cpe1\_1.py** (version 1.1)
  * **cpe2\_2.py** (version 2.2)
  * **cpe2\_3\_wfn.py** (version 2.3 with WFN style)
  * **cpe2\_3\_uri,py** (version 2.3 with URI style)
  * **cpe2\_3\_fs.py** (version 2.3 with formatted style style)

* CPE Name matching (classes to realize the name matching of CPE specification):

  * **cpeset1\_1.py** (version 1.1)
  * **cpeset2\_2.py** (version 2.2)
  * **cpeset2\_3.py** (version 2.3)

* CPE Language matching (classes to realize the language matching of CPE specification):

  * **cpelang2\_2.py** (version 2.2)
  * **cpelang2\_3.py** (version 2.3)
