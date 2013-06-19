#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.2 of CPE (Common Platform Enumeration) specification.

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

import re


class CPEComponent2_2(CPEComponentSingle):
    """
    Represents a component of version 2.2 of CPE specification.

    TEST: simple value
    >>> value = "microsoft"
    >>> comp = CPEComponent2_2(value, CPEComponentSingle.ATT_VENDOR)
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Characters of version 2.2 of CPE name to convert
    # to standard value (WFN value)
    NON_STANDARD_VALUES = [".", "-", "~", "%"]

    # Logical values in string format
    VALUE_UNDEFINED = None
    VALUE_EMPTY = ""

    ####################
    #  OBJECT METHODS  #
    ####################

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.
        """

        return super(CPEComponent2_2, self).__contains__(item)

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

        return super(CPEComponent2_2, self).__init__(comp_str, comp_att)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "CPEComponent2_2(%s)" % self.get_value()

    def __str__(self):
        """
        Returns a human-readable representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return super(CPEComponent2_2, self).__str__()

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value).

        INPUT:
            - None
        OUTPUT:
            - Decoded encoded value of component to WFN value
        """

        result = ""
        idx = 0
        s = self._encoded_value

        while (idx < len(s)):
            # Get the idx'th character of s
            c = s[idx]

            if (c in CPEComponent2_2.NON_STANDARD_VALUES):
                # Escape character
                result = "%s\\%s" % (result, c)
            else:
                # Do nothing
                result = "%s%s" % (result, c)

            idx += 1

        self._standard_value = result

    def _is_valid_edition(self):
        """
        Return True if the value of component in attribute "edition" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        return super(CPEComponent2_2, self)._is_valid_edition()

    def _is_valid_language(self):
        """
        Return True if the value of component in attribute "language" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        return super(CPEComponent2_2, self)._is_valid_language()

    def _is_valid_part(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value of component is valid, False otherwise
        """

        return super(CPEComponent2_2, self)._is_valid_part()

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

        # Compilation of regular expression associated with value of CPE part
        value_pattern = "^([\d\w\._\-~%]+)$"
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

        super(CPEComponent2_2, self)._parse(comp_att)

    def as_fs(self):
        """
        Returns the value of compoment encoded as formatted string.

        Inspect each character in value of component.
        Certain nonalpha characters pass thru without escaping
        into the result, but most retain escaping.

        INPUT:
            - None
        OUTPUT:
            - Formatted string

        - TEST
        >>> val = 'microsoft'
        >>> comp1 = CPEComponent2_2(val, CPEComponentSingle.ATT_VENDOR)
        >>> comp1.as_fs()
        'microsoft'
        """

        return super(CPEComponent2_2, self).as_fs()

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
        >>> val = 'windows_xp'
        >>> comp1 = CPEComponent2_2(val, CPEComponentSingle.ATT_UPDATE)
        >>> comp1.as_uri_2_3()
        'windows_xp'
        """

        return super(CPEComponent2_2, self).as_uri_2_3()

    def as_wfn(self):
        r"""
        Returns the value of compoment encoded as Well-Formed Name (WFN)
        string.

        INPUT:
            - None
        OUTPUT:
            - WFN string

        - TEST
        >>> val = 'linux%7'
        >>> comp1 = CPEComponent2_2(val, CPEComponentSingle.ATT_VERSION)
        >>> comp1.as_wfn()
        'linux\\%7'
        """

        return super(CPEComponent2_2, self).as_wfn()

    def get_value(self):
        """
        Returns the encoded value of component.
        """

        return super(CPEComponent2_2, self).get_value()

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
        >>> val = '%vista~'
        >>> val2 = 'sp2'
        >>> att = CPEComponentSingle.ATT_VERSION
        >>> comp1 = CPEComponent2_2(val, att)
        >>> comp1.set_value(val2, att)
        >>> comp1.get_value()
        'sp2'
        """

        super(CPEComponent2_2, self).set_value(comp_str, comp_att)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpecomp2_2.txt")
