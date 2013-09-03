Important issues
================

* The **auto version classes** receive an CPE Name and try to find out what version is associated.
* The **functions to get the values of attributes of a CPE Name** always return a list of string. That is so because the attributes of version 1.1 of CPE specification can be linked with several system and elements. For example, the attribute *vendor* in CPE Name *cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0* get three values: *sun*, *bea* and *mysql*.
* The **not logical values of the attributes in version 2.3** of CPE specification always start and end with double quotes. For example, the value of attribute *product* in CPE Name *wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8", update="beta"]* is *"internet\_explorer"*, not *internet\_explorer* without double quotes.
* Some **CPE Names of version 1.1 with several systems or elements defined** cannot convert into other CPE versions, for example, the CPE Name *cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0*
* **Comparing a CPE Name of version 1.1 with others**, if versions are incompatible, then the return value is *False* instead of raising an exception. 
* The methods :func:`ovalcheck` and :func:`ocilcheck` of :class:`CPELanguage2_3` class is **not implemented**.
* The language attribute of CPE Names only allow the normal language tags according to the shortest ISO 639 code in language part and the ISO 3166-1 and UN M.49 code in region part. The extended, registered or reserved subtags are not supported.
