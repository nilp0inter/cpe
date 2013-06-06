#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module is an implementation of CPE language matching
algorithm in accordance with version 2.2 of CPE (Common Platform
Enumeration) specification.

Copyright (C) 2013  Roberto A. Martínez, Alejandro Galindo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the cpe packge, or general questions and
feedback about it, please contact: galindo.garcia.alejandro@gmail.com.
'''

from cpe2_2 import CPE2_2
from xml.dom import minidom


class CPELanguage2_2(object):
    """
    Represents an expression in the CPE Language.

    This class allows match a CPE element against an expression
    in the CPE Language, that is, a XML document format for
    binding descriptive prose and diagnostic test to a CPE name
    (CPE Description Format).
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, expression, isFile=False):
        """
        Create an object that contains the input expression in
        the CPE Language (a set of CPE Names) and
        the DOM tree asociated with expression.

        INPUT:
            - expression: XML content in string or a path to XML file
            - isFile: indicates whether expression is a XML file or
                      XML content string
        OUPUT:
            - None
        """

        if isFile:
            self.expression = ""
            self.path = expression

            # Parse an XML file by name (filepath)
            self.document = minidom.parse(self.expression)
        else:
            self.expression = expression
            self.path = ""

            # Parse an XML stored in a string
            self.document = minidom.parseString(self.expression)

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.
        """

        return "CPE language version 2.2\n" + self.expression

    def language_match(self, cpeset, cpel_dom=None):
        """
        Accepts a set of known CPE Names and an expression in the CPE language,
        and delivers the answer 'true' if the expression matches with the set.
        Otherwise, it returns 'false'.

        INPUT:
            - self: An expression in the CPE Language, represented as
                    the XML infoset for the platform element.
            - cpeset: CPE set object to match with self expression.
            - cpel_dom: An expression in the CPE Language, represented as
                       DOM tree.
        OUTPUT:
            - True if self expression can be satisfied by language matching
              against cpeset, False otherwise.

        - TEST: matching
        >>> from cpeset2_2 import CPESet2_2
        >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform id="123"><cpe:title>Sun Solaris 5.8 or 5.9 with BEA Weblogic 8.1 installed</cpe:title><cpe:logical-test operator="AND" negate="FALSE"><cpe:logical-test operator="OR" negate="FALSE"><cpe:fact-ref name="cpe:/o:sun:solaris:5.8" /><cpe:fact-ref name="cpe:/o:sun:solaris:5.9" /></cpe:logical-test><cpe:fact-ref name="cpe:/a:bea:weblogic:8.1" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

        >>> c1 = CPE2_2('cpe:/o:sun:solaris:5.9:::en-us')
        >>> c2 = CPE2_2('cpe:/a:bea:weblogic:8.1')

        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)

        >>> l = CPELanguage2_2(document)
        >>> l.language_match(s)
        True

        - TEST: matching
        >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform><cpe:title>Windows with secedit.exe tool </cpe:title><cpe:logical-test operator="OR" negate="FALSE"><cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" /><cpe:fact-ref name="cpe:/o:microsoft:windows_7" /><cpe:fact-ref name="cpe:/o:microsoft:windows_vista" /><cpe:fact-ref name="cpe:/o:microsoft:windows_2003" /><cpe:fact-ref name="cpe:/o:microsoft:windows_2003_server" /><cpe:fact-ref name="cpe:/o:microsoft:windows_xp" /><cpe:fact-ref name="cpe:/o:microsoft:windows_2000" /><cpe:fact-ref name="cpe:/o:microsoft:windows_nt" /><cpe:fact-ref name="cpe:/o:microsoft:windows-nt" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

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
        >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform><cpe:title>Windows with secedit.exe tool </cpe:title><cpe:logical-test operator="AND" negate="TRUE"><cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" /><cpe:fact-ref name="cpe:/o:microsoft:windows_xp" /><cpe:fact-ref name="cpe:/o:microsoft:windows_2000" /><cpe:fact-ref name="cpe:/o:microsoft:windows_nt" /><cpe:fact-ref name="cpe:/o:microsoft:windows-nt" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

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
        >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform><cpe:title>Windows with secedit.exe tool </cpe:title><cpe:logical-test operator="AND" negate="FALSE"><cpe:fact-ref name="cpe:/o:microsoft:windows_server_2008" /><cpe:fact-ref name="cpe:/o:microsoft:windows_xp" /><cpe:fact-ref name="cpe:/o:microsoft:windows_2000" /><cpe:fact-ref name="cpe:/o:microsoft:windows_nt" /><cpe:fact-ref name="cpe:/o:microsoft:windows-nt" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

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

        # Tags
        TAG_ROOT = '#document'
        TAG_PLATSPEC = 'cpe:platform-specification'
        TAG_PLATFORM = 'cpe:platform'
        TAG_LOGITEST = 'cpe:logical-test'
        TAG_CPE = 'cpe:fact-ref'

        # Tag attributes
        ATT_NAME = 'name'
        ATT_OP = 'operator'
        ATT_NEGATE = 'negate'

        # Attribute values
        ATT_OP_AND = 'AND'
        ATT_OP_OR = 'OR'
        ATT_NEGATE_TRUE = 'TRUE'

        if cpel_dom is None:
            cpel_dom = self.document

        # Identify the root element
        if cpel_dom.nodeName == TAG_ROOT or cpel_dom.nodeName == TAG_PLATSPEC:
            for node in cpel_dom.childNodes:
                if node.nodeName == TAG_PLATSPEC:
                    return self.language_match(cpeset, node)
                if node.nodeName == TAG_PLATFORM:
                    return self.language_match(cpeset, node)

        # Identify a platform element
        elif cpel_dom.nodeName == TAG_PLATFORM:
            for node in cpel_dom.childNodes:
                if node.nodeName == TAG_LOGITEST:
                    return self.language_match(cpeset, node)

        # Identify a CPE element
        elif cpel_dom.nodeName == TAG_CPE:
            cpename = cpel_dom.getAttribute(ATT_NAME)
            c = CPE2_2(cpename)

            # Try to match a CPE name with CPE set
            return cpeset.name_match(c)

        # Identify a logical operator element
        elif cpel_dom.nodeName == TAG_LOGITEST:
            count = 0
            len = 0
            answer = False

            for node in cpel_dom.childNodes:
                if node.nodeName.find("#") == 0:
                    continue
                len = len + 1
                if self.language_match(cpeset, node):
                    count = count + 1

            operator = cpel_dom.getAttribute(ATT_OP).upper()

            if operator == ATT_OP_AND:
                if count == len:
                    answer = True
            elif operator == ATT_OP_OR:
                if count > 0:
                    answer = True

            operator_not = cpel_dom.getAttribute(ATT_NEGATE)
            if operator_not:
                if operator_not.upper() == ATT_NEGATE_TRUE:
                    answer = not answer

            return answer
        else:
            return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
