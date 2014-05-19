#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with version 1.1 of CPE (Common Platform Enumeration)
specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
"""

from .cpe import CPE
from .cpe2_3_wfn import CPE2_3_WFN
from .comp.cpecomp import CPEComponent
from .comp.cpecomp1_1 import CPEComponent1_1
from .comp.cpecomp2_3_wfn import CPEComponent2_3_WFN
from .comp.cpecomp_empty import CPEComponentEmpty
from .comp.cpecomp_undefined import CPEComponentUndefined

import re


class CPE1_1(CPE):
    """
    Implementation of version 1.1 of CPE specification.

    Basic structure of CPE Name:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE Name syntax:

        cpe:/ {hardware-part} [ / {OS-part} [ / {application-part} ] ]
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Part separator of CPE Name
    PART_SEPARATOR = "/"

    #: Separator of part elements of CPE Name
    ELEMENT_SEPARATOR = ";"

    #: Version of CPE Name
    VERSION = CPE.VERSION_1_1

    ###############
    #  VARIABLES  #
    ###############

    # Compilation of regular expression associated with parts of CPE Name
    _hw = "?P<{0}>[^{1}]+".format(CPE.KEY_HW, PART_SEPARATOR)
    _os = "?P<{0}>[^{1}]+".format(CPE.KEY_OS, PART_SEPARATOR)
    _app = "?P<{0}>[^{1}]+".format(CPE.KEY_APP, PART_SEPARATOR)

    _parts_pattern = "^cpe:/({0})?(/({1})?(/({2})?)?)?$".format(_hw, _os, _app)
    _parts_rxc = re.compile(_parts_pattern)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE Name.

        :param int i: component index to find
        :returns: component string found
        :rtype: CPEComponent
        :exception: IndexError - index not found in CPE Name

        TEST: good index

        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE1_1(str)
        >>> c[0]
        CPEComponent1_1(sun_microsystem)
        """

        count = 0
        errmsg = "Component index '{0}' of CPE Name out of range".format(
            i.__str__())

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                    # Part attribute not exist in version 1.1 of CPE.
                    # This attribute is ignored
                    if ck != CPEComponent.ATT_PART:
                        comp = elem.get(ck)
                        if (count == i):
                            if not isinstance(comp, CPEComponentUndefined):
                                return comp
                            else:
                                raise IndexError(errmsg)
                        else:
                            count += 1

        raise IndexError(errmsg)

    def __len__(self):
        """
        Returns the number of components of CPE Name.

        :returns: count of components of CPE Name
        :rtype: int

        TEST: a CPE Name with two parts (hw and os) and
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
                    for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                        # Part attribute not exist in version 1.1 of CPE.
                        # This attribute is ignored
                        if ck != CPEComponent.ATT_PART:
                            comp = elem.get(ck)
                            if not isinstance(comp, CPEComponentUndefined):
                                count += 1

        return count

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE Name of version 1.1.

        :param string cpe_str: CPE Name string
        :returns: CPE object of version 1.1 of CPE specification.
        :rtype: CPE1_1
        """

        return dict.__new__(cls)

    def _parse(self):
        """
        Checks if the CPE Name is valid.

        :returns: None
        :exception: ValueError - bad-formed CPE Name
        """

        # CPE Name must not have whitespaces
        if (self.cpe_str.find(" ") != -1):
            errmsg = "Bad-formed CPE Name: it must not have whitespaces"
            raise ValueError(errmsg)

        # Partitioning of CPE Name in parts
        parts_match = CPE1_1._parts_rxc.match(self.cpe_str)

        # ################################
        #  Validation of CPE Name parts  #
        # ################################

        if (parts_match is None):
            errmsg = "Bad-formed CPE Name: not correct definition of CPE Name parts"
            raise ValueError(errmsg)

        CPE_PART_KEYS = (CPE.KEY_HW, CPE.KEY_OS, CPE.KEY_APP)

        for pk in CPE_PART_KEYS:
            # Get part content
            part = parts_match.group(pk)
            elements = []

            if (part is not None):
                # Part of CPE Name defined

                # ###############################
                #  Validation of part elements  #
                # ###############################

                # semicolon (;) is used to separate the part elements
                for part_elem in part.split(CPE1_1.ELEMENT_SEPARATOR):
                    j = 1

                    # ####################################
                    #  Validation of element components  #
                    # ####################################

                    components = dict()

                    # colon (:) is used to separate the element components
                    for elem_comp in part_elem.split(CPEComponent1_1.SEPARATOR_COMP):
                        comp_att = CPEComponent.ordered_comp_parts[j]

                        if elem_comp == CPEComponent1_1.VALUE_EMPTY:
                            comp = CPEComponentEmpty()
                        else:
                            try:
                                comp = CPEComponent1_1(elem_comp, comp_att)
                            except ValueError:
                                errmsg = "Bad-formed CPE Name: not correct value: {0}".format(
                                    elem_comp)
                                raise ValueError(errmsg)

                        # Identification of component name
                        components[comp_att] = comp

                        j += 1

                    # Adds the components of version 2.3 of CPE not defined
                    # in version 1.1
                    for idx in range(j, len(CPEComponent.ordered_comp_parts)):
                        comp_att = CPEComponent.ordered_comp_parts[idx]
                        components[comp_att] = CPEComponentUndefined()

                    # Get the type of system associated with CPE Name and
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
        Returns the CPE Name as Well-Formed Name string of version 2.3.

        :return: CPE Name as WFN string
        :rtype: string
        :exception: TypeError - incompatible version
        """

        wfn = []
        wfn.append(CPE2_3_WFN.CPE_PREFIX)

        for ck in CPEComponent.CPE_COMP_KEYS:
            lc = self._get_attribute_components(ck)

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE Name
                errmsg = "Incompatible version {0} with WFN".format(
                    self.VERSION)
                raise TypeError(errmsg)

            else:
                comp = lc[0]

                if (isinstance(comp, CPEComponentUndefined) or
                   isinstance(comp, CPEComponentEmpty)):

                    # Do not set the attribute
                    continue
                else:
                    v = []
                    v.append(ck)
                    v.append("=")

                    # Get the value of WFN of component
                    v.append('"')
                    v.append(comp.as_wfn())
                    v.append('"')

                    # Append v to the WFN and add a separator
                    wfn.append("".join(v))
                    wfn.append(CPEComponent2_3_WFN.SEPARATOR_COMP)

        # Del the last separator
        wfn = wfn[:-1]

        # Return the WFN string
        wfn.append(CPE2_3_WFN.CPE_SUFFIX)

        return "".join(wfn)

    def get_attribute_values(self, att_name):
        """
        Returns the values of attribute "att_name" of CPE Name.
        By default a only element in each part.

        :param string att_name: Attribute name to get
        :returns: List of attribute values
        :rtype: list
        :exception: ValueError - invalid attribute name
        """

        lc = []

        if not CPEComponent.is_valid_attribute(att_name):
            errmsg = "Invalid attribute name: {0}".format(att_name)
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
