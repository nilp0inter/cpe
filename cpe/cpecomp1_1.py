#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 1.1 of CPE (Common Platform Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo

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
feedback about it, please contact: galindo.garcia.alejandro@gmail.com.
'''

from cpecomp import CPEComponent
import re


class CPEComponent1_1(CPEComponent):
    """
    Represents a component of version 1.1 of CPE specification.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str):
        """
        Store the value of component and parse it to validate it.

        INPUT:
            - comp_str: value of component
        OUPUT:
            - None
        """

        super(CPEComponent1_1, self).__init__(comp_str)
        self._parse(comp_str)

    def _parse(self, comp_str):
        """
        Check the input component value is correct.

        INPUT:
            - comp_str: value of component
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: incorrect value of component

        TEST: simple value
        >>> value = "microsoft"
        >>> comp = CPEComponent1_1(value)

        TEST: value with negation
        >>> value = "~microsoft"
        >>> comp = CPEComponent1_1(value)

        TEST: value with OR operation
        >>> value = "xp!vista"
        >>> comp = CPEComponent1_1(value)

        TEST: NOT and OR operators cannot be together
        >>> value = "~xp!vista"
        >>> comp = CPEComponent1_1(value) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Not correct value '~xp!vista'
        """

        if comp_str != CPEComponent.EMPTY_COMP_VALUE:
            # Compilation of regular expression associated with
            # components
            string = "\w\.\-,\(\)@\#"
            negate_pattern = "~[%s]+" % string
            not_negate_pattern = "[%s]+(![%s]+)*" % (string, string)
            cpe_comp_pattern = "^((%s)|(%s))$" % (negate_pattern,
                                                  not_negate_pattern)
            cpe_comp_rxc = re.compile(cpe_comp_pattern)

            # Partitioning of components in subcomponents
            comp_match = cpe_comp_rxc.match(comp_str)

            # Validation of components
            if (comp_match is None):
                errmsg = "Not correct value '%s'" % comp_str

                raise ValueError(errmsg)

        # Value of component is correct
        if comp_str == CPEComponent.EMPTY_COMP_VALUE:
            self._data = CPEComponent.ANY_VALUE
            self._is_negated = False
        else:
            self._data = comp_str.replace('~', '').split('!')
            self._is_negated = comp_str.startswith('~')

if __name__ == "__main__":

    import doctest
    doctest.testmod()
