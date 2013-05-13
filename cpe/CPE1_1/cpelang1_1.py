#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpelang1_1.py
Author: Alejandro Galindo
Date: 06-05-2013
Description: Implementation of CPE language matching algorithm
             in accordance with version 1.1 of specification CPE
             (Common Platform Enumeration).

             This class allows:
             - match a CPE element against an expression in the CPE Language,
             that is, a XML document format for binding descriptive prose and
             diagnostic test to a CPE Name (CPE Description Format).
'''


from cpe1_1 import CPE1_1
from cpe1_1 import CPESet1_1
from xml.dom import minidom
import types


class CPELanguage1_1(object):
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
        if isinstance(self.expression, types.StringTypes):
            # Parse an XML file by name (filepath)
            self.document = minidom.parseString(self.expression)
        else:
            # Parse an XML stored in a string
            self.document = minidom.parse(self.expression)

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
        """

        if cpel_dom is None:
            cpel_dom = self.document
        if cpel_dom.nodeName == '#document' or cpel_dom.nodeName == 'cpe-list':
            for node in cpel_dom.childNodes:
                if node.nodeName == 'cpe-item':
                    return self.language_match(cpeset, node)
        elif cpel_dom.nodeName == 'cpe-item':
            cpename = cpel_dom.getAttribute('name')
            c = CPE1_1(cpename)
            return cpeset.name_match(c)
        else:
            return False

if __name__ == "__main__":

    document = """\
        <?xml version="1.0">
        <cpe-list xmlns="http://cpe.mitre.org/XMLSchema/cpe/1.0"
                  xmlns:cpe="http://cpe.mitre.org/XMLSchema/cpe/1.0">
            <cpe-item name="cpe://redhat:enterprise_linux:3">
                <title>Red Hat Enterprise Linux 3</title>
            </cpe-item>
            <cpe-item name="cpe://sun:sunos:5.8">
                <title>Sun Microsystems SunOS 5.8</title>
                <notes>
                    <note>Also known as Solaris 8</note>
                </notes>
            </cpe-item>
            <cpe-item name="cpe://microsoft:windows:2003">
                <titleMicrosoft Windows Server 2003></title>
                <check system="http://oval.mitre.org/XMLSchema/oval-definitions-5">oval:org.mitre.oval:def:128</check>
            </cpe-item>
            <cpe-item name="cpe:/intel:ia-64:itanium">
                <title>Intel Itanium (IA-64)</title>
            </cpe-item>
        </cpe-list>
    """

    c1 = CPE1_1('cpe://microsoft:windows:2003')
    c2 = CPE1_1('cpe:/intel:ia-64:itanium:xp')

    s = CPESet1_1()
    s.append(c1)
    s.append(c2)

    lang = CPELanguage1_1(document)
    print lang.languag_matching(s)

#    import doctest
#    doctest.testmod()
