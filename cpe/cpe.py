#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe.py
Author: Alejandro Galindo
Date: 23-05-2013
Description: Contains the common characteristics of any type of CPE name,
             associated with a version of Common Platform Enumeration (CPE)
             specification.
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
        print cpe_str

        # Store CPE name with URI style:
        #     CPE names are case-insensitive.
        #     To reduce potential for confusion,
        #     all CPE Names should be written in lowercase
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
        Useful for users.
        """

        return self.__unicode__().encode('utf-8')

    def print_pretty_cpe(self):
        """
        Returns an unambiguous representation of CPE name.
        Useful for programmers and debuggers.
        """

        pp = pprint.PrettyPrinter(indent=4, width=80)

        result = '{0}({1})'.format(str(self.__class__.__name__),
                                   self.version)
        result += "CPE %r => %r\n\n%r\n" % (self.version,
                                            self.cpe_str,
                                            pp.pformat(self._cpe_dict))
        return result
