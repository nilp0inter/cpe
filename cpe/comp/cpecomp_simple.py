#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the string components
of a CPE name and compare it with others.

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

from .cpecomp import CPEComponent

import re


class CPEComponentSimple(CPEComponent):
    """
    Represents a generic string component of CPE name,
    compatible with the components of all versions of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Pattern to check if a character is a alphanumeric or underscore
    _ALPHANUM_PATTERN = "\w"

    #: Pattern to check the value of language component of CPE name
    _LANGTAG_PATTERN = "^([a-z]{2,3}(-([a-z]{2}|[\d]{3}))?)$"

    #: Pattern to check the value of part component of CPE name
    _PART_PATTERN = "^(h|o|a)$"

    ###############
    #  VARIABLES  #
    ###############

    #: Characters to convert to percent-encoded characters when converts
    #: WFN to URI
    spechar_to_pce = {
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

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _is_alphanum(cls, c):
        """
        Returns True if c is an uppercase letter, a lowercase letter,
        a digit or an underscore, otherwise False.

        :param string c: Character to check
        :returns: True if char is alphanumeric or an underscore,
            False otherwise
        :rtype: boolean

        TEST: a wrong character
        >>> c = "#"
        >>> CPEComponentSimple._is_alphanum(c)
        False
        """

        alphanum_rxc = re.compile(CPEComponentSimple._ALPHANUM_PATTERN)
        return (alphanum_rxc.match(c) is not None)

    @classmethod
    def _pct_encode_uri(cls, c):
        """
        Return the appropriate percent-encoding of character c (URI string).
        Certain characters are returned without encoding.

        :param string c: Character to check
        :returns: Encoded character as URI
        :rtype: string

        TEST:

        >>> c = '.'
        >>> CPEComponentSimple._pct_encode_uri(c)
        '.'

        TEST:

        >>> c = '@'
        >>> CPEComponentSimple._pct_encode_uri(c)
        '%40'
        """

        CPEComponentSimple.spechar_to_pce['-'] = c  # bound without encoding
        CPEComponentSimple.spechar_to_pce['.'] = c  # bound without encoding

        return CPEComponentSimple.spechar_to_pce[c]

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str, comp_att):
        """
        Store the value of component.

        :param string comp_str: value of component value
        :param string comp_att: attribute associated with component value
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        super(CPEComponentSimple, self).__init__(comp_str)
        self._standard_value = self._standard_value
        self.set_value(comp_str, comp_att)

    def __str__(self):
        """
        Returns a human-readable representation of CPE component.

        :returns: Representation of CPE component as string
        :rtype: string
        """

        return self.get_value()

    def _is_valid_edition(self):
        """
        Return True if the value of component in attribute "edition" is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        return self._is_valid_value() is not None

    def _is_valid_language(self):
        """
        Return True if the value of component in attribute "language" is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._encoded_value.lower()
        lang_rxc = re.compile(CPEComponentSimple._LANGTAG_PATTERN)
        return lang_rxc.match(comp_str) is not None

    def _is_valid_part(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        :returns: True if value of component is valid, False otherwise
        :rtype: boolean
        """

        comp_str = self._encoded_value.lower()
        part_rxc = re.compile(CPEComponentSimple._PART_PATTERN)
        return part_rxc.match(comp_str) is not None

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        :exception: NotImplementedError - class method not implemented
        """

        errmsg = "Class method not implemented. Use the method of some child class"
        raise NotImplementedError(errmsg)

    def _parse(self, comp_att):
        """
        Check if the value of component is correct in the attribute "comp_att".

        :param string comp_att: attribute associated with value of component
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        errmsg = "Invalid attribute '{0}'".format(comp_att)

        if not CPEComponent.is_valid_attribute(comp_att):
            raise ValueError(errmsg)

        comp_str = self._encoded_value

        errmsg = "Invalid value of attribute '{0}': {1}".format(
            comp_att, comp_str)

        # Check part (system type) value
        if comp_att == CPEComponentSimple.ATT_PART:
            if not self._is_valid_part():
                raise ValueError(errmsg)

        # Check language value
        elif comp_att == CPEComponentSimple.ATT_LANGUAGE:
            if not self._is_valid_language():
                raise ValueError(errmsg)

        # Check edition value
        elif comp_att == CPEComponentSimple.ATT_EDITION:
            if not self._is_valid_edition():
                raise ValueError(errmsg)

        # Check other type of component value
        elif not self._is_valid_value():
            raise ValueError(errmsg)

    def as_fs(self):
        """
        Returns the value of component encoded as formatted string.

        Inspect each character in value of component.
        Certain nonalpha characters pass thru without escaping
        into the result, but most retain escaping.

        :returns: Formatted string associated with component
        :rtype: string
        """

        s = self._standard_value
        result = []
        idx = 0
        while (idx < len(s)):

            c = s[idx]  # get the idx'th character of s
            if c != "\\":
                # unquoted characters pass thru unharmed
                result.append(c)
            else:
                # Escaped characters are examined
                nextchr = s[idx + 1]

                if (nextchr == ".") or (nextchr == "-") or (nextchr == "_"):
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

        return "".join(result)

    def as_uri_2_3(self):
        """
        Returns the value of component encoded as URI string.

        Scans an input string s and applies the following transformations:

        - Pass alphanumeric characters thru untouched
        - Percent-encode quoted non-alphanumerics as needed
        - Unquoted special characters are mapped to their special forms.

        :returns: URI string associated with component
        :rtype: string
        """

        s = self._standard_value
        result = []
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

            # Bind the unquoted '?' special character to "%01".
            if (thischar == "?"):
                result.append("%01")

            # Bind the unquoted '*' special character to "%02".
            if (thischar == "*"):
                result.append("%02")

            idx += 1

        return "".join(result)

    def as_wfn(self):
        """
        Returns the value of component encoded as Well-Formed Name (WFN)
        string.

        :returns: WFN string associated with component
        :rtype: string
        """

        return self._standard_value

    def get_value(self):
        """
        Returns the encoded value of component.

        :returns: The encoded value of component
        :rtype: string
        """

        return self._encoded_value

    def set_value(self, comp_str, comp_att):
        """
        Set the value of component. By default, the component has a simple
        value.

        :param string comp_str: new value of component
        :param string comp_att: attribute associated with value of component
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        old_value = self._encoded_value
        self._encoded_value = comp_str

        # Check the value of component
        try:
            self._parse(comp_att)
        except ValueError:
            # Restore old value of component
            self._encoded_value = old_value
            raise

        # Convert encoding value to standard value (WFN)
        self._decode()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('../tests/testfile_cpecomp_simple.txt')
