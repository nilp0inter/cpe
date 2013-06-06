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

from undefinedcpecomp import UndefinedCPEComponent


class CPE(dict):
    """
    Represents a generic CPE name compatible with
    all versions of CPE specification.

    Parts of CPE are stored in a dictionary.

    CPE structure (dictionary):
        |- part (hw, os, sw)
            |- element list (list)
                |- component list (dictionary)
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants of possible versions of CPE specification
    VERSION_UNDEFINED = "undefined"
    VERSION_1_1 = "1.1"
    VERSION_2_2 = "2.2"
    VERSION_2_3 = "2.3"

    # Dictionary keys associated with the three type of system
    # included in CPE specification
    KEY_HW = "hw"
    KEY_OS = "os"
    KEY_APP = "app"

    # List of keys associated with the three type of system
    # included in CPE specification
    CPE_PART_KEYS = [KEY_HW, KEY_OS, KEY_APP]

    # Dictionary keys associated with components of all versions of CPE
    KEY_PART = "part"
    KEY_VENDOR = "vendor"
    KEY_PRODUCT = "product"
    KEY_VERSION = "version"
    KEY_UPDATE = "update"
    KEY_EDITION = "edition"
    KEY_LANGUAGE = "language"

    # Dictionary keys associated with components of version 2.3 of CPE
    KEY_SW_EDITION = "sw_edition"
    KEY_TARGET_SW = "target_sw"
    KEY_TARGET_HW = "target_hw"
    KEY_OTHER = "other"

    # List of keys associated with CPE name components
    CPE_COMP_KEYS = [KEY_PART,
                     KEY_VENDOR,
                     KEY_PRODUCT,
                     KEY_VERSION,
                     KEY_UPDATE,
                     KEY_EDITION,
                     KEY_LANGUAGE,
                     KEY_SW_EDITION,
                     KEY_TARGET_SW,
                     KEY_TARGET_HW,
                     KEY_OTHER]

    # Mapping between order of CPE name components and their values
    ORDERED_COMP_PARTS = {
        0: KEY_PART,
        1: KEY_VENDOR,
        2: KEY_PRODUCT,
        3: KEY_VERSION,
        4: KEY_UPDATE,
        5: KEY_EDITION,
        6: KEY_LANGUAGE,
        7: KEY_SW_EDITION,
        8: KEY_TARGET_SW,
        9: KEY_TARGET_HW,
        10: KEY_OTHER}

    # Mapping between CPE name components and their order
    COMP_PART_ORDER = dict(zip(ORDERED_COMP_PARTS.values(),
                               ORDERED_COMP_PARTS.keys()))

    # Possible values of "part" component of CPE (type of system)
    VALUE_PART_HW = "h"
    VALUE_PART_OS = "o"
    VALUE_PART_APP = "a"

    # Constants of possible CPE name styles of version 2.3
    STYLE_UNDEFINED = "undefined"
    STYLE_URI = "URI"
    STYLE_WFN = "WFN"
    STYLE_FS = "FS"

    VERSION = VERSION_UNDEFINED

    def __new__(cls, cpe_str, version=None, *args, **kwargs):
        """
        Generator of CPE names.

        INPUT:
            - cpe_str: CPE name string
            - version: version of CPE specification of cpe_str
        OUTPUT:
            - CPE object with version of CPE detected correctly.
        EXCEPTIONS:
            - NotImplementedError: Version of CPE not implemented
            - ValueError: incorrect CPE name

        This class implements the factory pattern, that is,
        this class centralizes the creation of objects of a particular
        CPE version, hiding the user the requested object instance.
        """

        from cpe1_1 import CPE1_1
        from cpe2_2 import CPE2_2

        # List of implemented versions of CPE names
        _CPE_VERSIONS = {
            CPE.VERSION_1_1: CPE1_1,
            CPE.VERSION_2_2: CPE2_2}

        errmsg = 'Version of CPE not implemented'

        if version is None:
            # Detect CPE version of input CPE name
            for v in _CPE_VERSIONS:
                try:
                    # Validate CPE name
                    c = _CPE_VERSIONS[v](cpe_str)
                except ValueError:
                    # Test another version
                    continue
                else:
                    # Version detected
                    return c

            raise NotImplementedError(errmsg)

        elif version in _CPE_VERSIONS:
            # Correct input version, validate CPE name
            return _CPE_VERSIONS[version](cpe_str)
        else:
            # Invalid CPE version
            raise NotImplementedError(errmsg)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str):
        """
        Store the CPE name.

        INPUT:
            - cpe_str: CPE name string
        OUPUT:
            - None
        """

        # The original CPE name string
        self.cpe_str = cpe_str

        # Store CPE name in lower-case letters:
        # CPE names are case-insensitive.
        # To reduce potential for confusion,
        # all CPE Names should be written in lowercase.
        self._str = cpe_str.lower()

    def __len__(self):
        """
        Returns the number of components of CPE name.

        - TEST: a CPE name of version 1.1 with empty parts
        >>> str = "cpe:///"
        >>> c = CPE(str)
        >>> len(c)
        0

        - TEST: a CPE name of version 1.1 with two parts (hw and os) and
        some elements empty and with values
        >>> str = "cpe:/cisco::3825/cisco:ios:12.3:enterprise"
        >>> c = CPE(str)
        >>> len(c)
        7

        - TEST: a CPE name of version 1.1 with a application part and
        a component with two subcomponents
        >>> str = "cpe:///adobe:acrobat:6.0:std!pro"
        >>> c = CPE(str)
        >>> len(c)
        4

        - TEST: a CPE name of version 2.2 with a application part
        >>> str = "cpe:/a:adobe:acrobat:6.0:pro"
        >>> c = CPE(str)
        >>> len(c)
        5
        """

        count = 0
        nullcomp = UndefinedCPEComponent()

        for part in CPE.CPE_PART_KEYS:
            elements = self.get(part)
            for elem in elements:
                for ck in CPE.CPE_COMP_KEYS:
                    comp = elem.get(ck)
                    if comp != nullcomp:
                        count += 1

        return count

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.
        """

        return "CPE v%s: %s" % (CPE.VERSION, self.cpe_str)

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE name.

        INPUT:
            - self: initialized CPE name
            - i: component index to find
        OUTPUT:
            - component string found
        EXCEPTIONS:
            - IndexError: index not found in CPE name
            - KeyError: not correct internal dictionary of CPE object

        - TEST: CPE name of version 2.2
        >>> str = 'cpe:/a:sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE(str)
        >>> c[2]
        sun@os

        - TEST: CPE name of version 2.2
        >>> str = 'cpe:/h:hp:graphicmedia:7.0'
        >>> c = CPE(str)
        >>> c[6]
        Traceback (most recent call last):
        IndexError: Component index of CPE name out of range
        """

        count = 0
        nullcomp = UndefinedCPEComponent()
        errmsg = "Component index of CPE name out of range"

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                for ck in CPE.CPE_COMP_KEYS:
                    comp = elem.get(ck)
                    if (count == i):
                        if comp != nullcomp:
                            return comp
                        else:
                            raise IndexError(errmsg)
                    else:
                        count += 1

    def _getPartCompNameList(self, part, index):
        """
        Returns the i'th component name of elements of input part.

        INPUT:
            - self: CPE name with data
            - part: Type of part of system (hardware, os, application)
            - index: position of component inside part
        OUTPUT:
            - list of subcomponents of i'th component
        EXCEPTIONS:
            - KeyError: incorrect part

        - TEST: CPE name version 1.1 empty part and index not exists
        >>> str = 'cpe://microsoft:windows:2000!2007'
        >>> c = CPE(str)
        >>> c._getPartCompNameList(CPE.KEY_HW, 2)
        []

        - TEST: CPE name version 1.1 not empty result
        >>> str = 'cpe://microsoft:windows:2000!2007'
        >>> c = CPE(str)
        >>> c._getPartCompNameList(CPE.KEY_OS, 1)
        ['windows']

        - TEST: CPE name version 1.1 two elements in part
        >>> str = 'cpe://microsoft:windows:2000!2007;linux:suse'
        >>> c = CPE(str)
        >>> c._getPartCompNameList(CPE.KEY_OS, 1)
        ['windows', 'suse']
        """

        lc = []
        if (part not in CPE.CPE_PART_KEYS):
            errmsg = "Key '%s' is not exist" % part
            raise KeyError(errmsg)

        elements = self.get(part)
        for elem in elements:
            if len(elem) > index:
                comp = elem[index]
                lc.append(comp.__str__())
        return lc

    def print_cpe(self):
        """
        Returns an unambiguous representation of CPE name.
        """

        txt = ""
        for pk in CPE.CPE_PART_KEYS:
            txt += "%s\n" % pk
            elements = self.get(pk)
            for i in range(0, len(elements)):
                txt += "  elem %s\n" % i
                for ck in CPE.CPE_COMP_KEYS:
                    txt += "    %s\n" % ck
                    comp = elements[i].get(ck)
                    txt += "      %s\n" % comp.__str__()

        return txt

    def as_dict(self):
        """
        Returns CPE name dict as string.
        """

        return super(CPE, self).__str__()

    def as_uri(self):
        """
        Return the CPE name with URI style.
        """

        return self.cpe_str

    def isHardware(self):
        """
        Returns True if CPE name corresponds to hardware elem.

        - TEST: CPE name version 2.2 is HW
        >>> str = 'cpe:/h:nvidia:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE(str)
        >>> c.isHardware() == True
        True

        - TEST: CPE name version 2.2 is not HW
        >>> str = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE(str)
        >>> c.isHardware() == False
        True

        - TEST: CPE name version 2.2 is not HW
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.isHardware() == False
        True
        """

        elements = self.get(CPE.KEY_HW)
        return len(elements) > 0

    def isOperatingSystem(self):
        """
        Returns True if CPE name corresponds to operating system elem.

        - TEST: CPE name version 2.2 is not OS
        >>> str = 'cpe:/h:nvidia:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE(str)
        >>> c.isOperatingSystem() == False
        True

        - TEST: CPE name version 2.2 is OS
        >>> str = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE(str)
        >>> c.isOperatingSystem() == True
        True

        - TEST: CPE name version 2.2 is not OS
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.isOperatingSystem() == False
        True
        """

        elements = self.get(CPE.KEY_OS)
        return len(elements) > 0

    def isApplication(self):
        """
        Returns True if CPE name corresponds to application elem.

        - TEST: CPE name version 2.2 is not application
        >>> str = 'cpe:/h:nvidia:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE(str)
        >>> c.isApplication() == False
        True

        - TEST: CPE name version 2.2 is not application
        >>> str = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE(str)
        >>> c.isApplication() == False
        True

        - TEST: CPE name version 2.2 is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.isApplication() == True
        True
        """

        elements = self.get(CPE.KEY_APP)
        return len(elements) > 0

    def getPart(self):
        """
        Returns the part component of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.

        - TEST: CPE name version 2.2 is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.getPart()
        ['a']

        - TEST: CPE name version 2.2 is operating system
        >>> str = 'cpe:/o:microsoft:xp'
        >>> c = CPE(str)
        >>> c.getPart()
        ['o']

        - TEST: CPE name version 2.2 is hardware
        >>> str = 'cpe:/h:cisco'
        >>> c = CPE(str)
        >>> c.getPart()
        ['h']
        """

        comp_key = CPE.KEY_PART
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])

    def getVendor(self):
        """
        Returns the vendor name of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.

        - TEST: CPE name version 1.1 is application
        >>> str = 'cpe://microsoft:ie:10;hp:admincenter:8'
        >>> c = CPE(str)
        >>> c.getVendor()
        ['microsoft', 'hp']

        - TEST: CPE name version 2.2 is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.getVendor()
        ['microsoft']
        """

        comp_key = CPE.KEY_VENDOR
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])

    def getProduct(self):
        """
        Returns the product name of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.

        - TEST: CPE name version 1.1 is application
        >>> str = 'cpe://microsoft:ie:10;hp:admincenter:8'
        >>> c = CPE(str)
        >>> c.getVendor()
        ['ie', 'admincenter']

        - TEST: CPE name version 2.2 is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.getProduct()
        ['ie']
        """

        comp_key = CPE.KEY_PRODUCT
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])

    def getVersion(self):
        """
        Returns the version of product of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.

        - TEST: CPE name version 2.2 is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE(str)
        >>> c.getVersion()
        ['10']
        """

        comp_key = CPE.KEY_VERSION
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE name as a list.
        According to the CPE version, this list can contains one or more items.

        - TEST: CPE name version 2.2 is operating system
        >>> str = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE(str)
        >>> c.getUpdate()
        ['sp2']
        """

        comp_key = CPE.KEY_UPDATE
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])

    def getEdition(self):
        """
        Returns the edition of product of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.

        - TEST: CPE name version 2.2 is operating system
        >>> str = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE(str)
        >>> c.getEdition()
        ['pro']
        """

        comp_key = CPE.KEY_EDITION
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])

    def getLanguage(self):
        """
        Returns the internationalization information of CPE name as a list.
        According to the CPE version, this list can contains one or more items.

        - TEST: CPE name version 2.2 is application
        >>> str = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE(str)
        >>> c.getLanguage()
        ['es-es']
        """

        comp_key = CPE.KEY_LANGUAGE
        for pk in CPE.CPE_PART_KEYS:
            return self._getPartCompNameList(pk, CPE.COMP_PART_ORDER[comp_key])
