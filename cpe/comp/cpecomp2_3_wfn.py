#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification with
Well-Formed Name (WFN) style.

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

from .cpecomp2_3 import CPEComponent2_3

import re


class CPEComponent2_3_WFN(CPEComponent2_3):
    """
    Represents a component of version 2.3 of CPE specification with WFN style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Patterns used to check the value of component
    _ESCAPE = r"\\"
    _PUNC_NO_DASH = "\!|\"|\;|\#|\$|\%|\&|\'|\(|\)|\+|\,|\.|\/|\:|\<|\=|\>|\@|\[|\]|\^|\`|\{|\||\}|\~"

    #: Separator of components of CPE name with URI style
    SEPARATOR_COMP = ", "

    #: Separator of attribute and value in pairs of component
    SEPARATOR_PAIR = "="

    #: Separator of language parts: language and region
    SEPARATOR_LANG = r"\-"

    # Logical values in string format

    #: Logical value associated with a any value logical value
    VALUE_ANY = "ANY"

    #: Logical value associated with a not applicable logical value
    VALUE_NA = "NA"

    #: Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = "*"
    #: Constant associated with wildcard to indicate a character
    WILDCARD_ONE = "?"

    ###############
    #  VARIABLES  #
    ###############

    _spec1 = "\{0}".format(WILDCARD_ONE)
    _spec2 = "\{0}".format(WILDCARD_MULTI)
    _spec_chrs = "{0}+|{1}".format(_spec1, _spec2)
    _special = "{0}|{1}".format(_spec1, _spec2)
    _punc_w_dash = "{0}|-".format(_PUNC_NO_DASH)
    _quoted1 = "{0}({1}|{2}|{3})".format(_ESCAPE, _ESCAPE, _special,
                                         _PUNC_NO_DASH)
    _quoted2 = "{0}({1}|{2}|{3})".format(_ESCAPE, _ESCAPE,
                                         _special, _punc_w_dash)
    _body1 = "\w|{0}".format(_quoted1)
    _body2 = "\w|{0}".format(_quoted2)
    _body = "(({0})({1})*)|{2}({3})+".format(_body1, _body2, _body2, _body2)
    _avstring_pattern = "^((({0})|(({1})({2})*))({3})?)$".format(_body,
                                                                 _spec_chrs,
                                                                 _body2,
                                                                 _spec_chrs)

    _value_rxc = re.compile(_avstring_pattern)

    ####################
    #  OBJECT METHODS  #
    ####################

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value) is
        not necessary in this case because the internal value is in WFN
        already.
        """

        pass

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._standard_value
        return CPEComponent2_3_WFN._value_rxc.match(comp_str) is not None

    def get_value(self):
        """
        Returns the encoded value of component.

        :returns: encoded value of component
        :rtype: string
        """

        # Add double quotes
        return '"{0}"'.format(super(CPEComponent2_3_WFN, self).get_value())

    def set_value(self, comp_str, comp_att):
        """
        Set the value of component.

        :param string comp_str: value of component
        :param string comp_att: attribute associated with comp_str
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        # Del double quotes of value
        str = comp_str[1:-1]
        self._standard_value = str

        # Parse the value
        super(CPEComponent2_3_WFN, self).set_value(str, comp_att)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("../tests/testfile_cpecomp2_3_wfn.txt")
