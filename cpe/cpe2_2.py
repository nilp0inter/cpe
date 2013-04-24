#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe2_2.py
Author: Alejandro Galindo
Date: 23-04-2013
Description: Module for the treatment of identifiers in accordance with
             version 2.2 of standard CPE (Common Platform Enumeration).
'''


from cpebase import CPEBASE

import re


class CPE2_2(CPEBASE):
    '''
    Implementation of CPE 2.2 specification.
    '''

    # CPE version
    VERSION = '2.2'

    # Constants associated dictionary keys that store CPE id elements
    KEY_TYPE = "type"
    KEY_VENDOR = "vendor"
    KEY_PRODUCT = "product"
    KEY_VERSION = "version"
    KEY_UPDATE = "update"
    KEY_EDITION = "edition"
    KEY_LANGUAGE = "language"

    KEY_TYPE_HW = "h"
    KEY_TYPE_OS = "o"
    KEY_TYPE_APP = "a"

    def __init__(self, cpe_uri):
        """
        Checks that a CPE identifier defined as URI binding is valid and,
        if so, stores the components in a dictionary.
        """

        CPEBASE.__init__(self, cpe_uri)

        self.__validate_uri()

        # Mapping between order of parts and its value
        self.order_parts_dict = {
            0: CPE2_2.KEY_TYPE,
            1: CPE2_2.KEY_VENDOR,
            2: CPE2_2.KEY_PRODUCT,
            3: CPE2_2.KEY_VERSION,
            4: CPE2_2.KEY_UPDATE,
            5: CPE2_2.KEY_EDITION,
            6: CPE2_2.KEY_LANGUAGE
        }

    def __validate_uri(self):
        '''
        Checks input CPE identifier URI is correct.
        '''

        # CPE ID URI must not have whitespaces
        if (self.cpe_uri.find(" ") != -1):
            msg = "Malformed CPE, it must not have whitespaces"
            raise TypeError(msg)

        # #####################
        #  CHECK CPE ID PARTS
        # #####################

        # Compilation of regular expression associated with parts of CPE ID
        typesys = "?P<%s>(h|o|a)" % CPE2_2.KEY_TYPE
        vendor = "?P<%s>[^:]+" % CPE2_2.KEY_VENDOR
        product = "?P<%s>[^:]+" % CPE2_2.KEY_PRODUCT
        version = "?P<%s>[^:]+" % CPE2_2.KEY_VERSION
        update = "?P<%s>[^:]+" % CPE2_2.KEY_UPDATE
        edition = "?P<%s>[^:]+" % CPE2_2.KEY_EDITION
        language = "?P<%s>[^:]+" % CPE2_2.KEY_LANGUAGE

        parts_pattern = "^cpe:/"
        parts_pattern += "(%s)?" % typesys
        parts_pattern += "(:(%s)?)?" % vendor
        parts_pattern += "(:(%s)?)?" % product
        parts_pattern += "(:(%s)?)?" % version
        parts_pattern += "(:(%s)?)?" % update
        parts_pattern += "(:(%s)?)?" % edition
        parts_pattern += "(:(%s)?)?$" % language
        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE ID
        parts_match = parts_rxc.match(self.cpe_uri)

        # Validation of CPE ID parts
        if (parts_match is None):
            msg = "Input identifier is not a valid CPE ID: "
            msg += "Error to split CPE ID parts"
            raise TypeError(msg)

        parts_key = []
        parts_key.append(CPE2_2.KEY_TYPE)
        parts_key.append(CPE2_2.KEY_VENDOR)
        parts_key.append(CPE2_2.KEY_PRODUCT)
        parts_key.append(CPE2_2.KEY_VERSION)
        parts_key.append(CPE2_2.KEY_UPDATE)
        parts_key.append(CPE2_2.KEY_EDITION)
        parts_key.append(CPE2_2.KEY_LANGUAGE)

        # Compilation of regular expression associated with
        # value of CPE part
        part_value_pattern = "[\d\w\._-~%]+"
        part_value_rxc = re.compile(part_value_pattern, re.IGNORECASE)

        for pk in parts_key:
            value = parts_match.group(pk)

            if (value is not None):
                if (part_value_rxc.match(value) is None):
                    msg = "Malformed CPE, part value must have "
                    msg += "only the following characters:"
                    msg += " alfanumeric, '.', '_', '-', '~', '%'"

                    raise TypeError(msg)

            self.cpe_dict[pk] = value

        return self.cpe_dict

    def __len__(self):
        '''
        Returns the number of parts of CPE ID.
        '''

        return len(self.cpe_dict.keys())

    def __getitem__(self, i):
        '''
        Returns the i'th component name of CPE ID as a string.
        '''

        if i not in self.order_parts_dict.keys():
            max_index = len(self.order_parts_dict.keys())
            msg = "index not exists. Possible values: 0-%s" % max_index
            raise KeyError(msg)

        part_key = self.order_parts_dict[i]

        return self.cpe_dict[part_key]

    def isHardware(self):
        '''
        Returns TRUE if CPE ID corresponds to hardware elem.
        '''

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_2.KEY_TYPE]

        isHW = type_value == CPE2_2.KEY_TYPE_HW
        isEmpty = type_value == ""

        return (isHW or isEmpty)

    def isOperatingSystem(self):
        '''
        Returns TRUE if CPE ID corresponds to operating system elem.
        '''

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_2.KEY_TYPE]

        isOS = type_value == CPE2_2.KEY_TYPE_OS
        isEmpty = type_value == ""

        return (isOS or isEmpty)

    def isApplication(self):
        '''
        Returns TRUE if CPE ID corresponds to application elem.
        '''

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_2.KEY_TYPE]

        isApp = type_value == CPE2_2.KEY_TYPE_APP
        isEmpty = type_value == ""

        return (isApp or isEmpty)

    def getVendor(self):
        '''
        Returns the vendor name of CPE ID.
        '''

        return self.cpe_dict[CPE2_2.KEY_VENDOR]

    def getProduct(self):
        '''
        Returns the product name of CPE ID.
        '''

        return self.cpe_dict[CPE2_2.KEY_PRODUCT]

    def getVersion(self):
        '''
        Returns the version of product of CPE ID.
        '''

        return self.cpe_dict[CPE2_2.KEY_VERSION]

    def getUpdate(self):
        '''
        Returns the update or service pack information of CPE ID.
        '''

        return self.cpe_dict[CPE2_2.KEY_UPDATE]

    def getEdition(self):
        '''
        Returns the edition of product of CPE ID.
        '''

        return self.cpe_dict[CPE2_2.KEY_EDITION]

    def getLanguage(self):
        '''
        Returns the internationalization information of CPE ID.
        '''

        return self.cpe_dict[CPE2_2.KEY_LANGUAGE]

if __name__ == "__main__":
    #uri = 'cpe:/'
    uri = 'cpe:/::::::'
    #uri = 'cpe:/o:microsoft:windows_xp:::pro'
    #uri = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
    #uri = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'

    ce = CPE2_2(uri)
    print("")
    print(ce)
    print("Elements: %s") % len(ce)
    print("")
    for i in range(len(ce)):
        print("Element %s: %s") % (i, ce[i])
    print("")
    print("IS HARDWARE: %s") % ce.isHardware()
    print("IS OS: %s") % ce.isOperatingSystem()
    print("IS APPLICATION: %s") % ce.isApplication()
    print("")
    print("VENDOR: %s") % ce.getVendor()
    print("PRODUCT: %s") % ce.getProduct()
    print("VERSION: %s") % ce.getVersion()
    print("UPDATE: %s") % ce.getUpdate()
    print("EDITION: %s") % ce.getEdition()
    print("LANGUAGE: %s") % ce.getLanguage()
    print("")
