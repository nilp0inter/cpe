#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification.

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

from .cpecomp_simple import CPEComponentSimple

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

        :returns: Representation of CPE component as string
        :rtype: string
        """

        value = self.get_value()

        return "{0}({1})".format(self.__class__.__name__, value)

    def _is_valid_language(self):
        """
        Return True if the value of component in attribute "language" is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean

        CASE 1: Language part with/without region part
        CASE 2: Language part without region part
        CASE 3: Region part with language part
        CASE 4: Region part without language part
        """

        def check_generic_language(self, value):
            """
            Check possible values in language part
            when region part exists or not in language value.

            Possible values of language attribute: a=letter
            | *a
            | *aa
            | aa
            | aaa
            | ?a
            | ?aa
            | ??
            | ??a
            | ???
            """
            lang_pattern = []
            lang_pattern.append("^(\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append("[a-z]{1,2}")
            lang_pattern.append("|\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append("(([a-z][a-z]?)|(\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append("(\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append("|[a-z])?))")
            lang_pattern.append("|([a-z]{2,3}))$")

            lang_rxc = re.compile("".join(lang_pattern))

            return lang_rxc.match(value)

        def check_language_without_region(self, value):
            """
            Check possible values in language part
            when region part not exist in language value.

            Possible values of language attribute: a=letter
            | a?
            | aa?
            | a??
            | a*
            | aa*
            | aaa*
            | *a*
            | *a?
            | ?a*
            | ?a?
            """
            lang_pattern = []
            lang_pattern.append("^([a-z]")
            lang_pattern.append("([a-z](\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append("|\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append("|")
            lang_pattern.append("([a-z]\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append("))")
            lang_pattern.append("|")
            lang_pattern.append("\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append("(\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append(")?")
            lang_pattern.append("|\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append(")|\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append("[a-z](\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append("|\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append(")")
            lang_pattern.append("|\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append("[a-z](\\")
            lang_pattern.append(self.WILDCARD_MULTI)
            lang_pattern.append("|\\")
            lang_pattern.append(self.WILDCARD_ONE)
            lang_pattern.append(")")
            lang_pattern.append(")$")

            lang_rxc = re.compile("".join(lang_pattern))

            return lang_rxc.match(value)

        def check_region_with_language(self, value):
            """
            Check possible values in region part when language part exists.

            Possible values of language attribute: a=letter, 1=digit
            | *
            | a*
            | a?
            | aa
            | ??
            | 1*
            | 1??
            | 11*
            | 11?
            | 111
            | ???
            """
            region_pattern = []
            region_pattern.append("^(")
            region_pattern.append("(\\")
            region_pattern.append(self.WILDCARD_MULTI)
            region_pattern.append(")|((\\")
            region_pattern.append(self.WILDCARD_ONE)
            region_pattern.append("){2,3})|([a-z]([a-z]|\\")
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
            return region_rxc.match(region)

        def check_region_without_language(self, value):
            """
            Check possible values in region part when language part not exist.

            Possible values of language attribute: 1=digit
            | *111
            | *11
            | *1
            """
            region_pattern = []
            region_pattern.append("^(")
            region_pattern.append("(\\")
            region_pattern.append(self.WILDCARD_MULTI)
            region_pattern.append("[0-9])")
            region_pattern.append("([0-9]([0-9])?)?")
            region_pattern.append(")$")

            region_rxc = re.compile("".join(region_pattern))
            return region_rxc.match(region)

        comp_str = self._encoded_value.lower()

        # Value with wildcards; separate language and region of value
        parts = comp_str.split(self.SEPARATOR_LANG)
        language = parts[0]
        region_exists = len(parts) == 2

        # Check the language part
        if check_generic_language(self, language) is not None:
            # Valid language, check region part
            if region_exists:
                # Region part exists; check it
                region = parts[1]
                return (check_region_with_language(self, region) is not None)
            else:
                # Not region part
                return True
        elif check_language_without_region(self, language) is not None:
            # Language without region; region part should not exist
            return not region_exists
        else:
            # Language part not exist; check region part
            region = parts[0]
            return check_region_without_language(self, region) is not None

    def _is_valid_part(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        :returns: True if value of component is valid, False otherwise
        :rtype: boolean
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
