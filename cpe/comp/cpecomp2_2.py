#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.2 of CPE (Common Platform Enumeration) specification.

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


class CPEComponent2_2(CPEComponentSimple):
    """
    Represents a component of version 2.2 of CPE specification.

    TEST: simple value

    >>> value = "microsoft"
    >>> comp = CPEComponent2_2(value, CPEComponentSimple.ATT_VENDOR)
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Pattern used to check the value of component
    _VALUE_PATTERN = "^([\d\w\._\-~%]+)$"

    #: Separator of components of CPE name with URI style
    SEPARATOR_COMP = ":"

    #: Characters of version 2.2 of CPE name to convert
    #: to standard value (WFN value)
    NON_STANDARD_VALUES = [".", "-", "~", "%"]

    # Logical values in string format

    #: Logical value associated with a undefined component of CPE Name
    VALUE_UNDEFINED = None

    #: Logical value associated with a component without value set
    VALUE_EMPTY = ""

    ###############
    #  VARIABLES  #
    ###############

    #: Compilation of pattern used to check the value of component
    _value_rxc = re.compile(_VALUE_PATTERN)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        :returns: Representation of CPE component as string
        :rtype: string
        """

        return "{0}({1})".format(self.__class__.__name__, self.get_value())

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value).
        """

        result = []
        idx = 0
        s = self._encoded_value

        while (idx < len(s)):
            # Get the idx'th character of s
            c = s[idx]

            if (c in CPEComponent2_2.NON_STANDARD_VALUES):
                # Escape character
                result.append("\\")
                result.append(c)
            else:
                # Do nothing
                result.append(c)

            idx += 1

        self._standard_value = "".join(result)

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._encoded_value
        return CPEComponent2_2._value_rxc.match(comp_str) is not None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("../tests/testfile_cpecomp2_2.txt")
