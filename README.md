[![Build Status](https://travis-ci.org/galindale/cpe.png)](https://travis-ci.org/galindale/cpe)
[![PyPI version](https://badge.fury.io/py/cpe.png)](http://badge.fury.io/py/cpe)
[![Downloads](https://pypip.in/d/cpe/badge.png)](https://crate.io/packages/cpe)

CPE PACKAGE
===========

This file intended to be a small tutorial about cpe package. It contains a brief introduction about Common Platform Enumeration (CPE) specification, the CPE version list implemented, the installation options and usage examples about cpe package, and several important issues to consider associated with the functionality of this package.

<h2 id="index">Index</h2>

1. [Introduction](#1-introduction)
2. [List of implemented CPE versions](#2-list-of-implemented-cpe-versions)
3. [Installation](#3-installation)
4. [Usage examples](#4-usage-examples)  
	4.1. [Naming](#41-naming)  
	4.2. [Name matching](#42-name-matching)  
	4.3. [Language matching](#43-language-matching)  
5. [Documentation](#5-documentation)
6. [Important issues](#6-important-issues)
7. [Bugtracker](#7-bugtracker)
8. [TODO](#8-todo)
9. [Authors](#9-authors)
10. [License](#10-license)
11. [References](#11-references)

<h2 id="1-introduction">1. Introduction</h2>

Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, operating systems, and hardware devices present among an enterprise's computing assets [[1]][cpe].

CPE provides [[2]][about_cpe]:

* A standard machine-readable format for encoding names of IT products and platforms (naming).
* A set of procedures for comparing names (name matching).
* A language for constructing "applicability statements" that combine CPE Names with simple logical operators (language matching).
* A standard notion of a CPE Dictionary.

For more information, please visit the official website of CPE, maintained by MITRE: [http://cpe.mitre.org/](http://cpe.mitre.org/)

![CPE specification logo](http://cpe.mitre.org/images/cpe_logo.gif)

[--- Return to index ---](#index)

<h2 id="2-list-of-implemented-cpe-versions">2. List of implemented CPE versions</h2>

This package implements the validation of both CPE Names and platforms (set of CPE Names), and the comparisons between them, corresponding to some versions of CPE specification [[3]][cpe_archive].

The functionality implemented in this package, associated with versions 1.1, 2.2 and 2.3 of CPE specification, is below:

* Version 1.1 [[4]][cpe11]:
 * CPE naming
 * CPE Name matching
* Version 2.2 [[5]][cpe22]:
 * CPE naming
 * CPE Name matching
 * CPE Language matching
* Version 2.3:
 * CPE naming [[6]][cpe23_naming]
 * CPE Name matching [[7]][cpe23_matching]
 * CPE Applicability Language matching [[8]][cpe23_language]

The CPE naming of version 2.3 supports the definition of three different styles of CPE Name:

* WFN: Well-Formed Name
* URI: Uniform Resource Identifier
* FS: Formatted String

[--- Return to index ---](#index)

<h2 id="3-installation">3. Installation</h2>
Install the package using pip:

	pip install cpe

or download it and execute the setup.py file:

	python setup.py install

[--- Return to index ---](#index)

<h2 id="4-usage-examples">4. Usage examples</h2>

This section explains with several examples how to use this package to create both CPE Names and platforms in a particular version of CPE specification.

[--- Return to index ---](#index)

<h3 id="41-naming">4.1. Naming</h3>

To create a new CPE Name, the cpe package provides a generating class of CPE objects called CPE. It implements the factory pattern and receive two parameters: version of CPE specification and URI associated with CPE Name. Also, it is possible create a instance of a particular version of CPE Name directly using the class associated with the version.

In the following example, a CPE Name of version 2.3 of CPE specification is created:

* Imports the class

		>>> from cpe import CPE

* Creates a CPE Name of version 2.3 (URI style) with an application system where the value of edition component is packed:

		>>> str23_uri = 'cpe:/a:hp:insight_diagnostics:8::~~online~win2003~x64~'
		>>> c23_uri = CPE(str23_uri)

The cpe package provides methods to get the value of components of a CPE Name (these functions always return a string list) and identify the type of system associated with it (hardware, operating system or application):

	>>> c23_uri.get_target_hardware()	# Simple Target_hw attribute (v2.3, URI style)
	['x64']
	>>> c23_uri.is_hardware()			# Type of system (v2.3, URI style)
	False

Finally, the cpe package contains methods to convert any CPE Name defined under a particular style (URI version 2.3, WFN or formatted string) in other different styles:

	>>> c23_uri.as_wfn()
        'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="8", update=ANY, edition=ANY, sw_edition="online", target_sw="win2003", target_hw="x64", other=ANY]'
	>>> c23_uri.as_uri_2_3()
        'cpe:/a:hp:insight_diagnostics:8::~~online~win2003~x64~'
	>>> c23_uri.as_fs()
        'cpe:2.3:a:hp:insight_diagnostics:8:*:*:*:online:win2003:x64:*'

[--- Return to index ---](#index)

<h3 id="42-name-matching">4.2. Name matching</h3>

To create a set of CPE Name the package cpe provides the CPESetX\_Y class, where X\_Y is the target version of CPE specification. The *name_match* function of set allows do the name matching of CPE specification.

In the following example, a set of CPE Names of version 2.2 is created and the name matching is realized:

* Imports the classes of version:

		>>> from cpe.cpe2_2 import CPE2_2
		>>> from cpe.cpeset2_2 import CPESet2_2

* Creates the CPE Names of target system:

		>>> c1 = CPE2_2('cpe:/o:microsoft:windows_2000::sp3:pro')
		>>> c2 = CPE2_2('cpe:/a:microsoft:ie:5.5')

* Creates a set that contains the above CPE Names (known instances): K = {"cpe:/o:microsoft:windows\_2000::sp3:pro", "cpe:/a:microsoft:ie:5.5"}

		>>> K = CPESet2_2()
		>>> K.append(c1)
		>>> K.append(c2)

* Create the candidate CPE Name. It represents a rule in a security guidance checklist describes some settings to check on a system running Microsoft Windows 2000: X = "cpe:/o:microsoft:windows\_2000"
 
		>>> X = CPE2_2('cpe:/o:microsoft:windows_2000')

* Does the name matching:

		>>> K.name_match(X)
		True

There are three components in X: C1=o, C2=microsoft, C3=windows\_2000. Each component matches the corresponding component of the first CPE Name in K. So, the algorithm returns true and the rule can be applied to the target system.

[--- Return to index ---](#index)

<h3 id="43-language-matching">4.3. Language matching</h3>

To create an expression of CPE Language the cpe package provides the CPELanguageX\_Y class, where X\_Y is the version of CPE specification used. The *language_match* function of class allows do the language matching of CPE specification.

In the following example, an expression of CPE Language of version 2.2 is created and the language matching is realized:

* Imports the classes of version:

		>>> from cpe import CPE
		>>> from cpe.cpeset2_2 import CPESet2_2
		>>> from cpe.cpelang2_2 import CPELanguage2_2

* Creates the CPE Names of target system:

		>>> c1 = CPE('cpe:/o:sun:solaris:5.9:::en-us', CPE.VERSION_2_2)
		>>> c2 = CPE('cpe:/a:bea:weblogic:8.1', CPE.VERSION_2_2)

* Creates a set that contains the above CPE Names (known instances): K = {"cpe:/o:sun:sunos:5.9:::en-us", "cpe:/a:bea:weblogic:8.1"}

		>>> K = CPESet2_2()
		>>> K.append(c1)
		>>> K.append(c2)

* Creates the expression in XML of candidate CPE Language statement:  

		>>> It is necessary specify the "cpe:platform-specification" tag

		>>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform id="123"><cpe:title>Sun Solaris 5.8 or 5.9 with BEA Weblogic 8.1 installed</cpe:title><cpe:logical-test operator="AND" negate="FALSE"><cpe:logical-test operator="OR" negate="FALSE"><cpe:fact-ref name="cpe:/o:sun:solaris:5.8" /><cpe:fact-ref name="cpe:/o:sun:solaris:5.9" /></cpe:logical-test><cpe:fact-ref name="cpe:/a:bea:weblogic:8.1" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

* Does the language matching:

		>>> X = CPELanguage2_2(document)
		>>> X.language_match(K)
		True

[--- Return to index ---](#index)

<h2 id="5-documentation">5. Documentation</h2>

To get more information about cpe package and its implementation details you can visit the following links:

* GitHub: [https://github.com/galindale/cpe](https://github.com/galindale/cpe "GitHub")
* PyPi: [https://pypi.python.org/pypi/cpe/](https://pypi.python.org/pypi/cpe/ "PyPI")
* Read the Docs: [https://cpe.readthedocs.org/en/latest/](https://cpe.readthedocs.org/en/latest/ "Read the Docs")

[--- Return to index ---](#index)

<h2 id="6-important-issues">6. Important issues</h2>

* The **auto version classes** receive an CPE Name and try to find out what version is associated.
* The **functions to get the values of attributes of a CPE Name** always return a list of string. That is so because the attributes of version 1.1 of CPE specification can be linked with several system and elements. For example, the attribute *vendor* in CPE Name *cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0* get three values: *sun*, *bea* and *mysql*.
* The **not logical values of the attributes in version 2.3** of CPE specification always start and end with double quotes. For example, the value of attribute *product* in CPE Name *wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8", update="beta"]* is *"internet\_explorer"*, not *internet\_explorer* without double quotes.
* Some **CPE Names of version 1.1 with several systems or elements defined** cannot convert into other CPE versions, for example, the CPE Name *cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0*
* **Comparing a CPE Name of version 1.1 with others**, if versions are incompatible, then the return value is *False* instead of raising an exception. 
* The methods ***ovalcheck* and *ocilcheck*** of CPELanguage2_3 class is **not implemented**.
* The language attribute of CPE Names only allow the normal language tags according to the shortest ISO 639 code in language part and the ISO 3166-1 and UN M.49 code in region part. The extended, registered or reserved subtags are not supported.

[--- Return to index ---](#index)

<h2 id="7-bugtracker">7. Bugtracker</h2>

If you have any suggestions, bug reports or annoyances please report them to the issue tracker at <https://github.com/galindale/cpe/issues>

[--- Return to index ---](#index)

<h2 id="8-todo">8. TODO</h2>

* Implement methods *ovalcheck* and *ocilcheck* of CPELanguage2_3 class.
* Implement versions 2.0 and 2.1 of CPE specification.
* Implement methods *as\_uri\_1\_1* and *as\_uri\_2\_2* to convert any CPE Name into a CPE Name of versions 1.1 and 2.2 respectively.

[--- Return to index ---](#index)

<h2 id="9-authors">9. Authors</h2>

* Alejandro Galindo García: <galindo.garcia.alejandro@gmail.com>
* Roberto Abdelkader Martínez Pérez: <robertomartinezp@gmail.com>

[--- Return to index ---](#index)

<h2 id="10-license">10. License</h2>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

[--- Return to index ---](#index)

<h2 id="11-references">11. References</h2>

* [1] CPE: [http://scap.nist.gov/specifications/cpe/] [cpe]
* [2] About CPE: [http://cpe.mitre.org/about/] [about_cpe]
* [3] CPE Archive: [http://cpe.mitre.org/cpe/archive/] [cpe_archive]
* [4] CPE 1.1: [http://cpe.mitre.org/specification/1.1/cpe-specification_1.1.pdf] [cpe11]
* [5] CPE 2.2: [http://cpe.mitre.org/specification/2.2/cpe-specification_2.2.pdf] [cpe22]
* [6] CPE 2.3 - Naming Specification: [http://csrc.nist.gov/publications/nistir/ir7695/NISTIR-7695-CPE-Naming.pdf] [cpe23_naming]
* [7] CPE 2.3 - Name Matching Specification: [http://csrc.nist.gov/publications/nistir/ir7696/NISTIR-7696-CPE-Matching.pdf] [cpe23_matching]
* [8] CPE 2.3 - Applicability Language Specification: [http://csrc.nist.gov/publications/nistir/ir7698/NISTIR-7698-CPE-Language.pdf] [cpe23_language]

[cpe]: http://scap.nist.gov/specifications/cpe/
[about_cpe]: http://cpe.mitre.org/about/
[cpe_archive]: http://cpe.mitre.org/cpe/archive/
[cpe11]: http://cpe.mitre.org/specification/1.1/cpe-specification_1.1.pdf
[cpe22]: http://cpe.mitre.org/specification/2.2/cpe-specification_2.2.pdf
[cpe23_naming]: http://csrc.nist.gov/publications/nistir/ir7695/NISTIR-7695-CPE-Naming.pdf
[cpe23_matching]: http://csrc.nist.gov/publications/nistir/ir7696/NISTIR-7696-CPE-Matching.pdf
[cpe23_language]: http://csrc.nist.gov/publications/nistir/ir7698/NISTIR-7698-CPE-Language.pdf

[--- Return to index ---](#index)
