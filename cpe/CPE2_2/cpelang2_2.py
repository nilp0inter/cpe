#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpelang2_2.py
Author: Alejandro Galindo
Date: 13-05-2013
Description: Implementation of CPE language matching algorithm
             in accordance with version 2.2 of specification CPE
             (Common Platform Enumeration).

             This class allows:
             - match a CPE element against an expression in the CPE Language,
             that is, a XML document format for binding descriptive prose and
             diagnostic test to a CPE Name (CPE Description Format).
'''


from cpe2_2 import CPE2_2
from cpeset2_2 import CPESet2_2
from xml.dom import minidom

import re


class CPELanguage2_2(object):
    """
    Represents an expression in the CPE Language.
    """

    def __init__(self, expression):
        """
        Create an object that contains the input expression in
        the CPE Language (a set of CPE Names) and
        the DOM tree asociated with expression.
        """

        self.expression = expression

        xml_rxc = re.compile("^\<\?xml")
        if xml_rxc.match(self.expression) is None:
            # Parse an XML file by name (filepath)
            self.document = minidom.parse(self.expression)
        else:
            # Parse an XML stored in a string
            self.document = minidom.parseString(self.expression)

    def __repr__(self):
        return self.expression

    def language_match(self, cpeset, cpel_dom=None):
        """
        Accepts a set of known CPE Names and an expression in the CPE language,
        and delivers the answer 'true' if the expression matches with the set.
        Otherwise, it returns 'false'.

        Inputs:
            - self: An expression in the CPE Language, represented as
                    the XML infoset for the platform element.
            - cpeset: CPE set object to match with self expression.
            - cpel_dom: An expression in the CPE Language, represented as
                       DOM tree.
        Output:
            - True if self expression can be satisfied by language matching
              against cpeset, False otherwise.

        - TEST: matching
        >>> document = '''\
        ... <?xml version="1.0" encoding="UTF-8"?>
        ... <cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0">
        ...     <cpe:platform id="123">
        ...         <cpe:title>Sun Solaris 5.8 or 5.9 with BEA Weblogic 8.1 installed</cpe:title>
        ...         <cpe:logical-test operator="AND" negate="FALSE">
        ...             <cpe:logical-test operator="OR" negate="FALSE">
        ...                 <cpe:fact-ref name="cpe:/o:sun:solaris:5.8" />
        ...                 <cpe:fact-ref name="cpe:/o:sun:solaris:5.9" />
        ...             </cpe:logical-test>
        ...             <cpe:fact-ref name="cpe:/a:bea:weblogic:8.1" />
        ...         </cpe:logical-test>
        ...     </cpe:platform>
        ... </cpe:platform-specification>
        ... '''
        >>> c1 = CPE2_2('cpe:/o:sun:solaris:5.9:::en-us')
        >>> c2 = CPE2_2('cpe:/a:bea:weblogic:8.1')

        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)

        >>> l = CPELanguage2_2(document)
        >>> l.language_match(s)
        True

        - TEST: matching
        >>> document = '''\
        ... <?xml version="1.0" encoding="UTF-8"?>
        ... <cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0">
        ...     <cpe:platform>
        ...         <cpe:title>Windows with secedit.exe tool </cpe:title>
        ...         <cpe:logical-test operator="OR" negate="FALSE">
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_7" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_vista" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_2003" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_2003_server" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_xp" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_2000" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_nt" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows-nt" />
        ...         </cpe:logical-test>
        ...     </cpe:platform>
        ... </cpe:platform-specification>
        ... '''
        >>> c1 = CPE2_2('cpe:/o:microsoft:windows_2000::pro')
        >>> c2 = CPE2_2('cpe:/a:microsoft:office:2007')
        >>> c3 = CPE2_2('cpe:/o:sun:solaris:5')

        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c3)

        >>> l = CPELanguage2_2(document)
        >>> l.language_match(s)
        True

        - TEST: matching (negate)
        >>> document = '''\
        ... <?xml version="1.0" encoding="UTF-8"?>
        ... <cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0">
        ...     <cpe:platform>
        ...         <cpe:title>Windows with secedit.exe tool </cpe:title>
        ...         <cpe:logical-test operator="AND" negate="TRUE">
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_xp" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_2000" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_nt" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows-nt" />
        ...         </cpe:logical-test>
        ...     </cpe:platform>
        ... </cpe:platform-specification>
        ... '''
        >>> c1 = CPE2_2('cpe:/o:microsoft:windows_2000::pro')
        >>> c2 = CPE2_2('cpe:/a:microsoft:office:2007')
        >>> c3 = CPE2_2('cpe:/o:sun:solaris:5')

        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c3)

        >>> l = CPELanguage2_2(document)
        >>> l.language_match(s)
        True

        - TEST: not matching
        >>> document = '''\
        ... <?xml version="1.0" encoding="UTF-8"?>
        ... <cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0">
        ...     <cpe:platform>
        ...         <cpe:title>Windows with secedit.exe tool </cpe:title>
        ...         <cpe:logical-test operator="AND" negate="FALSE">
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_xp" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_2000" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows_nt" />
        ...             <cpe:fact-ref name="cpe:/o:microsoft:windows-nt" />
        ...         </cpe:logical-test>
        ...     </cpe:platform>
        ... </cpe:platform-specification>
        ... '''
        >>> c1 = CPE2_2('cpe:/o:microsoft:windows_2000::pro')
        >>> c2 = CPE2_2('cpe:/a:microsoft:office:2007')
        >>> c3 = CPE2_2('cpe:/o:sun:solaris:5')

        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c3)

        >>> l = CPELanguage2_2(document)
        >>> l.language_match(s)
        False
        """

        ROOT_TAG = '#document'
        PLATSPEC_TAG = 'cpe:platform-specification'
        PLATFORM_TAG = 'cpe:platform'
        LOGITEST_TAG = 'cpe:logical-test'
        CPE_TAG = 'cpe:fact-ref'

        if cpel_dom is None:
            cpel_dom = self.document

        # Identify the root element
        if cpel_dom.nodeName == ROOT_TAG or cpel_dom.nodeName == PLATSPEC_TAG:
            for node in cpel_dom.childNodes:
                if node.nodeName == PLATSPEC_TAG:
                    return self.language_match(cpeset, node)
                if node.nodeName == PLATFORM_TAG:
                    return self.language_match(cpeset, node)

        # Identify a platform element
        elif cpel_dom.nodeName == PLATFORM_TAG:
            for node in cpel_dom.childNodes:
                if node.nodeName == LOGITEST_TAG:
                    return self.language_match(cpeset, node)

        # Identify a CPE element
        elif cpel_dom.nodeName == CPE_TAG:
            cpename = cpel_dom.getAttribute('name')
            c = CPE2_2(cpename)

            # Try to match a CPE name with CPE set
            return cpeset.name_match(c)

        # Identify a logical operator element
        elif cpel_dom.nodeName == LOGITEST_TAG:
            count = 0
            len = 0
            answer = False

            for node in cpel_dom.childNodes:
                if node.nodeName.find("#") == 0:
                    continue
                len = len + 1
                if self.language_match(cpeset, node):
                    count = count + 1

            operator = cpel_dom.getAttribute('operator').upper()

            if operator == 'AND':
                if count == len:
                    answer = True
            elif operator == 'OR':
                if count > 0:
                    answer = True

            operator_not = cpel_dom.getAttribute('negate')
            if operator_not:
                if operator_not.upper() == 'TRUE':
                    answer = not answer

            return answer
        else:
            return False


if __name__ == "__main__":

#    document = """\
#<?xml version="1.0" encoding="UTF-8"?>
#<cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0">
#    <cpe:platform>
#        <cpe:title>Windows with secedit.exe tool </cpe:title>
#        <cpe:logical-test operator="OR" negate="FALSE">
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_7" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_vista" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_2003" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_2003_server" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_xp" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_2000" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows_nt" />
#            <cpe:fact-ref name="cpe:/o:microsoft:windows-nt" />
#        </cpe:logical-test>
#    </cpe:platform>
#</cpe:platform-specification>
#     """
#
#    c1 = CPE2_2('cpe:/o:microsoft:windows_2000::pro')
#    c2 = CPE2_2('cpe:/a:microsoft:office:2007')
#    c3 = CPE2_2('cpe:/o:sun:solaris:5')
#
#    s = CPESet2_2()
#    s.append(c1)
#    s.append(c2)
#    s.append(c3)
#
#    lang = CPELanguage2_2(document)
#    print lang.language_match(s)

    import doctest
    doctest.testmod()
