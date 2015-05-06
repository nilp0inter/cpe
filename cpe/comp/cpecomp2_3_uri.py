#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification
with Universal Resource Identifier (URI) style.

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

import re


class CPEComponent2_3_URI(CPEComponent2_3):
    """
    Represents a component of version 2.3 of CPE specification with URI style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Patterns used to check the value of component
    _PCT_ENCODED = "%21|%22|%23|%24|%25|%26|%27|%28|%29|%2a|%2b|%2c|%2f|%3a|%3b|%3c|%3d|%3e|%3f|%40|%5b|%5c|%5d|%5e|%60|%7b|%7c|%7d|%7e"
    _SPEC_CHRS = "((%01)+|%02)"
    _UNRESERVED = "[\w\-\.]"

    #: Separator of components of CPE name with URI style
    SEPARATOR_COMP = ":"

    #: Separator of language parts: language and region
    SEPARATOR_LANG = "-"

    #: Separator of edition part components in CPE uri
    SEPARATOR_PACKED_EDITION = "~"

    # Logical values in string format

    #: Logical value associated with a any value logical value
    VALUE_ANY = ""

    #: Logical value associated with a not applicable logical value
    VALUE_NA = "-"

    #: Logical value associated with a component without value
    VALUE_EMPTY = ""

    #: Logical value associated with a undefined component
    VALUE_UNDEFINED = None

    #: Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = "%02"
    #: Constant associated with wildcard to indicate a character
    WILDCARD_ONE = "%01"

    ###############
    #  VARIABLES  #
    ###############

    # Variable used to check the value of component
    _str_w_special = "({0}?({1}|{2})+{3}?)".format(_SPEC_CHRS, _UNRESERVED,
                                                   _PCT_ENCODED, _SPEC_CHRS)
    _str_wo_special = "({0}|{1})*".format(_UNRESERVED, _PCT_ENCODED)
    _string = "({0}|{1})".format(_str_wo_special, _str_w_special)

    # Compilation of regular expression associated with value of component
    _value_pattern = "^{0}$".format(_string)
    _value_rxc = re.compile(_value_pattern)

    #: Characters to convert to percent-encoded characters
    char_to_pce = {
        '!': "%21",
        '"': "%22",
        '#': "%23",
        '$': "%24",
        '%': "%25",
        '&': "%26",
        '\'': "%27",
        '(': "%28",
        ')': "%29",
        '*': "%2a",
        '+': "%2b",
        ',': "%2c",
        '/': "%2f",
        ':': "%3a",
        ';': "%3b",
        '<': "%3c",
        '=': "%3d",
        '>': "%3e",
        '?': "%3f",
        '@': "%40",
        '[': "%5b",
        '\\': "%5c",
        ']': "%5d",
        '^': "%5e",
        '`': "%60",
        '{': "%7b",
        '|': "%7c",
        '}': "%7d",
        '~': "%7e"}

    #: Percent-encoded characters to decode
    pce_char_to_decode = {
        "%21": '\\!',
        "%22": '\\\"',
        "%23": '\\#',
        "%24": '\\$',
        "%25": '\\%',
        "%26": '\\&',
        "%27": '\\\'',
        "%28": '\\(',
        "%29": '\\)',
        "%2a": '\\*',
        "%2b": '\\+',
        "%2c": '\\,',
        "%2f": '\\/',
        "%3a": '\\:',
        "%3b": '\\;',
        "%3c": '\\<',
        "%3d": '\\=',
        "%3e": '\\>',
        "%3f": '\\?',
        "%40": '\\@',
        "%5b": '\\[',
        "%5c": '\\\\',
        "%5d": '\\]',
        "%5e": '\\^',
        "%60": '\\`',
        "%7b": '\\{',
        "%7c": '\\|',
        "%7d": '\\}',
        "%7e": '\\~'}

    ####################
    #  OBJECT METHODS  #
    ####################

    def _decode(self):
        """
        Convert the characters of character in value of component to standard
        value (WFN value).
        This function scans the value of component and returns a copy
        with all percent-encoded characters decoded.

        :exception: ValueError - invalid character in value of component
        """

        result = []
        idx = 0
        s = self._encoded_value
        embedded = False

        errmsg = []
        errmsg.append("Invalid value: ")

        while (idx < len(s)):
            errmsg.append(s)
            errmsg_str = "".join(errmsg)

            # Get the idx'th character of s
            c = s[idx]

            # Deal with dot, hyphen and tilde: decode with quoting
            if ((c == '.') or (c == '-') or (c == '~')):
                result.append("\\")
                result.append(c)
                idx += 1
                embedded = True  # a non-%01 encountered
                continue

            if (c != '%'):
                result.append(c)
                idx += 1
                embedded = True  # a non-%01 encountered
                continue

            # we get here if we have a substring starting w/ '%'
            form = s[idx: idx + 3]  # get the three-char sequence

            if form == CPEComponent2_3_URI.WILDCARD_ONE:
                # If %01 legal at beginning or end
                # embedded is false, so must be preceded by %01
                # embedded is true, so must be followed by %01
                if (((idx == 0) or (idx == (len(s)-3))) or
                    ((not embedded) and (s[idx - 3:idx] == CPEComponent2_3_URI.WILDCARD_ONE)) or
                    (embedded and (len(s) >= idx + 6) and (s[idx + 3:idx + 6] == CPEComponent2_3_URI.WILDCARD_ONE))):

                    # A percent-encoded question mark is found
                    # at the beginning or the end of the string,
                    # or embedded in sequence as required.
                    # Decode to unquoted form.
                    result.append(CPEComponent2_3_WFN.WILDCARD_ONE)
                    idx += 3
                    continue
                else:
                    raise ValueError(errmsg_str)

            elif form == CPEComponent2_3_URI.WILDCARD_MULTI:
                if ((idx == 0) or (idx == (len(s) - 3))):
                    # Percent-encoded asterisk is at the beginning
                    # or the end of the string, as required.
                    # Decode to unquoted form.
                    result.append(CPEComponent2_3_WFN.WILDCARD_MULTI)
                else:
                    raise ValueError(errmsg_str)

            elif form in CPEComponent2_3_URI.pce_char_to_decode.keys():
                value = CPEComponent2_3_URI.pce_char_to_decode[form]
                result.append(value)

            else:
                errmsg.append("Invalid percent-encoded character: ")
                errmsg.append(s)
                raise ValueError("".join(errmsg))

            idx += 3
            embedded = True  # a non-%01 encountered.

        self._standard_value = "".join(result)

    def _is_valid_edition(self):
        """
        Return True if the input value of attribute "edition" is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._standard_value[0]

        packed = []
        packed.append("(")
        packed.append(CPEComponent2_3_URI.SEPARATOR_PACKED_EDITION)
        packed.append(CPEComponent2_3_URI._string)
        packed.append("){5}")

        value_pattern = []
        value_pattern.append("^(")
        value_pattern.append(CPEComponent2_3_URI._string)
        value_pattern.append("|")
        value_pattern.append("".join(packed))
        value_pattern.append(")$")

        value_rxc = re.compile("".join(value_pattern))
        return value_rxc.match(comp_str) is not None

    def _is_valid_value(self):
        """
        Return True if the input value CPE name attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._standard_value[0]
        return CPEComponent2_3_URI._value_rxc.match(comp_str) is not None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("../tests/testfile_cpecomp2_3_uri.txt")
