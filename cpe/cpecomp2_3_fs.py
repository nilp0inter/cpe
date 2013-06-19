#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification
with formatted string style.

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
from cpecomp2_3_wfn import CPEComponent2_3_WFN
from cpecomp_single import CPEComponentSingle

import re


class CPEComponent2_3_FS(CPEComponent2_3):
    """
    Represents a component of version 2.3 of CPE specification with URI style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Logical values in string format
    VALUE_ANY = "*"
    VALUE_NA = "-"

    # Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = CPEComponent2_3_WFN.WILDCARD_MULTI
    # Constant associated with wildcard to indicate a character
    WILDCARD_ONE = CPEComponent2_3_WFN.WILDCARD_ONE

    # Separator of language parts: language and region
    SEPARATOR_LANG = "-"

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

        return super(CPEComponent2_3_FS, self).__init__(comp_str, comp_att)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "CPEComponent2_3_FS(%s)" % self.get_value()

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return super(CPEComponent2_3_FS, self).__str__()

    def _decode(self):
        """
        Convert the characters of string s to standard value (WFN value).
        Inspect each character in value of component. Copy quoted characters,
        with their escaping, into the result. Look for unquoted non
        alphanumerics and if not "*" or "?", add escaping.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: Invalid character in value of component
        """

        result = ""
        idx = 0
        s = self._encoded_value
        embedded = False

        while (idx < len(s)):
            c = s[idx]  # get the idx'th character of s
            errmsg = "Invalid character '%s'" % c
            if (CPEComponentSingle._is_alphanum(c)):
                # Alphanumeric characters pass untouched
                result = "%s%s" % (result, c)
                idx += 1
                embedded = True
                continue

            if c == "\\":
                # Anything quoted in the bound string stays quoted
                # in the unbound string.
                result = "%s%s" % (result, s[idx: idx + 2])
                idx += 2
                embedded = True
                continue

            if (c == CPEComponent2_3_FS.WILDCARD_MULTI):
                # An unquoted asterisk must appear at the beginning or
                # end of the string.
                if (idx == 0) or (idx == (len(s) - 1)):
                    result = "%s%s" % (result, c)
                    idx += 1
                    embedded = True
                    continue
                else:
                    raise ValueError(errmsg)

            if (c == CPEComponent2_3_FS.WILDCARD_ONE):
                # An unquoted question mark must appear at the beginning or
                # end of the string, or in a leading or trailing sequence:
                # - ? legal at beginning or end
                # - embedded is false, so must be preceded by ?
                # - embedded is true, so must be followed by ?
                if (((idx == 0) or (idx == (len(s) - 1))) or
                   ((not embedded) and (s[idx - 1] == CPEComponent2_3_FS.WILDCARD_ONE)) or
                   (embedded and (s[idx + 1] == CPEComponent2_3_FS.WILDCARD_ONE))):
                    result = "%s%s" % (result, c)
                    idx += 1
                    embedded = False
                    continue
                else:
                    raise ValueError(errmsg)

            # all other characters must be quoted
            result = "%s\\%s" % (result, c)
            idx += 1
            embedded = True

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

        return super(CPEComponent2_3_FS, self)._is_valid_edition()

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        comp_str = self._standard_value[0]

        # Compilation of regular expression associated with value of CPE part
        logical = "(\%s|%s)" % (CPEComponent2_3_FS.VALUE_ANY,
                                CPEComponent2_3_FS.VALUE_NA)
        quest = "\%s" % CPEComponent2_3_FS.WILDCARD_ONE
        asterisk = "\%s" % CPEComponent2_3_FS.WILDCARD_MULTI
        unreserved = "\w|\.|\-"
        special = "%s|%s" % (quest, asterisk)
        spec_chrs = "%s+|%s" % (quest, asterisk)
        punc = "\!|\"|\;|\#|\$|\%|\&|\'|\(|\)|\+|\,|\/|\:|\<|\=|\>|\@|\[|\]|\^|\`|\{|\||\}|\~|\-"
        quoted = r"\\(\\" + "|%s|%s)" % (special, punc)
        avstring = "%s|%s" % (unreserved, quoted)
        value_string_pattern = "^((%s+|%s*(%s)+|%s(%s)+)(%s)?|%s)$" % (quest,
                                                                       quest, avstring,
                                                                       asterisk, avstring,
                                                                       spec_chrs,
                                                                       logical)

        part_value_rxc = re.compile(value_string_pattern)

        # Validation of value
        return part_value_rxc.match(comp_str) is not None

    def get_value(self):
        """
        Returns the encoded value of component.
        """

        return super(CPEComponent2_3_FS, self).get_value()

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

        super(CPEComponent2_3_FS, self).set_value(comp_str, comp_att)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpecomp2_3_fs.txt")
