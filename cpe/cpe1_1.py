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
from cpecomp1_1 import CPEComponent1_1
from emptycpecomp import EmptyCPEComponent

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
    #  VARIABLES  #
    ###############

    VERSION = CPE.VERSION_1_1

    ####################
    #  OBJECT METHODS  #
    ####################

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 1.1.
        """

        return dict.__new__(cls)

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
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: an application part
        >>> str = 'cpe://microsoft:windows:2000'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: an OS part with an application part
        >>> str = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: an hardware part with OS part
        >>> str = 'cpe:/cisco::3825/cisco:ios:12.3:enterprise'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: an application part
        >>> str = 'cpe:///microsoft:ie:6.0'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: OS part with operator OR (two subcomponents)
        >>> str = 'cpe://microsoft:windows:xp!vista'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: OS part with operator NOT (a subcomponent)
        >>> str = 'cpe://microsoft:windows:~xp'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: OS part with two elements in application part
        >>> str = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

        - TEST: CPE with special characters
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE(str, CPE.VERSION_1_1) # doctest: +ELLIPSIS

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

            if (part is None):
                # Part of CPE name not defined.
                # Create a element and fill its components with empty values
                elem_parts = dict()
                elements.append(CPE._init_part(elem_parts))
            else:
                # Part of CPE name defined

                # ###############################
                #  Validation of part elements  #
                # ###############################

                # semicolon (;) is used to separate the part elements
                for part_elem in part.split(';'):
                    j = 0

                    # ####################################
                    #  Validation of element components  #
                    # ####################################

                    components = dict()

                    # colon (:) is used to separate the element components
                    for elem_comp in part_elem.split(":"):
                        if elem_comp == "":
                            # Empty value: any value is possible
                            comp = EmptyCPEComponent()
                        else:
                            try:
                                comp = CPEComponent1_1(elem_comp)
                            except ValueError:
                                errmsg = "Malformed CPE name: "
                                errmsg += "not correct value '%s'" % elem_comp

                                raise ValueError(errmsg)

                        # Identification of component name
                        key = CPE.ORDERED_COMP_PARTS[j+1]
                        components[key] = comp

                        j += 1

                    # Store the element identified
                    elements.append(components)
            # Store the part identified
            self[pk] = elements

    def as_uri(self):
        """
        Return the CPE name with URI style.
        """

        return self.cpe_str

if __name__ == "__main__":

    import doctest
    doctest.testmod()
