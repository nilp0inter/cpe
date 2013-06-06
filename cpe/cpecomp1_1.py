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

    def __eq__(self, other):
        """
        Returns True if self and other are equal components.

        TEST: simple value
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('vista')
        >>> comp1 == comp2
        False

        TEST: value with negation
        >>> comp1 = CPEComponent1_1('~xp')
        >>> comp2 = CPEComponent1_1('xp!vista')
        >>> comp1 == comp2
        False

        TEST: value with negation
        >>> comp1 = CPEComponent1_1('xp!vista')
        >>> comp2 = CPEComponent1_1('~xp')
        >>> comp1 == comp2
        False

        TEST: value with OR operation
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('xp!vista')
        >>> comp1 == comp2
        False

        TEST: value with OR operation
        >>> comp1 = CPEComponent1_1('xp!vista')
        >>> comp2 = CPEComponent1_1('xp')
        >>> comp1 == comp2
        False

        TEST: two equal values
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('xp')
        >>> comp1 == comp2
        True

        TEST: an empty value and single value
        >>> comp1 = CPEComponent1_1('')
        >>> comp2 = CPEComponent1_1('xp')
        >>> comp1 == comp2
        False
        """

        return super(CPEComponent1_1, self).__eq__(other)

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        Comparatives in name matching of version 1.1 of CPE:

        c = self._data
        d = item._data

        IF c is empty THEN match True.
        ELSE IF c is a singleton AND c = d THEN match True.
        ELSE IF c has form ~v AND v != d THEN match True.
        ELSE IF c has form v1!v2!..!vn AND v = d for some v THEN match True.
        ENDIF.

        Examples:

        item._data = ['~xp']
        self._data = ['xp', 'vista']
        item in self => False

        item._data = ['xp']
        self._data = ['xp', 'vista']
        item in self => True

        item._data = ['xp', 'vista']
        self._data = ['xp']
        item in self => False

        INPUT:
            - self: set of elements
            - item: elem to find in self
        OUTPUT:
            - True if item is included in set of self

        TEST: two simple values
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('xp')
        >>> comp1 in comp2
        True

        TEST: two values with OR operator
        >>> comp1 = CPEComponent1_1('xp!vista')
        >>> comp2 = CPEComponent1_1('xp!vista')
        >>> comp1 in comp2
        True

        TEST: two different simple values
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('vista')
        >>> comp1 in comp2
        False

        TEST: a value with negation and another with OR operator
        >>> comp1 = CPEComponent1_1('~xp')
        >>> comp2 = CPEComponent1_1('xp!vista')
        >>> comp1 in comp2
        False

        TEST: a value with OR operator and another with negation
        >>> comp1 = CPEComponent1_1('xp!vista')
        >>> comp2 = CPEComponent1_1('~xp')
        >>> comp1 in comp2
        True

        TEST: a single value and a value with OR operator
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('xp!vista')
        >>> comp1 in comp2
        True

        TEST: a value with OR operation and a single value
        >>> comp1 = CPEComponent1_1('xp!vista')
        >>> comp2 = CPEComponent1_1('xp')
        >>> comp1 in comp2
        False

        TEST: an empty value and single value
        >>> comp1 = CPEComponent1_1('xp')
        >>> comp2 = CPEComponent1_1('')
        >>> comp1 in comp2
        True

        TEST: an empty value and single value
        >>> comp1 = CPEComponent1_1('~xp')
        >>> comp2 = CPEComponent1_1('vista')
        >>> comp1 in comp2
        True
        """

        dataset = self._data
        dataitem = item._data

        # len(self) == 0
        if ((self == item) or (dataset is CPEComponent.UNDEFINED_VALUE)):
            return True

        # len(self) == 1
        if len(dataset) == 1:
            valset = dataset[0]
            if ((valset == CPEComponent.EMPTY_VALUE) or
               (valset != dataitem and
               self._is_negated != item._is_negated)):
                return True
            else:
                return False

        # len(self) > 1 (OR operation)
        eqNegated = self._is_negated == item._is_negated
        for elem in dataset:
            if [elem] == dataitem and eqNegated:
                return True

        return False

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

        if CPEComponent._isAnyValue(comp_str):
            if comp_str == CPEComponent.EMPTY_VALUE:
                self._data = [comp_str]
            else:
                self._data = None
            self._is_negated = False
        else:
            # Check the component value

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

            # Component value is correct
            self._data = comp_str.replace('~', '').split('!')
            self._is_negated = comp_str.startswith('~')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
