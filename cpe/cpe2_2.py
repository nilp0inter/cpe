#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with version 2.2 of CPE (Common Platform Enumeration)
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
from emptycpecomp import EmptyCPEComponent
from undefinedcpecomp import UndefinedCPEComponent

import re


class CPE2_2(CPE):
    """
    Implementation of version 2.2 of CPE specification.

    A CPE name is a percent-encoded URI with each name
    starting with the prefix (the URI scheme name) 'cpe:'.

    Each platform can be broken down into many distinct parts.
    A CPE name specifies a single part and is used to identify
    any platform that matches the description of that part.
    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE name syntax:
    - cpe:/{part}:{vendor}:{product}:{version}:{update}:{edition}:{language}
    """

    ###############
    #  CONSTANTS  #
    ###############

    VERSION = CPE.VERSION_2_2

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str, *args, **kwargs):
        """
        Checks if input CPE name is valid and,
        if so, stores its components.

        INPUT:
            - self: CPE name object
            - cpe_str: CPE name string
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: CPE name bad-formed

        - TEST: bad URI
        >>> str = 'baduri'
        >>> CPE(str, CPE.VERSION_2_2) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Malformed CPE name: validation of parts failed

        - TEST: URI with whitespaces
        >>> str = 'cpe con espacios'
        >>> CPE(str, CPE.VERSION_2_2) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Malformed CPE name: it must not have whitespaces

        - TEST: an empty CPE.
        >>> str = 'cpe:/'
        >>> c = CPE(str, CPE.VERSION_2_2)

        - TEST: an empty CPE with five parts
        >>> str = 'cpe:/::::'
        >>> c = CPE(str, CPE.VERSION_2_2)

        - TEST: an empty CPE with bad part name
        >>> str = 'cpe:/b::::'
        >>> CPE(str, CPE.VERSION_2_2) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Input identifier is not a valid CPE name: Error to split CPE name parts

        - TEST: an CPE with too many components
        >>> str = 'cpe:/a:1:2:3:4:5:6:7'
        >>> CPE(str, CPE.VERSION_2_2) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Input identifier is not a valid CPE name: Error to split CPE name parts

        - TEST: an application CPE
        >>> str = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
        >>> c = CPE(str, CPE.VERSION_2_2)

        - TEST: an operating system CPE
        >>> str = 'cpe:/o:microsoft:windows_xp:::pro'
        >>> c = CPE(str, CPE.VERSION_2_2)

        - TEST: an hardware CPE
        >>> str = 'cpe:/h:nvidia'
        >>> c = CPE(str, CPE.VERSION_2_2)

        - TEST: an CPE with special characters
        >>> str = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE(str, CPE.VERSION_2_2)
        """

        super(CPE2_2, self).__init__(cpe_str)
        self._parse()

    def __len__(self):
        """
        Returns the number of components of CPE name.

        - TEST: a CPE name without components
        >>> str = "cpe:/"
        >>> c = CPE(str)
        >>> len(c)
        0

        - TEST: a CPE name with some full components
        >>> str = "cpe:/a:i4s:javas"
        >>> c = CPE(str)
        >>> len(c)
        3

        - TEST: a CPE name with some empty components
        >>> str = "cpe:/a:i4s:::javas"
        >>> c = CPE(str)
        >>> len(c)
        5

        - TEST: a CPE name with all components
        >>> str = "cpe:/a:acme:product:1.0:update2:-:en-us"
        >>> c = CPE(str)
        >>> len(c)
        7
        """

        count = self.cpe_str.count(":")
        if count > 1:
            return count
        else:
            return 0

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 2.2.
        """

        return dict.__new__(cls)

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.
        """

        return "CPE v%s: %s" % (CPE2_2.VERSION, self.cpe_str)

    def _parse(self):
        """
        Checks if CPE name is valid.

        INPUT:
            - self: CPE name object with CPE name string
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: CPE name bad-formed
        """

        # CPE name must not have whitespaces
        if (self._str.find(" ") != -1):
            msg = "Malformed CPE name: it must not have whitespaces"
            raise ValueError(msg)

        # Compilation of regular expression associated with components
        # of CPE name
        part = "?P<%s>(h|o|a)" % CPE.KEY_PART
        vendor = "?P<%s>[^:]+" % CPE.KEY_VENDOR
        product = "?P<%s>[^:]+" % CPE.KEY_PRODUCT
        version = "?P<%s>[^:]+" % CPE.KEY_VERSION
        update = "?P<%s>[^:]+" % CPE.KEY_UPDATE
        edition = "?P<%s>[^:]+" % CPE.KEY_EDITION
        language = "?P<%s>[^:]+" % CPE.KEY_LANGUAGE

        parts_pattern = "^cpe:/"
        parts_pattern += "(%s)?" % part
        parts_pattern += "(:(%s)?)?" % vendor
        parts_pattern += "(:(%s)?)?" % product
        parts_pattern += "(:(%s)?)?" % version
        parts_pattern += "(:(%s)?)?" % update
        parts_pattern += "(:(%s)?)?" % edition
        parts_pattern += "(:(%s)?)?$" % language
        parts_rxc = re.compile(parts_pattern)

        # Partitioning of CPE name
        parts_match = parts_rxc.match(self._str)

        # #####################################
        #  Validation of CPE name components  #
        # #####################################

        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        # Compilation of regular expression associated with value of CPE part
        part_value_pattern = "[\d\w\._\-~%]+"
        part_value_rxc = re.compile(part_value_pattern)

        components = dict()
        parts_match_dict = parts_match.groupdict()

        for ck in CPE.CPE_COMP_KEYS:

            if ck in parts_match_dict:
                value = parts_match.group(ck)

                if (value is None):
                    comp = UndefinedCPEComponent()
                elif (value == CPEComponent.EMPTY_VALUE):
                    comp = EmptyCPEComponent()
                else:
                    if (part_value_rxc.match(value) is None):
                        msg = "Malformed CPE name: part value must have "
                        msg += "only alphanumeric and the following characters"
                        msg += ": '.', '_', '-', '~', '%'"

                        raise ValueError(msg)
                    else:
                        comp = CPEComponent(value)
            else:
                # Component not exist in this version of CPE
                comp = UndefinedCPEComponent()

            # Identification of component name
            components[ck] = comp

        # #######################
        #  Storage of CPE name  #
        # #######################

        system = parts_match.group(CPE.KEY_PART)

        for pk in CPE.CPE_PART_KEYS:
            elements = []

            # Find out the type of system of CPE name to store its values
            if pk == CPE.KEY_HW:
                if (system == CPE.VALUE_PART_HW):
                    # CPE name corresponds with hardware system
                    elements.append(components)
            elif pk == CPE.KEY_OS:
                if (system == CPE.VALUE_PART_OS):
                    # CPE name corresponds with operating system
                    elements.append(components)
            elif pk == CPE.KEY_APP:
                if (system == CPE.VALUE_PART_APP):
                    # CPE name corresponds with application system
                    elements.append(components)

            self[pk] = elements

if __name__ == "__main__":
    import doctest
    doctest.testmod()
