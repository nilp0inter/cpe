#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with version 1.1 of CPE (Common Platform Enumeration)
specification.

Copyright (C) 2013  Roberto A. Martínez, Alejandro Galindo

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

from cpe import CPE

import re


class CPE1_1(CPE):
    """
    Implementation of version 1.1 of CPE specification.

    Basic structure of CPE name:
    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE name syntax:
    - cpe:/ {hardware-part} [ / {OS-part} [ / {application-part} ] ]

    - TEST: an empty hardware part, and no OS or application part.
    >>> str = 'cpe:/'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an application part
    >>> str = 'cpe://microsoft:windows:2000'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an OS part with an application part
    >>> str = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an hardware part with OS part
    >>> str = 'cpe:/cisco::3825/cisco:ios:12.3:enterprise'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an application part
    >>> str = 'cpe:///microsoft:ie:6.0'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: OS part with operator OR (two subcomponents)
    >>> str = 'cpe://microsoft:windows:xp!vista'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: OS part with operator NOT (a subcomponent)
    >>> str = 'cpe://microsoft:windows:~xp'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: OS part with two elements in application part
    >>> str = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: CPE with special characters
    >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
    >>> CPE1_1(str) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: bad URI syntax
    >>> str = 'baduri'
    >>> c = CPE1_1(str)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: validation of parts failed

    - TEST: URI with whitespaces
    >>> str = 'cpe:/con espacios'
    >>> c = CPE1_1(str)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: it must not have whitespaces

    - TEST: two operators in a subcomponent
    >>> str = 'cpe://microsoft:windows:~2000!2007'
    >>> c = CPE1_1(str)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: operators '~' and '!' \
    cannot be together in the same component
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Dictionary keys associated with parts of CPE name
    KEY_HW = "hw"
    KEY_OS = "os"
    KEY_APP = "app"

    # Dictionary keys associated with component data of CPE name
    KEY_COMP_OP = "op"
    KEY_COMP_STR = "str"

    # Possible values of operators in components of CPE name
    VALUE_COMP_OP_OR = "!"
    VALUE_COMP_OP_NOT = "~"
    VALUE_COMP_OP_NONE = "None"
    VALUE_COMP_OP_ANY = "ANY"

    ###############
    #  VARIABLES  #
    ###############

    cpe_part_keys = [KEY_HW, KEY_OS, KEY_APP]

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _create_comp(cls, str, op):
        """
        Returns a dictionary with component data: value str and operator op.
        """

        comp = dict()
        comp[CPE1_1.KEY_COMP_OP] = op
        comp[CPE1_1.KEY_COMP_STR] = str

        return comp

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str='cpe:/'):
        """
        Checks if input CPE name defined with URI style is valid and,
        if so, stores its parts, elements and components.
        """

        CPE.__init__(self, cpe_str)
        CPE.version = CPE.VERSION_1_1
        self._validate()

    def __len__(self):
        """
        Returns the number of components of CPE name.
        "a!b" is a component, not two components.

        - TEST: a CPE name without components
        >>> str = "cpe:///"
        >>> c = CPE1_1(str)
        >>> len(c)
        0

        - TEST: a CPE name with some elements
        >>> str = "cpe:/cisco::3825/cisco:ios:12.3:enterprise"
        >>> c = CPE1_1(str)
        >>> len(c)
        7

        - TEST: a component with two subcomponents
        >>> str = "cpe:///adobe:acrobat:6.0:std!pro"
        >>> c = CPE1_1(str)
        >>> len(c)
        4
        """

        count = 0

        for pk in CPE1_1.cpe_part_keys:
            elements = self._cpe_dict[pk]
            for elem in elements:
                for component in elem:
                    count += 1

        return count

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE name as a string.

        - TEST
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE1_1(str)
        >>> c[1]
        [{'str': 'sun@os', 'op': 'None'}]

        - TEST
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE1_1(str)
        >>> c[6]
        Traceback (most recent call last):
        IndexError: Component index of CPE name out of range

        - TEST
        >>> str = 'cpe://'
        >>> c = CPE1_1(str)
        >>> c[6]
        Traceback (most recent call last):
        IndexError: Component index of CPE name out of range
        """

        count = 0

        for pk in CPE1_1.cpe_part_keys:
            elements = self._cpe_dict[pk]
            for elem in elements:
                for comp in elem:
                    if (count == i):
                        return comp
                    else:
                        count += 1

        msg = "Component index of CPE name out of range"
        raise IndexError(msg)

    def _validate(self):
        """
        Checks if CPE name with URI style is valid.
        """

        # CPE name must not have whitespaces
        if (self.cpe_str.find(" ") != -1):
            msg = "Malformed CPE name: it must not have whitespaces"
            raise ValueError(msg)

        # Compilation of regular expression associated with parts of CPE name
        hw = "?P<%s>[^/]+" % CPE1_1.KEY_HW
        os = "?P<%s>[^/]+" % CPE1_1.KEY_OS
        app = "?P<%s>[^/]+" % CPE1_1.KEY_APP

        parts_pattern = "^cpe:/(%s)?(/(%s)?(/(%s)?)?)?$" % (hw, os, app)
        parts_rxc = re.compile(parts_pattern)

        # Partitioning of CPE name in parts
        parts_match = parts_rxc.match(self.cpe_str)

        # ################################
        #  Validation of CPE name parts  #
        # ################################

        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        # Compilation of regular expression associated with
        # string of components
        str_pattern = "[\w\.\-,\(\)@\#]+"
        str_rxc = re.compile(str_pattern)

        for pk in CPE1_1.cpe_part_keys:
            self._cpe_dict[pk] = []

            # Get part content
            part = parts_match.group(pk)

            if (part is not None):

                # Part content is not empty
                i = 0

                # ###############################
                #  Validation of part elements  #
                # ###############################

                # semicolon (;) is used to separate the part elements
                for part_elem in part.split(';'):
                    self._cpe_dict[pk].append([])
                    self._cpe_dict[pk][i] = []
                    j = 0

                    # ####################################
                    #  Validation of element components  #
                    # ####################################

                    # colon (:) is used to separate the element components
                    for elem_comp in part_elem.split(":"):
                        self._cpe_dict[pk][i].append([])
                        self._cpe_dict[pk][i][j] = []

                        # Compilation of regular expression associated with
                        # components
                        forbidden = "[^~!:;/%]+"
                        cpe_comp_pattern = "^(~?%s)(!%s)*$" % (forbidden,
                                                               forbidden)
                        cpe_comp_rxc = re.compile(cpe_comp_pattern)

                        # Partitioning of components
                        comp_match = cpe_comp_rxc.match(elem_comp)

                        # Validation of compoments
                        if (comp_match is not None):
                            if (len(elem_comp) == 0):
                                # Any value is possible
                                comp = CPE1_1._create_comp(elem_comp,
                                                           CPE1_1.VALUE_COMP_OP_ANY)

                                self._cpe_dict[pk][i][j].append(comp)
                            else:
                                # Component is not empty
                                not_found = elem_comp.find('~') != -1
                                or_found = elem_comp.find('!') != -1

                                if (not_found) and (or_found):
                                    # The OR and NOT operators may not be used
                                    # together
                                    msg = "Malformed CPE name: operators '~' and '!' "
                                    msg += "cannot be together in the same component"

                                    raise ValueError(msg)

                                elif elem_comp.find('~') == 0:
                                    # Operator NOT with a string
                                    str = elem_comp[1:]

                                    comp = CPE1_1._create_comp(elem_comp,
                                                               CPE1_1.VALUE_COMP_OP_NOT)

                                    if (str_rxc.match(str) is None):
                                        msg = "Malformed CPE name: component string must have "
                                        msg += "only alphanumeric and the following characters:"
                                        msg += " '.', '_', '-', ',', '(', ')', '@', '#'"

                                        raise ValueError(msg)

                                    self._cpe_dict[pk][i][j].append(comp)

                                elif elem_comp.find('!') != -1:
                                    # Operator OR with two or more strings
                                    for str in elem_comp.split('!'):
                                        if (str_rxc.match(str) is None):
                                            msg = "Malformed CPE name: names must have "
                                            msg += "only the following characters:"
                                            msg += " alfanumeric, '.', '_', '-', "
                                            msg += "',', '(', ')', '@', '#'"

                                            raise ValueError(msg)

                                        comp = CPE1_1._create_comp(str,
                                                                   CPE1_1.VALUE_COMP_OP_OR)

                                        self._cpe_dict[pk][i][j].append(comp)
                                else:
                                    # Name without operator
                                    comp = CPE1_1._create_comp(elem_comp,
                                                               CPE1_1.VALUE_COMP_OP_NONE)

                                    self._cpe_dict[pk][i][j].append(comp)
                        j += 1
                    i += 1

        return self._cpe_dict

    def _getPartCompNameList(self, part, index):
        """
        Returns the i'th component name of elements of input part:

        INPUT:
            - part: Type of part of system (hardware, os, application)
            - index: position of component inside part

        OUTPUT:
            - list of subcomponents of i'th component

        - TEST: empty part and index not exists
        >>> str = 'cpe://microsoft:windows:2000!2007'
        >>> c = CPE1_1(str)
        >>> c._getPartCompNameList(CPE1_1.KEY_HW, 2)
        []

        - TEST: not empty result
        >>> str = 'cpe://microsoft:windows:2000!2007'
        >>> c = CPE1_1(str)
        >>> c._getPartCompNameList(CPE1_1.KEY_OS, 1)
        ['windows']

        - TEST: two elements in part
        >>> str = 'cpe://microsoft:windows:2000!2007;linux:suse'
        >>> c = CPE1_1(str)
        >>> c._getPartCompNameList(CPE1_1.KEY_OS, 1)
        ['windows', 'suse']
        """

        lc = []
        if (part not in self._cpe_dict.keys()):
            raise KeyError("Part key is not exist")

        elements = self._cpe_dict[part]
        for elem in elements:
            if len(elem) > index:
                comp = elem[index]
                for subcomp in comp:
                    key = CPE1_1.KEY_COMP_STR
                    lc.append(subcomp[key])
        return lc

    def getHardwareVendorList(self):
        """
        Returns the hardware vendor list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_HW, 0)

    def getHardwareProductList(self):
        """
        Returns the hardware family name list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_HW, 1)

    def getHardwareVersionList(self):
        """
        Returns the hardware model list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_HW, 2)

    def getOsVendorList(self):
        """
        Returns the operating system vendor list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_OS, 0)

    def getOsProductList(self):
        """
        Returns the operating system family name list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_OS, 1)

    def getOsVersionList(self):
        """
        Returns the operating system version list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_OS, 2)

    def getAppVendorList(self):
        """
        Returns the application vendor list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_APP, 0)

    def getAppProductList(self):
        """
        Returns the application family name list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_APP, 1)

    def getAppVersionList(self):
        """
        Returns the application edition list.
        """

        return self._getPartCompNameList(CPE1_1.KEY_APP, 2)


if __name__ == "__main__":

    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
