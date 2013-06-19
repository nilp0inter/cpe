#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification
with Universal Resource Identifier (URI) style.

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

import re


class CPEComponent2_3_URI(CPEComponent2_3):
    """
    Represents a component of version 2.3 of CPE specification with URI style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Logical values in string format
    VALUE_ANY = ""
    VALUE_NA = "-"
    VALUE_EMPTY = ""
    VALUE_UNDEFINED = None

    # Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = "%02"
    # Constant associated with wildcard to indicate a character
    WILDCARD_ONE = "%01"

    # Percent-encoded characters to decode
    DECODE_DICT = {
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

    # Characters to convert to percent-encoded characters
    PCE_DICT = {
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

    PCT_ENCODED = "%21|%22|%23|%24|%25|%26|%27|%28|%29"
    PCT_ENCODED += "|%2a|%2b|%2c|%2f"
    PCT_ENCODED += "|%3a|%3b|%3c|%3d|%3e|%3f"
    PCT_ENCODED += "|%40|%5b|%5c|%5d|%5e"
    PCT_ENCODED += "|%60|%7b|%7c|%7d|%7e"
    UNRESERVED = "[\w\-\.]"
    SPEC_CHRS = "((%01)+|%02)"
    STR_W_SPECIAL = "(%s?(%s|%s)+%s?)" % (SPEC_CHRS, UNRESERVED,
                                          PCT_ENCODED, SPEC_CHRS)
    STR_WO_SPECIAL = "(%s|%s)*" % (UNRESERVED, PCT_ENCODED)
    STRING = "(%s|%s)" % (STR_WO_SPECIAL, STR_W_SPECIAL)

    # Separator of edition part components in CPE uri
    PACKED_EDITION_SEPARATOR = "~"

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

        super(CPEComponent2_3_URI, self).__init__(comp_str, comp_att)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "CPEComponent2_3_URI(%s)" % self.get_value()

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return super(CPEComponent2_3_URI, self).__str__()

    def _decode(self):
        """
        Convert the characters of character in value of component to standard
        value (WFN value).
        This function scans the value of component and returns a copy
        with all percent-encoded characters decoded.

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
            # Get the idx'th character of s
            c = s[idx]

            # Deal with dot, hyphen and tilde: decode with quoting
            if ((c == '.') or (c == '-') or (c == '~')):
                result = "%s\\%s" % (result, c)
                idx += 1
                embedded = True  # a non-%01 encountered
                continue

            if (c != '%'):
                result = "%s%s" % (result, c)
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
                   ((not embedded) and (s[idx - 3, idx - 1] == CPEComponent2_3_URI.WILDCARD_MULTI)) or
                   (embedded and (len(s) >= idx + 6) and (s[idx + 3, idx + 5] == CPEComponent2_3_URI.PCE_ASTERISK))):

                    # A percent-encoded question mark is found
                    # at the beginning or the end of the string,
                    # or embedded in sequence as required.
                    # Decode to unquoted form.
                    result = "%s%s" % (result,
                                       CPEComponent2_3_WFN.WILDCARD_ONE)
                    idx += 3
                    continue
                else:
                    errmsg = "Invalid value '%s'" % s
                    raise ValueError(errmsg)

            elif form == CPEComponent2_3_URI.WILDCARD_MULTI:
                if ((idx == 0) or (idx == (len(s) - 3))):
                    # Percent-encoded asterisk is at the beginning
                    # or the end of the string, as required.
                    # Decode to unquoted form.
                    result = "%s%s" % (result,
                                       CPEComponent2_3_WFN.WILDCARD_MULTI)
                else:
                    errmsg = "Invalid value '%s'" % s
                    raise ValueError(errmsg)

            elif form in CPEComponent2_3_URI.DECODE_DICT.keys():
                value = CPEComponent2_3_URI.DECODE_DICT[form]
                result = "%s%s" % (result, value)

            else:
                errmsg = "Invalid percent-encoded character '%s'" % s
                raise ValueError(errmsg)

            idx += 3
            embedded = True  # a non-%01 encountered.

        self._standard_value = result

    def _is_valid_edition(self):
        """
        Return True if the input value of attribute "edition" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        comp_str = self._standard_value[0]

        # Compilation of regular expression associated with value of CPE part
        packed = "(%s%s){5}" % (CPEComponent2_3_URI.PACKED_EDITION_SEPARATOR,
                                CPEComponent2_3_URI.STRING)

        value_pattern = "^(%s|%s)$" % (CPEComponent2_3_URI.STRING, packed)
        value_rxc = re.compile(value_pattern)

        # Validation of value
        return value_rxc.match(comp_str) is not None

    def _is_valid_value(self):
        """
        Return True if the input value CPE name attribute is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        comp_str = self._standard_value[0]

        # Compilation of regular expression associated with value of CPE part
        value_pattern = "^%s$" % CPEComponent2_3_URI.STRING
        value_rxc = re.compile(value_pattern)

        # Validation of value
        return value_rxc.match(comp_str) is not None

    def get_value(self):
        """
        Returns the encoded value of component.
        """

        return super(CPEComponent2_3_URI, self).get_value()

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

        super(CPEComponent2_3_URI, self).set_value(comp_str, comp_att)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpecomp2_3_uri.txt")
