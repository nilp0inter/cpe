#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification
with formatted string style.

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
from .cpecomp2_3_wfn import CPEComponent2_3_WFN
from .cpecomp_simple import CPEComponentSimple

import re


class CPEComponent2_3_FS(CPEComponent2_3):
    """
    Represents a component of version 2.3 of CPE specification with URI style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Patterns used to check the value of component
    _UNRESERVED = "\w|\.|\-"
    _PUNC = "\!|\"|\;|\#|\$|\%|\&|\'|\(|\)|\+|\,|\/|\:|\<|\=|\>|\@|\[|\]|\^|\`|\{|\||\}|\~|\-"

    #: Separator of components of CPE name with URI style
    SEPARATOR_COMP = ":"

    #: Separator of language parts: language and region
    SEPARATOR_LANG = "-"

    # Logical values in string format

    #: Logical value associated with a any value logical value
    VALUE_ANY = "*"

    #: Logical value associated with a not applicable logical value
    VALUE_NA = "-"

    #: Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = CPEComponent2_3_WFN.WILDCARD_MULTI
    #: Constant associated with wildcard to indicate a character
    WILDCARD_ONE = CPEComponent2_3_WFN.WILDCARD_ONE

    ###############
    #  VARIABLES  #
    ###############

    # Compilation of regular expression associated with value of CPE part
    _logical = "(\{0}|{1})".format(VALUE_ANY, VALUE_NA)
    _quest = "\{0}".format(WILDCARD_ONE)
    _asterisk = "\{0}".format(WILDCARD_MULTI)
    _special = "{0}|{1}".format(_quest, _asterisk)
    _spec_chrs = "{0}+|{1}".format(_quest, _asterisk)
    _quoted = r"\\(\\" + "|{0}|{1})".format(_special, _PUNC)
    _avstring = "{0}|{1}".format(_UNRESERVED, _quoted)
    _value_string_pattern = "^(({0}+|{1}*({2})+|{3}({4})+)({5})?|{6})$".format(
        _quest, _quest, _avstring, _asterisk, _avstring, _spec_chrs, _logical)

    _part_value_rxc = re.compile(_value_string_pattern)

    ####################
    #  OBJECT METHODS  #
    ####################

    def _decode(self):
        """
        Convert the characters of string s to standard value (WFN value).
        Inspect each character in value of component. Copy quoted characters,
        with their escaping, into the result. Look for unquoted non
        alphanumerics and if not "*" or "?", add escaping.

        :exception: ValueError - invalid character in value of component
        """

        result = []
        idx = 0
        s = self._encoded_value
        embedded = False

        errmsg = []
        errmsg.append("Invalid character '")

        while (idx < len(s)):
            c = s[idx]  # get the idx'th character of s
            errmsg.append(c)
            errmsg.append("'")
            errmsg_str = "".join(errmsg)

            if (CPEComponentSimple._is_alphanum(c)):
                # Alphanumeric characters pass untouched
                result.append(c)
                idx += 1
                embedded = True
                continue

            if c == "\\":
                # Anything quoted in the bound string stays quoted
                # in the unbound string.
                result.append(s[idx: idx + 2])
                idx += 2
                embedded = True
                continue

            if (c == CPEComponent2_3_FS.WILDCARD_MULTI):
                # An unquoted asterisk must appear at the beginning or
                # end of the string.
                if (idx == 0) or (idx == (len(s) - 1)):
                    result.append(c)
                    idx += 1
                    embedded = True
                    continue
                else:
                    raise ValueError(errmsg_str)

            if (c == CPEComponent2_3_FS.WILDCARD_ONE):
                # An unquoted question mark must appear at the beginning or
                # end of the string, or in a leading or trailing sequence:
                # - ? legal at beginning or end
                # - embedded is false, so must be preceded by ?
                # - embedded is true, so must be followed by ?
                if (((idx == 0) or (idx == (len(s) - 1))) or
                   ((not embedded) and (s[idx - 1] == CPEComponent2_3_FS.WILDCARD_ONE)) or
                   (embedded and (s[idx + 1] == CPEComponent2_3_FS.WILDCARD_ONE))):
                    result.append(c)
                    idx += 1
                    embedded = False
                    continue
                else:
                    raise ValueError(errmsg_str)

            # all other characters must be quoted
            result.append("\\")
            result.append(c)
            idx += 1
            embedded = True

        self._standard_value = "".join(result)

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._standard_value[0]
        return CPEComponent2_3_FS._part_value_rxc.match(comp_str) is not None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("../tests/testfile_cpecomp2_3_fs.txt")
