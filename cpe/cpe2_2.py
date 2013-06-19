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
from cpecomp2_2 import CPEComponent2_2
from cpecomp_empty import CPEComponentEmpty
from cpecomp_undefined import CPEComponentUndefined

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

    # Separator of components of a part of CPE name
    COMP_SEPARATOR = ":"

    # Version of CPE name
    VERSION = CPE.VERSION_2_2

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str, *args, **kwargs):
        """
        Checks if input CPE name is valid and,
        if so, stores its parts, elements and components.

        INPUT:
            - cpe_str: CPE name as string
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: Bad-formed CPE name

        - TEST: a CPE name with some full components
        >>> str = 'cpe:/a:i4s:javas'
        >>> c = CPE2_2(str)
        """

        super(CPE2_2, self).__init__(cpe_str)

    def __len__(self):
        """
        Returns the number of components of CPE name.
        """

        prefix = "cpe:/"
        data = self.cpe_str[len(prefix):]

        if data == "":
            return 0

        count = data.count(":")

        return count + 1

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 2.2.
        """

        return dict.__new__(cls)

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string

        TEST:
        >>> str = 'cpe:/a:i4s:javas'
        >>> c = CPE2_2(str, CPE.VERSION_2_2)
        >>> print c
        CPE v2.2: cpe:/a:i4s:javas
        """

        return "CPE v%s: %s" % (CPE2_2.VERSION, self.cpe_str)

    def _parse(self):
        """
        Checks if CPE name is valid.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: bad-formed CPE name
        """

        # CPE name must not have whitespaces
        if (self._str.find(" ") != -1):
            msg = "Malformed CPE name: it must not have whitespaces"
            raise ValueError(msg)

        # Compilation of regular expression associated with components
        # of CPE name
        part = "?P<%s>(h|o|a)" % CPEComponent.ATT_PART
        vendor = "?P<%s>[^:]+" % CPEComponent.ATT_VENDOR
        product = "?P<%s>[^:]+" % CPEComponent.ATT_PRODUCT
        version = "?P<%s>[^:]+" % CPEComponent.ATT_VERSION
        update = "?P<%s>[^:]+" % CPEComponent.ATT_UPDATE
        edition = "?P<%s>[^:]+" % CPEComponent.ATT_EDITION
        language = "?P<%s>[^:]+" % CPEComponent.ATT_LANGUAGE

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

        # Validation of CPE name parts
        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        components = dict()
        parts_match_dict = parts_match.groupdict()

        for ck in CPEComponent.CPE_COMP_KEYS:
            if ck in parts_match_dict:
                value = parts_match.group(ck)

                if (value == CPEComponent2_2.VALUE_UNDEFINED):
                    comp = CPEComponentUndefined()
                elif (value == CPEComponent2_2.VALUE_EMPTY):
                    comp = CPEComponentEmpty()
                else:
                    try:
                        comp = CPEComponent2_2(value, ck)
                    except ValueError:
                        errmsg = "Malformed CPE name: "
                        errmsg += "not correct value '%s'" % value

                        raise ValueError(errmsg)
            else:
                # Component not exist in this version of CPE
                comp = CPEComponentUndefined()

            components[ck] = comp

        # Adds the components of version 2.3 of CPE not defined in version 2.2
        for ck2 in CPEComponent.CPE_COMP_KEYS_EXTEND:
            if ck2 not in components.keys():
                components[ck2] = CPEComponentUndefined()

        # #######################
        #  Storage of CPE name  #
        # #######################

        # If part component is undefined, store it in the part without name
        if components[CPEComponent.ATT_PART] == CPEComponentUndefined():
            system = CPEComponent.VALUE_PART_UNDEFINED
        else:
            system = parts_match.group(CPEComponent.ATT_PART)

        self._createCPEParts(system, components)

        # Adds the undefined parts
        for sys in CPEComponent.SYSTEM_VALUES:
            if sys != system:
                pk = CPE.SYSTEM_AND_PARTS[sys]
                self[pk] = []

    def as_wfn(self):
        """
        Returns the CPE name as WFN string of version 2.3.
        Only shows the first seven components.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - TypeError: incompatible version
        """

        separator = ", "
        wfn = "wfn:["

        for ck in CPEComponent.CPE_COMP_KEYS:
            lc = self._getAttributeComponents(ck)

            comp = lc[0]
            if (isinstance(comp, CPEComponentUndefined) or
               isinstance(comp, CPEComponentEmpty)):
                v = '%s=ANY' % (ck)
            else:
                # Get the value of WFN of component
                v = '%s="%s"' % (ck, comp.as_wfn())

            # Append v to the WFN then add a separator.
            wfn = "%s%s%s" % (wfn, v, separator)

        # Return the WFN string
        wfn = "%s]" % wfn[0:len(wfn) - len(separator)]
        return wfn

    def getAttributeValues(self, att_name):
        """
        Returns the values of attribute "att_name" of CPE name.
        By default a only element in each part.

        INPUT:
            - att_name: Attribute name to get
        OUTPUT:
            - List of attribute values
        """

        lc = []

        if not CPEComponent.is_valid_attribute(att_name):
            errmsg = "Invalid attribute name '%s'" % att_name
            raise ValueError(errmsg)

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                comp = elem.get(att_name)

                if (isinstance(comp, CPEComponentEmpty) or
                   isinstance(comp, CPEComponentUndefined)):

                    value = CPEComponent2_2.VALUE_EMPTY
                else:
                    value = comp.get_value()

                lc.append(value)
        return lc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe2_2.txt")
