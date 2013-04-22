#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe1_1.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Module for the treatment of identifiers in accordance with
             version 1.1 of standard CPE (Common Platform Enumeration).
'''


from cpebase import CPEBASE

import re


class CPE1_1(CPEBASE):
    '''
    Implementation of CPE 1.1 specification.
    '''

    # CPE version
    VERSION = '1.1'

    # Constants associated dictionary keys that store CPE id elements
    KEY_HW = "hardware"
    KEY_OS = "os"
    KEY_APP = "application"

    KEY_OP = "op"
    KEY_NAME = "name"

    def __init__(self, cpe_uri):
        """
        Checks that a CPE identifier defined as URI binding is valid and,
        if so, stores the components in a dictionary.
        """

        CPEBASE.__init__(self, cpe_uri)

        self.__validate_uri()

    def __validate_uri(self):
        '''
        Checks input CPE identifier URI is correct.
        '''

        # CPE ID URI must not have whitespaces
        if (self.cpe_uri.find(" ") != -1):
            msg = "Malformed CPE, it must not have whitespaces"
            raise TypeError(msg)

        # Compilation of regular expression associated with name of components
        name_pattern = "[\d\w\.\-,\(\)@#]+"
        name_rxc = re.compile(name_pattern, re.IGNORECASE)

        # ###################
        #  CPE ID PART
        # ###################

        # Compilation of regular expression associated with parts of CPE ID
        hw = "?P<%s>[^/]+" % CPE1_1.KEY_HW
        os = "?P<%s>[^/]+" % CPE1_1.KEY_OS
        app = "?P<%s>[^/]+" % CPE1_1.KEY_APP

        parts_pattern = "^cpe:/(%s)?(/(%s)?(/(%s)?)?)?$" % (hw, os, app)
        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE ID
        parts_match = parts_rxc.match(self.cpe_uri)

        # Validation of CPE ID parts
        if (parts_match is None):
            msg = "Input identifier is not a valid CPE ID: "
            msg += "Error to split CPE ID parts"
            raise TypeError(msg)

        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]
        for pk in parts_key:
            self.cpe_dict[pk] = []

            # Get part content
            part = parts_match.group(pk)

            if (part is not None):

                # Part content is not empty
                i = 0

                # ############################
                #  CPE ID PART ELEMENTS
                # ###########################

                # semicolon (;) is ueesed to separate the name elements
                # in a CPE Name part
                for part_elem in part.split(';'):
                    self.cpe_dict[pk].append({})
                    self.cpe_dict[pk][i] = []
                    j = 0

                    # #################################
                    #  CPE ID PART ELEMENT COMPONENTS
                    # #################################

                    # colon (:) is used to separate the components
                    # in a name element
                    for elem_comp in part_elem.split(":"):

                        self.cpe_dict[pk][i].append({})
                        self.cpe_dict[pk][i][j] = {}

                        # Compilation of regular expression associated with
                        # components of CPE part
                        cpe_comp_pattern = "^(~?[^~!:;/%]+)(![^~!:;/%]+)*$"
                        cpe_comp_rxc = re.compile(cpe_comp_pattern,
                                                  re.IGNORECASE)

                        comp_match = cpe_comp_rxc.match(elem_comp)

                        if (comp_match is not None):
                            # Component is not empty
                            not_found = elem_comp.find('~') != -1
                            or_found = elem_comp.find('!') != -1

                            if (not_found) and (or_found):
                                # The OR and NOT operators may not be used
                                # together
                                msg = "Malformed CPE, can't ~ and ! "
                                msg += "in the same component"

                                raise TypeError(msg)

                            elif elem_comp.find('~') == 0:
                                # Operator NOT with a name
                                op = elem_comp[0]
                                name = elem_comp[1:]

                                component = {}
                                component[CPE1_1.KEY_OP] = op
                                component[CPE1_1.KEY_NAME] = name

                                if (name_rxc.match(name) is None):
                                    msg = "Malformed CPE, names must have "
                                    msg += "only the following characters: "
                                    msg += "alfanumeric, '.', '_', '-', "
                                    msg += "',', '(', ')', '@', '#'"

                                    raise TypeError(msg)

                                self.cpe_dict[pk][i][j] = component

                            elif elem_comp.find('!') != -1:
                                # Operator OR with two or more names
                                for name in elem_comp.split('!'):
                                    component = {}
                                    component[CPE1_1.KEY_OP] = '!'
                                    component[CPE1_1.KEY_NAME] = name

                                    if (name_rxc.match(name) is None):
                                        msg = "Malformed CPE, names must have "
                                        msg += "only the following characters:"
                                        msg += " alfanumeric, '.', '_', '-', "
                                        msg += "',', '(', ')', '@', '#'"

                                        raise TypeError(msg)

                                    self.cpe_dict[pk][i][j] = component
                            else:
                                # Name without operator
                                component = {}
                                component[CPE1_1.KEY_OP] = ""
                                component[CPE1_1.KEY_NAME] = elem_comp

                                self.cpe_dict[pk][i][j] = component
                        j += 1
                    i += 1

        return self.cpe_dict

    def __len__(self):
        '''
        Returns the number of component names of CPE ID.
        '''

        count = 0
        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]

        for pk in parts_key:
            elements = self.cpe_dict[pk]
            for elem in elements:
                for component in elem:
                    count += 1

        return count

    def __getitem__(self, i):
        '''
        Returns the i'th component name of CPE ID as a string.
        '''

        NONAME = ""
        count = 0
        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]

        for pk in parts_key:
            elements = self.cpe_dict[pk]
            for elem in elements:
                for comp in elem:
                    if (count == i):
                        key = CPE1_1.KEY_NAME
                        if (key in comp):
                            return comp[key]
                        else:
                            return NONAME
                    else:
                        count += 1
        return NONAME

    def __getPartCompNameList(self, part, index):
        '''
        Returns the i'th component name of elements of input part:

        INPUT:
            - part: Type of part of system (hardware, os, application)
            - index: position of component inside part

        OUTPUT:
            - list of component name of part
        '''

        NONAME = ""
        l = []
        if (part not in self.cpe_dict.keys()):
            raise ValueError("Part key is not exist")

        elements = self.cpe_dict[part]

        for elem in elements:
            if len(elem) > index:
                comp = elem[index]
                if len(comp.keys()) == 0:
                    l.append(NONAME)
                else:
                    l.append(comp[CPE1_1.KEY_NAME])

        return l

    def getHardwareVendorList(self):
        '''
        Returns the hardware vendor list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_HW, 0)

    def getHardwareFamilyList(self):
        '''
        Returns the hardware family name list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_HW, 1)

    def getHardwareModelList(self):
        '''
        Returns the hardware model list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_HW, 2)

    def getOsVendorList(self):
        '''
        Returns the operating system vendor list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_OS, 0)

    def getOsFamilyList(self):
        '''
        Returns the operating system family name list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_OS, 1)

    def getOsVersionList(self):
        '''
        Returns the operating system version list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_OS, 2)

    def getAppVendorList(self):
        '''
        Returns the application vendor list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_APP, 0)

    def getAppFamilyList(self):
        '''
        Returns the application family name list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_APP, 1)

    def getAppEditionList(self):
        '''
        Returns the application edition list.
        '''

        return self.__getPartCompNameList(CPE1_1.KEY_APP, 2)

if __name__ == "__main__":
    #uri = 'cpe:/cisco::3825/cisco:ios:12.3:enterprise'
    #uri = 'cpe:///'
    #uri = 'cpe:////'
    #uri = 'cpe://microsoft:windows:2000::sp4'
    #uri = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
    uri = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
    #uri = 'cpe://microsoft:windows:xp!vista'
    #uri = 'cpe://microsoft:windows:~xp'
    #uri = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'

    ce = CPE1_1(uri)
    print("")
    print(ce)
    print("Elements: %s") % len(ce)
    print("")
    for i in range(len(ce)):
        print("Element %s: %s") % (i, ce[i])
    print("")
    print("HARDWARE vendor list: %s") % ce.getHardwareVendorList()
    print("")
    print("HARDWARE family name list: %s") % ce.getHardwareFamilyList()
    print("")
    print("HARDWARE model list: %s") % ce.getHardwareModelList()
    print("")
    print("OS vendor list: %s") % ce.getOsVendorList()
    print("")
    print("OS family name list: %s") % ce.getOsFamilyList()
    print("")
    print("OS version list: %s") % ce.getOsVersionList()
    print("")
    print("Application vendor list: %s") % ce.getAppVendorList()
    print("")
    print("Application family name list: %s") % ce.getAppFamilyList()
    print("")
    print("Application edition list: %s") % ce.getAppEditionList()
    print("")
