#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez

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

For any problems using the cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
'''

from cpecomp_simple import CPEComponentSimple

import re


class CPEComponent2_3(CPEComponentSimple):
    """
    Represents a component of version 2.3 of CPE specification.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        value = self.get_value()

        return "{0}({1})".format(self.__class__.__name__, value)

    def _is_valid_language(self):
        """
        Return True if the value of component in attribute "language" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise

        Possible values of language attribute: a=letter, 1=digit
        LANGUAGE VALUES
        *a
        *aa
        aa
        aaa
        ?a
        ?aa
        ??
        ??a
        ???

        LANGUAGE WITHOUT REGION VALUES
        a*
        aa*
        aaa*
        *111
        *11
        *1

        REGION WITH LANGUAGE VALUES
        *
        ??
        a*
        a?
        aa
        1*
        1?
        1??
        11*
        11?
        111
        """

        comp_str = self._encoded_value.lower()

        # Value with wildcards; separate language and region of value
        parts = comp_str.split(self.SEPARATOR_LANG)
        language = parts[0]

        # Check the language
        lang1_pattern = []
        lang1_pattern.append("^(\\")
        lang1_pattern.append(self.WILDCARD_MULTI)
        lang1_pattern.append("[a-z]{1,2}")
        lang1_pattern.append("|\\")
        lang1_pattern.append(self.WILDCARD_ONE)
        lang1_pattern.append("(([a-z][a-z]?)|(\\")
        lang1_pattern.append(self.WILDCARD_ONE)
        lang1_pattern.append("(\\")
        lang1_pattern.append(self.WILDCARD_ONE)
        lang1_pattern.append("|[a-z])?))")
        lang1_pattern.append("|([a-z]{2,3}))$")

        lang1_rxc = re.compile("".join(lang1_pattern))

        if lang1_rxc.match(language) is not None:
            # Correct language; check the region part
            region = parts[1]

            region_pattern = []
            region_pattern.append("^(")
            region_pattern.append("(\\")
            region_pattern.append(self.WILDCARD_MULTI)
            region_pattern.append(")|((\\")
            region_pattern.append(self.WILDCARD_ONE)
            region_pattern.append("){2})|([a-z]([a-z]|\\")
            region_pattern.append(self.WILDCARD_MULTI)
            region_pattern.append("|\\")
            region_pattern.append(self.WILDCARD_ONE)
            region_pattern.append("))|([0-9](\\")
            region_pattern.append(self.WILDCARD_MULTI)
            region_pattern.append("|\\")
            region_pattern.append(self.WILDCARD_ONE)
            region_pattern.append("(\\")
            region_pattern.append(self.WILDCARD_ONE)
            region_pattern.append(")?|[0-9][0-9\\")
            region_pattern.append(self.WILDCARD_MULTI)
            region_pattern.append("\\")
            region_pattern.append(self.WILDCARD_ONE)
            region_pattern.append("])))$")

            region_rxc = re.compile("".join(region_pattern))
            return region_rxc.match(region) is not None

        elif len(parts) == 1:
            # No region part in value
            lang2_pattern = []
            lang2_pattern.append("^((\\")
            lang2_pattern.append(self.WILDCARD_MULTI)
            lang2_pattern.append("\d{1,3})|([a-z]{1,3}\\")
            lang2_pattern.append(self.WILDCARD_MULTI)
            lang2_pattern.append("))$")

            lang2_rxc = re.compile("".join(lang2_pattern))
            return lang2_rxc.match(language) is not None

        else:
            return False

    def _is_valid_part(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value of component is valid, False otherwise
        """

        comp_str = self._encoded_value

        # Check if value of component do not have wildcard
        if ((comp_str.find(self.WILDCARD_ONE) == -1) and
           (comp_str.find(self.WILDCARD_MULTI) == -1)):

            return super(CPEComponent2_3, self)._is_valid_part()

        # Compilation of regular expression associated with value of part
        part_pattern = "^(\{0}|\{1})$".format(self.WILDCARD_ONE,
                                              self.WILDCARD_MULTI)
        part_rxc = re.compile(part_pattern)

        return part_rxc.match(comp_str) is not None
