#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 1.1 of CPE (Common Platform Enumeration) specification.

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
from .cpecomp_undefined import CPEComponentUndefined
from .cpecomp_empty import CPEComponentEmpty

import re


class CPEComponent1_1(CPEComponentSimple):
    """
    Represents a component of version 1.1 of CPE specification.

    TEST: simple value

    >>> value = "microsoft"
    >>> comp = CPEComponent1_1(value, CPEComponentSimple.ATT_VENDOR)
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Escape component separator
    _ESCAPE_SEPARATOR = "\\!"

    #: Pattern used in regular expression of the value of a component
    _STRING = "\w\.\-,\(\)@\#"

    #: Separator of components of CPE name with URI style
    SEPARATOR_COMP = ":"

    #: Characters of version 1.1 of CPE name to convert
    #: to standard value (WFN value)
    NON_STANDARD_VALUES = [".", "-", ",", "(", ")", "@", "#"]

    # Logical values in string format

    #: Logical value associated with a undefined component of CPE Name
    VALUE_UNDEFINED = None

    #: Logical value associated with a component without value set
    VALUE_EMPTY = ""

    ####################
    #  OBJECT METHODS  #
    ####################

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        Comparatives in name matching of version 1.1 of CPE:

        | c = self._standard_value
        | d = item._standard_value

        | IF c is empty THEN match True.
        | ELSE IF c is a singleton AND c = d THEN match True.
        | ELSE IF c has form ~v AND v != d THEN match True.
        | ELSE IF c has form v1!v2!..!vn AND v = d for some v THEN match True.
        | ENDIF.

        :param CPEComponent item: component to find in self
        :returns: True if item is included in set of self
        :rtype: boolean

        TEST: two different simple values

        >>> comp1 = CPEComponent1_1('5.0', CPEComponentSimple.ATT_VERSION)
        >>> comp2 = CPEComponent1_1('9.0', CPEComponentSimple.ATT_VERSION)
        >>> comp1 in comp2
        False
        """

        if ((self == item) or
           isinstance(self, CPEComponentUndefined) or
           isinstance(self, CPEComponentEmpty)):

            return True

        dataset = self._standard_value
        dataitem = item._standard_value

        # len(self) == 1, check NOT operation
        if len(dataset) == 1:
            valset = dataset[0]
            if ((valset != dataitem) and
               self._is_negated and
               (not item._is_negated) and
               len(dataitem) == 1):

                return True
            else:
                return False

        # len(self) > 1, check OR operation
        eqNegated = self._is_negated == item._is_negated
        for elem in dataset:
            if ([elem] == dataitem) and eqNegated:
                return True

        return False

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        :returns: Representation of CPE component as string
        :rtype: string
        """

        value = self.get_value()
        result = []

        if self._is_negated:
            value = value.replace("~", "")
            result.append("NOT ")

        result.append(self.__class__.__name__)
        result.append("(")
        result.append(value)
        result.append(")")

        return "".join(result)

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value).
        """

        s = self._encoded_value
        elements = s.replace('~', '').split('!')
        dec_elements = []

        for elem in elements:
            result = []
            idx = 0
            while (idx < len(elem)):
                # Get the idx'th character of s
                c = elem[idx]

                if (c in CPEComponent1_1.NON_STANDARD_VALUES):
                    # Escape character
                    result.append("\\")
                    result.append(c)
                else:
                    # Do nothing
                    result.append(c)

                idx += 1
            dec_elements.append("".join(result))

        self._standard_value = dec_elements

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._encoded_value

        value_pattern = []
        value_pattern.append("^((")
        value_pattern.append("~[")
        value_pattern.append(CPEComponent1_1._STRING)
        value_pattern.append("]+")
        value_pattern.append(")|(")
        value_pattern.append("[")
        value_pattern.append(CPEComponent1_1._STRING)
        value_pattern.append("]+(![")
        value_pattern.append(CPEComponent1_1._STRING)
        value_pattern.append("]+)*")
        value_pattern.append("))$")

        value_rxc = re.compile("".join(value_pattern))
        return value_rxc.match(comp_str) is not None

    def as_fs(self):
        r"""
        Returns the value of compoment encoded as formatted string.

        Inspect each character in value of component.
        Certain nonalpha characters pass thru without escaping
        into the result, but most retain escaping.

        :returns: Formatted string associated with the component
        :rtype: string

        TEST:

        >>> val = 'xp!vista'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSimple.ATT_VERSION)
        >>> comp1.as_fs()
        'xp\\!vista'
        """

        result = []

        for s in self._standard_value:
            idx = 0
            while (idx < len(s)):
                c = s[idx]  # get the idx'th character of s
                if c != "\\":
                    # unquoted characters pass thru unharmed
                    result.append(c)
                else:
                    # Escaped characters are examined
                    nextchr = s[idx + 1]

                    if ((nextchr == ".") or (nextchr == "-")
                       or (nextchr == "_")):
                        # the period, hyphen and underscore pass unharmed
                        result.append(nextchr)
                        idx += 1
                    else:
                        # all others retain escaping
                        result.append("\\")
                        result.append(nextchr)
                        idx += 2
                        continue
                idx += 1
            result.append(CPEComponent1_1._ESCAPE_SEPARATOR)

        return "".join(result[0:-1])

    def as_uri_2_3(self):
        """
        Returns the value of compoment encoded as URI string.

        Scans an input string s and applies the following transformations:

        - Pass alphanumeric characters thru untouched
        - Percent-encode quoted non-alphanumerics as needed
        - Unquoted special characters are mapped to their special forms.

        :returns: URI string
        :rtype: string

        TEST:

        >>> val = '#nvidi@'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSimple.ATT_VENDOR)
        >>> comp1.as_uri_2_3()
        '%23nvidi%40'
        """

        separator = CPEComponentSimple._pct_encode_uri("!")
        result = []

        for s in self._standard_value:
            idx = 0
            while (idx < len(s)):
                thischar = s[idx]  # get the idx'th character of s

                # alphanumerics (incl. underscore) pass untouched
                if (CPEComponentSimple._is_alphanum(thischar)):
                    result.append(thischar)
                    idx += 1
                    continue

                # escape character
                if (thischar == "\\"):
                    idx += 1
                    nxtchar = s[idx]
                    result.append(CPEComponentSimple._pct_encode_uri(nxtchar))
                    idx += 1
                    continue

                idx += 1

            result.append(separator)

        return "".join(result[0:-1])

    def as_wfn(self):
        r"""
        Returns the value of compoment encoded as Well-Formed Name (WFN)
        string.

        :returns: WFN string
        :rtype: string

        TEST:

        >>> val = 'xp!vista'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSimple.ATT_VERSION)
        >>> comp1.as_wfn()
        'xp\\!vista'
        """

        result = []

        for s in self._standard_value:
            result.append(s)
            result.append(CPEComponent1_1._ESCAPE_SEPARATOR)

        return "".join(result[0:-1])

    def set_value(self, comp_str, comp_att):
        """
        Set the value of component. By default, the component has a simple
        value.

        :param string comp_att: attribute associated with value of component
        :returns: None
        :exception: ValueError - incorrect value of component

        TEST:

        >>> val = 'xp!vista'
        >>> val2 = 'sp2'
        >>> att = CPEComponentSimple.ATT_VERSION
        >>> comp1 = CPEComponent1_1(val, att)
        >>> comp1.set_value(val2, att)
        >>> comp1.get_value()
        'sp2'
        """

        super(CPEComponent1_1, self).set_value(comp_str, comp_att)
        self._is_negated = comp_str.startswith('~')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("../tests/testfile_cpecomp1_1.txt")
