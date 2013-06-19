#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.3 of CPE (Common Platform Enumeration) specification.

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
from abc import ABCMeta
from abc import abstractmethod

import re


class CPEComponent2_3(CPEComponentSingle):
    """
    Represents a component of version 2.3 of CPE specification.
    """

    __metaclass__ = ABCMeta

    ####################
    #  OBJECT METHODS  #
    ####################

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.
        """

        return super(CPEComponent2_3, self).__contains__(item)

    @abstractmethod
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

        super(CPEComponent2_3, self).__init__(comp_str, comp_att)

    @abstractmethod
    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        pass

    @abstractmethod
    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value).

        INPUT:
            - None
        OUTPUT:
            - None
        """
        pass

    def _is_valid_language(self):
        """
        Return True if the value of component in attribute "language" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise

        Possible values of language attribute: a=letter, 1=digit
        LANGUAGE VALUES
        *a
        *aa
        aa
        aaa
        ?a
        ?aa
        ??
        ??a
        ???

        LANGUAGE WITHOUT REGION VALUES
        a*
        aa*
        aaa*
        *111
        *11
        *1

        REGION WITH LANGUAGE VALUES
        *
        ??
        a*
        a?
        aa
        1*
        1?
        1??
        11*
        11?
        111
        """

        comp_str = self._encoded_value.lower()

        # Value with wildcards; separate language and region of value
        parts = comp_str.split(self.SEPARATOR_LANG)
        language = parts[0]

        # Check the language
        lang1_pattern = "^("
        lang1_pattern += "\%s[a-z]{1,2}" % (self.WILDCARD_MULTI)
        lang1_pattern += "|"
        lang1_pattern += "\%s(([a-z][a-z]?)|(\%s(\%s|[a-z])?))" % (self.WILDCARD_ONE,
                                                                   self.WILDCARD_ONE,
                                                                   self.WILDCARD_ONE)
        lang1_pattern += "|"
        lang1_pattern += "([a-z]{2,3})"
        lang1_pattern += ")$"
        lang1_rxc = re.compile(lang1_pattern)

        if lang1_rxc.match(language) is not None:
            # Correct language; check the region part
            region = parts[1]
            region_pattern = "^("
            region_pattern += "(\%s)" % self.WILDCARD_MULTI
            region_pattern += "|"
            region_pattern += "((\%s){2})" % self.WILDCARD_ONE
            region_pattern += "|"
            region_pattern += "([a-z]([a-z]|\%s|\%s))" % (self.WILDCARD_MULTI,
                                                          self.WILDCARD_ONE)
            region_pattern += "|"
            region_pattern += "([0-9](\%s|\%s(\%s)?|[0-9][0-9\%s\%s]))" % (self.WILDCARD_MULTI,
                                                                           self.WILDCARD_ONE,
                                                                           self.WILDCARD_ONE,
                                                                           self.WILDCARD_MULTI,
                                                                           self.WILDCARD_ONE)
            region_pattern += ")$"
            region_rxc = re.compile(region_pattern)

            return region_rxc.match(region) is not None

        elif len(parts) == 1:
            # No region part in value
            lang2_pattern = "^((\%s\d{1,3})|([a-z]{1,3}\%s))$" % (self.WILDCARD_MULTI,
                                                                  self.WILDCARD_MULTI)
            lang2_rxc = re.compile(lang2_pattern)

            return lang2_rxc.match(language) is not None

        else:
            return False

    def _is_valid_part(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value of component is valid, False otherwise
        """

        comp_str = self._encoded_value

        # Check if value of component do not have wildcard
        if ((comp_str.find(self.WILDCARD_ONE) == -1) and
           (comp_str.find(self.WILDCARD_MULTI) == -1)):

            return super(CPEComponent2_3, self)._is_valid_part()

        # Compilation of regular expression associated with value of part
        part_pattern = "^(\%s|\%s)$" % (self.WILDCARD_ONE,
                                        self.WILDCARD_MULTI)
        part_rxc = re.compile(part_pattern)

        # Validation of language value
        return part_rxc.match(comp_str) is not None

    @abstractmethod
    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        INPUT:
            - None
        OUTPUT:
            True if value is valid, False otherwise
        """

        pass

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

        super(CPEComponent2_3, self)._parse(comp_att)

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
        """

        return super(CPEComponent2_3, self).as_fs()

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
        """

        return super(CPEComponent2_3, self).as_uri_2_3()

    def as_wfn(self):
        """
        Returns the value of compoment encoded as Well-Formed Name (WFN)
        string.

        INPUT:
            - None
        OUTPUT:
            - WFN string
        """

        return super(CPEComponent2_3, self).as_wfn()
