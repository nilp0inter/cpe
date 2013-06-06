#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name and
compare two components to know if they are equal.

Copyright (C) 2013  Alejandro Galindo, Roberto A. Martínez

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


class CPEComponent(object):
    """
    Represents a generic component of CPE name compatible with
    the components of all versions of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Value of an empty component. For example, product in the CPE name
    # cpe:/cisco::2345 of version 1.1 of CPE specification
    EMPTY_VALUE = ""

    # Value of an undefined component. For example, edition in the CPE name
    # cpe:/cisco::2345 of version 1.1 of CPE specification
    UNDEFINED_VALUE = None

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _isAnyValue(cls, value):
        """
        Returns True if value is an empty or undefined value.
        """

        return ((value == CPEComponent.EMPTY_VALUE) or
               (value is CPEComponent.UNDEFINED_VALUE))

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str):
        """
        Store the value of component.

        INPUT:
            - comp_str: value of component
        OUPUT:
            - None
        """

        if comp_str == CPEComponent.UNDEFINED_VALUE:
            self._data = None
        else:
            self._data = [comp_str]

        self._is_negated = False

    def __eq__(self, other):
        """
        Returns True if self and other are equal components.
        """

        return ((self._data == other._data) and
               (self._is_negated == other._is_negated))

    def __ne__(self, other):
        """
        Returns True if self and other are equal components.
        """

        return not (self == other)

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        INPUT:
            - self: set of elements
            - item: elem to find in self
        OUTPUT:
            - True if item is included in set of self

        TEST: a empty value with a single value
        >>> comp1 = CPEComponent('xp')
        >>> comp2 = CPEComponent('')
        >>> comp1 in comp2
        True

        TEST: a empty value with a single value
        >>> comp1 = CPEComponent('')
        >>> comp2 = CPEComponent('xp')
        >>> comp1 in comp2
        False

        TEST: two single equal values
        >>> comp1 = CPEComponent('xp')
        >>> comp2 = CPEComponent('xp')
        >>> comp1 in comp2
        True

        TEST: two single different values
        >>> comp1 = CPEComponent('vista')
        >>> comp2 = CPEComponent('xp')
        >>> comp1 in comp2
        False

        TEST: two single different values
        >>> comp1 = CPEComponent('xp!vista')
        >>> comp2 = CPEComponent('xp')
        >>> comp1 in comp2
        False
        """

        if ((self == item) or (self._data is CPEComponent.UNDEFINED_VALUE)):
            return True

        if len(self._data) == 1:
            if self._data[0] == CPEComponent.EMPTY_VALUE:
                return True

        return False

    def __str__(self):
        """
        Returns a human-readable representation of CPE component.
        """

        if CPEComponent._isAnyValue(self._data):
            txt = "<ANY>"
        else:
            txt = self._data

        if self._is_negated:
            txt = "NOT(%s)" % txt

        return txt

if __name__ == "__main__":
    import doctest
    doctest.testmod()
