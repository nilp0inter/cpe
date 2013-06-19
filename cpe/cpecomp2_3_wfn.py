#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification with
Well-Formed Name (WFN) style.

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

from cpecomp2_3 import CPEComponent2_3

import re


class CPEComponent2_3_WFN(CPEComponent2_3):
    """
    Represents a component of version 2.3 of CPE specification with WFN style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Logical values in string format
    VALUE_ANY = "ANY"
    VALUE_NA = "NA"

    # Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = "*"
    # Constant associated with wildcard to indicate a character
    WILDCARD_ONE = "?"

    # Separator of language parts: language and region
    SEPARATOR_LANG = r"\-"

    ####################
    #  OBJECT METHODS  #
    ####################

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

        super(CPEComponent2_3_WFN, self).__init__(comp_str, comp_att)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "CPEComponent2_3_WFN(%s)" % self.get_value()

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return super(CPEComponent2_3_WFN, self).__str__()

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value) is
        not necessary in this case because the internal value is in WFN
        already.

        INPUT:
            - None
        OUTPUT:
            - None
        """

        pass

    def _is_valid_edition(self):
        """
        Return True if the value of component in attribute "edition" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        return super(CPEComponent2_3_WFN, self)._is_valid_edition()

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        comp_str = self._standard_value
        # Checks value not equal than a dash
        #if comp_str == ("-") or comp_str == ("\\-"):
        #    return False

        # Compilation of regular expression associated with value of CPE part
        escape = r"\\"
        unreserved = "\w"
        dash = "-"
        spec1 = "\%s" % CPEComponent2_3_WFN.WILDCARD_ONE
        spec2 = "\%s" % CPEComponent2_3_WFN.WILDCARD_MULTI
        spec_chrs = "%s+|%s" % (spec1, spec2)
        special = "%s|%s" % (spec1, spec2)
        punc_no_dash = "\!|\"|\;|\#|\$|\%|\&|\'|\(|\)|\+|\,|\.|"
        punc_no_dash += "\/|\:|\<|\=|\>|\@|\[|\]|\^|\`|\{|\||\}|\~"
        punc_w_dash = "%s|%s" % (punc_no_dash, dash)
        quoted1 = "%s(%s|%s|%s)" % (escape, escape, special, punc_no_dash)
        quoted2 = "%s(%s|%s|%s)" % (escape, escape, special, punc_w_dash)
        body1 = "%s|%s" % (unreserved, quoted1)
        body2 = "%s|%s" % (unreserved, quoted2)
        body = "((%s)(%s)*)|%s(%s)+" % (body1, body2, body2, body2)
        avstring_pattern = "^(((%s)|((%s)(%s)*))(%s)?)$" % (body, spec_chrs,
                                                            body2, spec_chrs)

        value_rxc = re.compile(avstring_pattern)

        # Validation of value
        return value_rxc.match(comp_str) is not None

    def get_value(self):
        """
        Returns the encoded value of component.
        """

        value = super(CPEComponent2_3_WFN, self).get_value()

        # Add double quotes
        return '"%s"' % value

    def set_value(self, comp_str, comp_att):
        """
        Set the value of component.

        INPUT:
            - comp_str: value of component
            - comp_att: attribute associated with comp_str
        OUPUT:
            - None
        EXCEPTIONS:
            - ValueError: incorrect value of component
        """

        # Del double quotes of value
        str = comp_str[1:-1]
        self._standard_value = str

        # Parse the value
        super(CPEComponent2_3_WFN, self).set_value(str, comp_att)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpecomp2_3_wfn.txt")
