#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is an implementation of CPE language matching
algorithm in accordance with version 2.2 of CPE (Common Platform
Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
"""

from .cpe2_2 import CPE2_2
from .cpelang import CPELanguage


class CPELanguage2_2(CPELanguage):
    """
    Represents an expression in the CPE Language.

    This class allows match a CPE element against an expression
    in the CPE Language, that is, a XML document format for
    binding descriptive prose and diagnostic test to a CPE name
    (CPE Description Format).
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Version of CPE Language
    VERSION = "2.2"

    ####################
    #  OBJECT METHODS  #
    ####################

    def language_match(self, cpeset, cpel_dom=None):
        """
        Accepts a set of known CPE Names and an expression in the CPE language,
        and delivers the answer True if the expression matches with the set.
        Otherwise, it returns False.

        :param CPELanguage self: An expression in the CPE Applicability
            Language, represented as the XML infoset for the platform element.
        :param CPESet cpeset: CPE set object to match with self expression.
        :param string cpel_dom: An expression in the CPE Applicability
            Language, represented as DOM tree.
        :returns: True if self expression can be satisfied by language matching
            against cpeset, False otherwise.
        :rtype: boolean
        """

        # Root element tag
        TAG_ROOT = '#document'
        # A container for child platform definitions
        TAG_PLATSPEC = 'cpe:platform-specification'

        # Information about a platform definition
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
    doctest.testfile("tests/testfile_cpelang2_2.txt")
