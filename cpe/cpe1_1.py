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
from cpecomp_empty import CPEComponentEmpty
from cpecomp_undefined import CPEComponentUndefined

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

    # Separator of components of a part of CPE name
    COMP_SEPARATOR = ":"
    # Separator of three part of CPE name
    PART_SEPARATOR = "/"

    # Version of CPE name
    VERSION = CPE.VERSION_1_1

    ####################
    #  OBJECT METHODS  #
    ####################

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE name.

        INPUT:
            - i: component index to find
        OUTPUT:
            - component string found
        EXCEPTIONS:
            - IndexError: index not found in CPE name
            - KeyError: not correct internal dictionary of CPE object

        - TEST: good index
        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE1_1(str)
        >>> c[0]
        CPEComponent1_1(sun_microsystem)
        """

        count = 0
        nullcomp = CPEComponentUndefined()
        errmsg = "Component index '%s' of CPE name out of range" % i

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                for ck in CPEComponent.CPE_COMP_KEYS_EXTEND:
                    # Part value not exist as attribute in version 1.1 of CPE
                    if ck != CPEComponent.ATT_PART:
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
            - cpe_str: CPE name as string
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: Bad-formed CPE name

        - TEST: OS part with operator OR (two subcomponents)
        >>> str = 'cpe://microsoft:windows:xp!vista'
        >>> c = CPE1_1(str)
        """

        super(CPE1_1, self).__init__(cpe_str)

    def __len__(self):
        """
        Returns the number of components of CPE name.

        - TEST: a CPE name with two parts (hw and os) and
        some elements empty and with values
        >>> str = "cpe:/cisco::3825/cisco:ios:12.3:enterprise"
        >>> c = CPE1_1(str)
        >>> len(c)
        7
        """

        count = 0

        for part in CPE.CPE_PART_KEYS:
            if part != CPE.KEY_UNDEFINED:
                elements = self.get(part)
                for elem in elements:
                    for ck in CPEComponent.CPE_COMP_KEYS_EXTEND:
                        if ck != CPEComponent.ATT_PART:
                            comp = elem.get(ck)
                            if not isinstance(comp, CPEComponentUndefined):
                                count += 1

        return count

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 1.1.
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
        >>> str = 'cpe:///microsoft:ie:10.0'
        >>> c = CPE1_1(str, CPE.VERSION_1_1)
        >>> print c
        CPE v1.1: cpe:///microsoft:ie:10.0
        """

        return "CPE v%s: %s" % (CPE1_1.VERSION, self.cpe_str)

    def _parse(self):
        """
        Checks if the CPE name is valid.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: bad-formed CPE name
        """

        # CPE name must not have whitespaces
        if (self.cpe_str.find(" ") != -1):
            errmsg = "Malformed CPE name: it must not have whitespaces"
            raise ValueError(errmsg)

        # Compilation of regular expression associated with parts of CPE name
        hw = "?P<%s>[^%s]+" % (CPE.KEY_HW, CPE1_1.PART_SEPARATOR)
        os = "?P<%s>[^%s]+" % (CPE.KEY_OS, CPE1_1.PART_SEPARATOR)
        app = "?P<%s>[^%s]+" % (CPE.KEY_APP, CPE1_1.PART_SEPARATOR)

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

        CPE_PART_KEYS = [CPE.KEY_HW, CPE.KEY_OS, CPE.KEY_APP]

        for pk in CPE_PART_KEYS:
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
                    for elem_comp in part_elem.split(CPE1_1.COMP_SEPARATOR):
                        comp_att = CPEComponent.ORDERED_COMP_PARTS[j]
                        if elem_comp == CPEComponent1_1.VALUE_EMPTY:
                            comp = CPEComponentEmpty()
                        else:
                            try:
                                comp = CPEComponent1_1(elem_comp, comp_att)
                            except ValueError:
                                errmsg = "Malformed CPE name: "
                                errmsg += "not correct value '%s'" % elem_comp

                                raise ValueError(errmsg)

                        # Identification of component name
                        components[comp_att] = comp

                        j += 1

                    # Adds the components of version 2.3 of CPE not defined
                    # in version 1.1
                    for idx in range(j, len(CPEComponent.ORDERED_COMP_PARTS)):
                        comp_att = CPEComponent.ORDERED_COMP_PARTS[idx]
                        components[comp_att] = CPEComponentUndefined()

                    # Get the type of system associated with CPE name and
                    # store it in element as component
                    if (pk == CPE.KEY_HW):
                        components[CPEComponent.ATT_PART] = CPEComponent1_1(
                            CPEComponent.VALUE_PART_HW, CPEComponent.ATT_PART)
                    elif (pk == CPE.KEY_OS):
                        components[CPEComponent.ATT_PART] = CPEComponent1_1(
                            CPEComponent.VALUE_PART_OS, CPEComponent.ATT_PART)
                    elif (pk == CPE.KEY_APP):
                        components[CPEComponent.ATT_PART] = CPEComponent1_1(
                            CPEComponent.VALUE_PART_APP, CPEComponent.ATT_PART)

                    # Store the element identified
                    elements.append(components)

            # Store the part identified
            self[pk] = elements

        self[CPE.KEY_UNDEFINED] = []

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

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE name
                errmsg = "Incompatible version %s with WFN" % self.VERSION
                raise TypeError(errmsg)

            else:
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

                    value = CPEComponent1_1.VALUE_EMPTY
                else:
                    value = comp.get_value()

                lc.append(value)
        return lc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe1_1.txt")
