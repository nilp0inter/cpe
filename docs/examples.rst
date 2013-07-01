Usage examples
==============

This section explains with several examples how to use this package to create both CPE Names and platforms in a particular version of CPE specification.

Naming
------

To create a new CPE Name, the cpe package provides a generating class of CPE objects called CPE. It implements the factory pattern and receive two parameters: version of CPE specification and URI associated with CPE Name. Also, it is possible create a instance of a particular version of CPE Name directly using the class associated with the version.

In the following example, some CPE Names of different versions of CPE specification are created:

* Imports the class::

    >>> from cpe import CPE

* Creates a CPE Name of version 1.1 with an operating system and an application parts, without setting the version directly (auto version)::

    >>> str11 = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
    >>> c11 = CPE(str11)

* Creates a CPE Name of version 2.2 with an operating system where the version is set (manual version)::

    >>> str22 = 'cpe:/o:redhat:enterprise_linux:4:update4'
    >>> c22 = CPE(str22, CPE.VERSION_2_2)

* Creates a CPE Name of version 2.3 (URI style) with an application system where the value of edition component is packed::

    >>> str23_uri = 'cpe:/a:hp:insight_diagnostics:8::~~online~win2003~x64~'
    >>> c23_uri = CPE(str23_uri)

* Creates a CPE Name of version 2.3 (WFN style) with an application system where some values have wildcards::

    >>> str23_wfn = 'wfn:[part="a", vendor="hp", product="?insight_diagnostics?", version="8\.*", target_sw=ANY, target_hw="x32"]'
    >>> c23_wfn = CPE(str23_wfn)

* Creates a CPE Name of version 2.3 (formatted string style) with a hardware system::

    >>> str23_fs = 'cpe:2.3:h:cisco:ios:12.3:enterprise:*:*:*:*:*:*'
    >>> c23_fs = CPE(str23_fs)

The cpe package provides methods to get the value of components of a CPE Name (these functions always return a string list) and identify the type of system associated with it (hardware, operating system or application)::

    >>> c11.get_product()                   # Compound product attribute (v1.1)
    ['enterprise_linux', 'httpd']
    >>> c22.get_update()                    # Simple Update attribute (v2.2)
    ['update4']
    >>> c23_uri.get_target_hardware()       # Simple Target_hw attribute (v2.3, URI style)
    ['x64']
    >>> c23_wfn.get_target_hardware()       # Simple Target_hw attribute (v2.3, WFN style)
    ['"x32"']
    >>> c23_wfn.get_target_software()       # Target_sw attribute with logical value(v2.3, WFN style)
    ['ANY']
    >>> c23_fs.is_hardware()                # Type of system (v2.3, formatted string style)
    True

Finally, the cpe package contains methods to convert any CPE Name defined under a particular style (URI version 2.3, WFN or formatted string) in other different styles::

    >>> c22.as_wfn()
    'wfn:[part="o", vendor="redhat", product="enterprise_linux", version="4", update="update4"]'
    >>> c23_uri.as_uri_2_3()
    'cpe:/a:hp:insight_diagnostics:8::~~online~win2003~x64~'
    >>> c23_wfn.as_fs()
    'cpe:2.3:a:hp:?insight_diagnostics?:8.*:*:*:*:*:*:x32:*'

Name matching
-------------

To create a set of CPE Name the package cpe provides the CPESetX\_Y class, where X\_Y is the target version of CPE specification. The *name_match* function of set allows do the name matching of CPE specification.

In the following example, a set of CPE Names of version 2.2 is created and the name matching is realized:

* Imports the classes of version::

    >>> from cpe.cpe2_2 import CPE2_2
    >>> from cpe.cpeset2_2 import CPESet2_2

* Creates the CPE Names of target system::

    >>> c1 = CPE2_2('cpe:/o:microsoft:windows_2000::sp3:pro')
    >>> c2 = CPE2_2('cpe:/a:microsoft:ie:5.5')

* Creates a set that contains the above CPE Names (known instances): K = {"cpe:/o:microsoft:windows\_2000::sp3:pro", "cpe:/a:microsoft:ie:5.5"}::

    >>> K = CPESet2_2()
    >>> K.append(c1)
    >>> K.append(c2)

* Create the candidate CPE Name. It represents a rule in a security guidance checklist describes some settings to check on a system running Microsoft Windows 2000: X = "cpe:/o:microsoft:windows\_2000"::
 
    >>> X = CPE2_2('cpe:/o:microsoft:windows_2000')

* Does the name matching::

    >>> K.name_match(X)
    True

There are three components in X: C1=o, C2=microsoft, C3=windows\_2000. Each component matches the corresponding component of the first CPE Name in K. So, the algorithm returns true and the rule can be applied to the target system.

Language matching
-----------------

To create an expression of CPE Language the cpe package provides the CPELanguageX\_Y class, where X\_Y is the version of CPE specification used. The *language_match* function of class allows do the language matching of CPE specification.

In the following example, an expression of CPE Language of version 2.2 is created and the language matching is done:

* Imports the classes of version::

    >>> from cpe import CPE
    >>> from cpe.cpeset2_2 import CPESet2_2
    >>> from cpe.cpelang2_2 import CPELanguage2_2

* Creates the CPE Names of target system::

    >>> c1 = CPE('cpe:/o:sun:solaris:5.9:::en-us', CPE.VERSION_2_2)
    >>> c2 = CPE('cpe:/a:bea:weblogic:8.1', CPE.VERSION_2_2)

* Creates a set that contains the above CPE Names (known instances): K = {"cpe:/o:sun:sunos:5.9:::en-us", "cpe:/a:bea:weblogic:8.1"}::

    >>> K = CPESet2_2()
    >>> K.append(c1)
    >>> K.append(c2)

* Creates the expression in XML of candidate CPE Language statement:

  X = <cpe:platform id="123">
          <cpe:title>Sun Solaris 5.8 or 5.9 with BEA Weblogic 8.1 installed</cpe:title>  
    
          <cpe:logical-test operator="AND" negate="FALSE">

              <cpe:logical-test operator="OR" negate="FALSE">

                  <cpe:fact-ref name="cpe:/o:sun:solaris:5.8" />
    
                  <cpe:fact-ref name="cpe:/o:sun:solaris:5.9" />

              </cpe:logical-test>

              <cpe:fact-ref name="cpe:/a:bea:weblogic:8.1" />

          </cpe:logical-test>

      </cpe:platform>

  ::

    >>> It is necessary specify the "cpe:platform-specification" tag
    >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform id="123"><cpe:title>Sun Solaris 5.8 or 5.9 with BEA Weblogic 8.1 installed</cpe:title><cpe:logical-test operator="AND" negate="FALSE"><cpe:logical-test operator="OR" negate="FALSE"><cpe:fact-ref name="cpe:/o:sun:solaris:5.8" /><cpe:fact-ref name="cpe:/o:sun:solaris:5.9" /></cpe:logical-test><cpe:fact-ref name="cpe:/a:bea:weblogic:8.1" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

* Does the language matching::

    >>> X = CPELanguage2_2(document)
    >>> X.language_match(K)
    True
