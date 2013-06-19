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

from cpecomp_single import CPEComponentSingle
from cpecomp_undefined import CPEComponentUndefined
from cpecomp_empty import CPEComponentEmpty

import re


class CPEComponent1_1(CPEComponentSingle):
    """
    Represents a component of version 1.1 of CPE specification.

    TEST: simple value
    >>> value = "microsoft"
    >>> comp = CPEComponent1_1(value, CPEComponentSingle.ATT_VENDOR)
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Characters of version 1.1 of CPE name to convert
    # to standard value (WFN value)
    NON_STANDARD_VALUES = [".", "-", ",", "(", ")", "@", "#"]

    # Logical values in string format
    VALUE_UNDEFINED = None
    VALUE_EMPTY = ""

    ####################
    #  OBJECT METHODS  #
    ####################

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        Comparatives in name matching of version 1.1 of CPE:

        c = self._standard_value
        d = item._standard_value

        IF c is empty THEN match True.
        ELSE IF c is a singleton AND c = d THEN match True.
        ELSE IF c has form ~v AND v != d THEN match True.
        ELSE IF c has form v1!v2!..!vn AND v = d for some v THEN match True.
        ENDIF.

        INPUT:
            - item: component to find in self
        OUTPUT:
            - True if item is included in set of self

        TEST: two different simple values
        >>> comp1 = CPEComponent1_1('5.0', CPEComponentSingle.ATT_VERSION)
        >>> comp2 = CPEComponent1_1('9.0', CPEComponentSingle.ATT_VERSION)
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

    def __init__(self, comp_str, comp_att):
        """
        Store the value of component.

        INPUT:
            - comp_str: value of component value
            - comp_att: attribute associated with component value
        OUPUT:
            - None
        EXCEPTIONS:
            - ValueError: incorrect value of component
        """

        return super(CPEComponent1_1, self).__init__(comp_str, comp_att)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        value = self.get_value()
        txt = ""
        if self._is_negated:
            value = value.replace("~", "")
            txt = "NOT "
        txt += "CPEComponent1_1(%s)" % value

        return txt

    def __str__(self):
        """
        Returns a human-readable representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return super(CPEComponent1_1, self).__str__()

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value).

        INPUT:
            - None
        OUTPUT:
            - Decoded encoded value of component to WFN value

        TEST: OR operator
        >>> val ='microsoft'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSingle.ATT_VENDOR)
        >>> comp1._decode()
        >>> comp1._standard_value
        ['microsoft']
        """

        s = self._encoded_value
        elements = s.replace('~', '').split('!')
        dec_elements = []

        for elem in elements:
            result = ""
            idx = 0
            while (idx < len(elem)):
                # Get the idx'th character of s
                c = elem[idx]

                if (c in CPEComponent1_1.NON_STANDARD_VALUES):
                    # Escape character
                    result = "%s\\%s" % (result, c)
                else:
                    # Do nothing
                    result = "%s%s" % (result, c)

                idx += 1
            dec_elements.append(result)

        self._standard_value = dec_elements

    def _is_valid_edition(self):
        """
        Return True if the value of component in attribute "edition" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        return super(CPEComponent1_1, self)._is_valid_edition()

    def _is_valid_language(self):
        """
        Return True if the value of component in attribute "language" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        return super(CPEComponent1_1, self)._is_valid_language()

    def _is_valid_part(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value of component is valid, False otherwise
        """

        return super(CPEComponent1_1, self)._is_valid_part()

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        comp_str = self._encoded_value

        # Compilation of regular expression associated with value of component
        string = "\w\.\-,\(\)@\#"
        negate_pattern = "~[%s]+" % string
        not_negate_pattern = "[%s]+(![%s]+)*" % (string, string)
        value_pattern = "^((%s)|(%s))$" % (negate_pattern, not_negate_pattern)
        value_rxc = re.compile(value_pattern)

        # Validation of value
        return value_rxc.match(comp_str) is not None

    def _parse(self, comp_att):
        """
        Check if the value of component is correct
        in the attribute "comp_att".

        INPUT:
            - comp_att: attribute associated with value of component
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: incorrect value of component
        """

        super(CPEComponent1_1, self)._parse(comp_att)

    def as_fs(self):
        r"""
        Returns the value of compoment encoded as formatted string.

        Inspect each character in value of component.
        Certain nonalpha characters pass thru without escaping
        into the result, but most retain escaping.

        INPUT:
            - None
        OUTPUT:
            - Formatted string

        - TEST
        >>> val = 'xp!vista'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSingle.ATT_VERSION)
        >>> comp1.as_fs()
        'xp\\!vista'
        """

        # Escape component separator
        separator = "\\!"
        result = ""

        for s in self._standard_value:
            idx = 0
            while (idx < len(s)):
                c = s[idx]  # get the idx'th character of s
                if c != "\\":
                    # unquoted characters pass thru unharmed
                    result = "%s%s" % (result, c)
                else:
                    # Escaped characters are examined
                    nextchr = s[idx + 1]

                    if ((nextchr == ".") or (nextchr == "-")
                       or (nextchr == "_")):
                        # the period, hyphen and underscore pass unharmed
                        result = "%s%s" % (result, nextchr)
                        idx += 1
                    else:
                        # all others retain escaping
                        result = "%s\\%s" % (result, nextchr)
                        idx += 2
                        continue
                idx += 1
            result += separator

        return result[0:len(result)-len(separator)]

    def as_uri_2_3(self):
        """
        Returns the value of compoment encoded as URI string.

        Scans an input string s and applies the following transformations:
        - Pass alphanumeric characters thru untouched
        - Percent-encode quoted non-alphanumerics as needed
        - Unquoted special characters are mapped to their special forms.

        INPUT:
            - None
        OUTPUT:
            - URI string

        - TEST
        >>> val = '#nvidi@'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSingle.ATT_VENDOR)
        >>> comp1.as_uri_2_3()
        '%23nvidi%40'
        """

        separator = CPEComponentSingle._pct_encode_uri("!")
        result = ""

        for s in self._standard_value:
            idx = 0
            while (idx < len(s)):
                thischar = s[idx]  # get the idx'th character of s

                # alphanumerics (incl. underscore) pass untouched
                if (CPEComponentSingle._is_alphanum(thischar)):
                    result += thischar
                    idx += 1
                    continue

                # escape character
                if (thischar == "\\"):
                    idx += 1
                    nxtchar = s[idx]
                    result += CPEComponentSingle._pct_encode_uri(nxtchar)
                    idx += 1
                    continue

                idx += 1

            result += separator

        return result[0:len(result)-len(separator)]

    def as_wfn(self):
        r"""
        Returns the value of compoment encoded as Well-Formed Name (WFN)
        string.

        INPUT:
            - None
        OUTPUT:
            - WFN string

        - TEST
        >>> val = 'xp!vista'
        >>> comp1 = CPEComponent1_1(val, CPEComponentSingle.ATT_VERSION)
        >>> comp1.as_wfn()
        'xp\\!vista'
        """

        # Escape component separator
        separator = "\\!"
        result = ""

        for s in self._standard_value:
            result = "%s%s%s" % (result, s, separator)

        return result[0:len(result)-len(separator)]

    def get_value(self):
        """
        Returns the encoded value of component.

        TEST:
        >>> value = "hp"
        >>> att = CPEComponentSingle.ATT_VENDOR
        >>> comp1 = CPEComponent1_1(value, att)
        >>> comp1.get_value()
        'hp'
        """

        return super(CPEComponent1_1, self).get_value()

    def set_value(self, comp_str, comp_att):
        """
        Set the value of component. By default, the component has a single
        value.

        INPUT:
            - comp_att: attribute associated with value of component
        OUPUT:
            - None
        EXCEPTIONS:
            - ValueError: incorrect value of component

        - TEST
        >>> val = 'xp!vista'
        >>> val2 = 'sp2'
        >>> att = CPEComponentSingle.ATT_VERSION
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
    doctest.testfile("tests/testfile_cpecomp1_1.txt")
