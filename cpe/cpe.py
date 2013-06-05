#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module contains the common characteristics of
any type of CPE name, associated with a version of Common Platform
Enumeration (CPE) specification. The function is mainly related with
initialization and printing of CPE names.

Copyright (C) 2013  Alejandro Galindo, Roberto A. Martínez

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

import pprint


class CPE(object):
    """
    Represents a generic CPE name compatible with
    all versions of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants of possible versions of CPE specification
    VERSION_UNDEFINED = "undefined"
    VERSION_1_1 = "1.1"
    VERSION_2_2 = "2.2"
    VERSION_2_3 = "2.3"

    # Dictionary keys associated with components of some versions of CPE name
    KEY_PART = "part"
    KEY_VENDOR = "vendor"
    KEY_PRODUCT = "product"
    KEY_VERSION = "version"
    KEY_UPDATE = "update"
    KEY_EDITION = "edition"
    KEY_LANGUAGE = "language"

    # Possible values of part component of CPE name
    VALUE_PART_HW = "h"
    VALUE_PART_OS = "o"
    VALUE_PART_APP = "a"

    ###############
    #  VARIABLES  #
    ###############

    # List of keys associated with CPE name parts
    uri_part_keys = [KEY_PART,
                     KEY_VENDOR,
                     KEY_PRODUCT,
                     KEY_VERSION,
                     KEY_UPDATE,
                     KEY_EDITION,
                     KEY_LANGUAGE]

    # Mapping between order of parts and its value
    uri_ordered_part_dict = {
        0: KEY_PART,
        1: KEY_VENDOR,
        2: KEY_PRODUCT,
        3: KEY_VERSION,
        4: KEY_UPDATE,
        5: KEY_EDITION,
        6: KEY_LANGUAGE
    }

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str):
        """
        Initializes the CPE name object.
        """

        CPE.version = CPE.VERSION_UNDEFINED

        # The original CPE string
        self.cpe_str = cpe_str

        # Store CPE name with URI style:
        # CPE names are case-insensitive.
        # To reduce potential for confusion,
        # all CPE Names should be written in lowercase.
        self.str = cpe_str.lower()

        # Dictionary to save CPE name data
        self._cpe_dict = dict()

    def __unicode__(self):
        """
        Print CPE name as string.
        """

        return "CPE %s => %s\n" % (CPE.version, self.cpe_str)

    def __str__(self):
        """
        Returns a readable representation of CPE name.
        """

        return self.__unicode__().encode('utf-8')

    def print_pretty_cpe(self):
        """
        Returns an unambiguous representation of CPE name.
        """

        pp = pprint.PrettyPrinter(indent=4, width=80)

        result = '{0}({1})'.format(str(self.__class__.__name__),
                                   self.version)
        result += "CPE %r => %r\n\n%r\n" % (self.version,
                                            self.cpe_str,
                                            pp.pformat(self._cpe_dict))
        return result
