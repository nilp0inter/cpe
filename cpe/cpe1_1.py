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
from cpecomp import CPEComponent
from cpecomp1_1 import CPEComponent1_1
from emptycpecomp import EmptyCPEComponent
from undefinedcpecomp import UndefinedCPEComponent

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
    """

    ###############
    #  CONSTANTS  #
    ###############

    VERSION = CPE.VERSION_1_1

    ####################
    #  OBJECT METHODS  #
    ####################

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

        - TEST: CPE name of version 1.1
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE1_1(str)
        >>> comp = c[1]
        >>> comp._data
        ['sun@os']

        - TEST: CPE name of version 1.1
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE1_1(str)
        >>> c[6]
        Traceback (most recent call last):
        IndexError: Component index of CPE name out of range

        - TEST: CPE name of version 1.1
        >>> str = 'cpe://'
        >>> c = CPE1_1(str)
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
                    # Part value not exist as value in version 1.1 of CPE
                    if ck != CPE.KEY_PART:
                        comp = elem.get(ck)
                        if (count == i):
                            if comp != nullcomp:
                                return comp
                            else:
                                raise IndexError(errmsg)
                        else:
                            count += 1

        raise IndexError(errmsg)

    def __init__(self, cpe_str, *args, **kwargs):
        """
        Checks if input CPE name is valid and,
        if so, stores its parts, elements and components.

        INPUT:
            - self: CPE name object
            - cpe_str: CPE name string
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: CPE name bad-formed

        - TEST: an empty hardware part, and no OS or application part.
        >>> str = 'cpe:/'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: an application part
        >>> str = 'cpe://microsoft:windows:2000'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: an OS part with an application part
        >>> str = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: an hardware part with OS part
        >>> str = 'cpe:/cisco::3825/cisco:ios:12.3:enterprise'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: an application part
        >>> str = 'cpe:///microsoft:ie:6.0'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: OS part with operator OR (two subcomponents)
        >>> str = 'cpe://microsoft:windows:xp!vista'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: OS part with operator NOT (a subcomponent)
        >>> str = 'cpe://microsoft:windows:~xp'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: OS part with two elements in application part
        >>> str = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: CPE with special characters
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE(str, CPE.VERSION_1_1)

        - TEST: bad URI syntax
        >>> str = 'baduri'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Malformed CPE name: validation of parts failed

        - TEST: URI with whitespaces
        >>> str = 'cpe:/con espacios'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Malformed CPE name: it must not have whitespaces

        - TEST: two operators in a subcomponent
        >>> str = 'cpe://microsoft:windows:~2000!2007'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: not correct value '~2000!2007'
        """

        super(CPE1_1, self).__init__(cpe_str)
        self._parse()

    def __len__(self):
        """
        Returns the number of components of CPE name.

        - TEST: a CPE name of version 1.1 with empty parts
        >>> str = "cpe:///"
        >>> c = CPE1_1(str)
        >>> len(c)
        0

        - TEST: a CPE name of version 1.1 with two parts (hw and os) and
        some elements empty and with values
        >>> str = "cpe:/cisco::3825/cisco:ios:12.3:enterprise"
        >>> c = CPE1_1(str)
        >>> len(c)
        7

        - TEST: a CPE name of version 1.1 with a application part and
        a component with two subcomponents
        >>> str = "cpe:///adobe:acrobat:6.0:std!pro"
        >>> c = CPE1_1(str)
        >>> len(c)
        4
        """

        count = 0
        for part in CPE.CPE_PART_KEYS:
            if len(self.get(part)) > 0:
                count += 1

        return super(CPE1_1, self).__len__() - count

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 1.1.
        """

        return dict.__new__(cls)

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.
        """

        return "CPE v%s: %s" % (CPE1_1.VERSION, self.cpe_str)

    def _parse(self):
        """
        Checks if the CPE name is valid.

        INPUT:
            - self: CPE name object with CPE name string
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: CPE name bad-formed
        """

        # CPE name must not have whitespaces
        if (self.cpe_str.find(" ") != -1):
            errmsg = "Malformed CPE name: it must not have whitespaces"
            raise ValueError(errmsg)

        # Compilation of regular expression associated with parts of CPE name
        hw = "?P<%s>[^/]+" % CPE.KEY_HW
        os = "?P<%s>[^/]+" % CPE.KEY_OS
        app = "?P<%s>[^/]+" % CPE.KEY_APP

        parts_pattern = "^cpe:/(%s)?(/(%s)?(/(%s)?)?)?$" % (hw, os, app)
        parts_rxc = re.compile(parts_pattern)

        # Partitioning of CPE name in parts
        parts_match = parts_rxc.match(self.cpe_str)

        # ################################
        #  Validation of CPE name parts  #
        # ################################

        if (parts_match is None):
            errmsg = "Malformed CPE name: not correct definition "
            errmsg += "of CPE name parts"
            raise ValueError(errmsg)

        for pk in CPE.CPE_PART_KEYS:
            # Get part content
            part = parts_match.group(pk)
            elements = []

            if (part is not None):
                # Part of CPE name defined

                # ###############################
                #  Validation of part elements  #
                # ###############################

                # semicolon (;) is used to separate the part elements
                for part_elem in part.split(';'):
                    j = 1

                    # ####################################
                    #  Validation of element components  #
                    # ####################################

                    components = dict()

                    # colon (:) is used to separate the element components
                    for elem_comp in part_elem.split(":"):
                        if elem_comp == CPEComponent.EMPTY_VALUE:
                            comp = EmptyCPEComponent()
                        else:
                            try:
                                comp = CPEComponent1_1(elem_comp)
                            except ValueError:
                                errmsg = "Malformed CPE name: "
                                errmsg += "not correct value '%s'" % elem_comp

                                raise ValueError(errmsg)

                        # Identification of component name
                        key = CPE.ORDERED_COMP_PARTS[j]
                        components[key] = comp

                        j += 1

                    # Adds the undefined components
                    for idx in range(j, len(CPE.CPE_COMP_KEYS)):
                        key = CPE.ORDERED_COMP_PARTS[idx]
                        components[key] = UndefinedCPEComponent()

                    # Set the type of system associated with CPE name
                    if (pk == CPE.KEY_HW):
                        components[CPE.KEY_PART] = CPEComponent1_1(CPE.VALUE_PART_HW)
                    elif (pk == CPE.KEY_OS):
                        components[CPE.KEY_PART] = CPEComponent1_1(CPE.VALUE_PART_OS)
                    elif (pk == CPE.KEY_APP):
                        components[CPE.KEY_PART] = CPEComponent1_1(CPE.VALUE_PART_APP)

                    # Store the element identified
                    elements.append(components)
            # Store the part identified
            self[pk] = elements

if __name__ == "__main__":
    import doctest
    doctest.testmod()
