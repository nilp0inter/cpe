#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with Well-Formed Name (WFN) of version 2.3 of CPE
(Common Platform Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez

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
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
'''

from cpe import CPE
from cpe2_3 import CPE2_3
from cpecomp import CPEComponent
from cpecomp_logical import CPEComponentLogical
from cpecomp2_3_wfn import CPEComponent2_3_WFN
from cpecomp_undefined import CPEComponentUndefined
from cpecomp_anyvalue import CPEComponentAnyValue
from cpecomp_notapplicable import CPEComponentNotApplicable


class CPE2_3_WFN(CPE2_3):
    """
    Implementation of WFN of version 2.3 of CPE specification.

    A CPE Name is a percent-encoded WFN with each name
    starting with the prefix 'wfn:'.

    Each platform can be broken down into many distinct parts.
    A CPE Name specifies a single part and is used to identify
    any platform that matches the description of that part.
    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE name syntax: wfn:[a1=v1, a2=v2, …, an=vn]

    Only the following attributes SHALL be permitted in a WFN
    attribute-value pair:
    a. part
    b. vendor
    c. product
    d. version
    e. update
    f. edition
    g. language
    h. sw_edition
    i. target_sw
    j. target_hw
    k. other
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Style of CPE name
    STYLE = CPE2_3.STYLE_WFN

    # Prefix of CPE name with WFN style
    CPE_PREFIX = "wfn:["

    ####################
    #  OBJECT METHODS  #
    ####################

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 2.3 with WFN style.
        """

        return dict.__new__(cls)

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

        # Check prefix and initial bracket of WFN
        if self._str[0:5] != CPE2_3_WFN.CPE_PREFIX:
            errmsg = "Malformed CPE name: WFN prefix not found"
            raise ValueError(errmsg)

        # Check final backet
        if self._str[-1:] != "]":
            errmsg = "Malformed CPE name: final bracket of WFN not found"
            raise ValueError(errmsg)

        content = self._str[5:-1]

        if content != "":
            # Dictionary with pairs attribute-value
            components = dict()

            # Split WFN in components
            list_component = content.split(CPEComponent2_3_WFN.SEPARATOR_COMP)

            # Adds the defined components
            for e in list_component:
                # Whitespace not valid in component names and values
                if e.find(" ") != -1:
                    msg = "Malformed CPE name: WFN with too many whitespaces"
                    raise ValueError(msg)

                # Split pair attribute-value
                pair = e.split(CPEComponent2_3_WFN.SEPARATOR_PAIR)
                att_name = pair[0]
                att_value = pair[1]

                # Check valid attribute name
                if att_name not in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                    msg = "Malformed CPE name: invalid attribute name '{0}'".format(
                        att_name)
                    raise ValueError(msg)

                if att_name in components:
                    # Duplicate attribute
                    msg = "Malformed CPE name: attribute '{0}' repeated".format(
                        att_name)
                    raise ValueError(msg)

                if not (att_value.startswith('"') and
                        att_value.endswith('"')):

                    # Logical value
                    strUpper = att_value.upper()
                    if strUpper in CPEComponent2_3_WFN.VALUE_ANY:
                        comp = CPEComponentAnyValue()
                    elif strUpper in CPEComponent2_3_WFN.VALUE_NA:
                        comp = CPEComponentNotApplicable()
                    else:
                        msg = "Invalid logical value '{0}'".format(att_value)
                        raise ValueError(msg)

                elif att_value.startswith('"') and att_value.endswith('"'):
                    # String value
                    comp = CPEComponent2_3_WFN(att_value, att_name)

                else:
                    # Bad value
                    msg = "Malformed CPE name: invalid value '{0}'".format(
                        att_value)
                    raise ValueError(msg)

                components[att_name] = comp

            # Adds the undefined components
            for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                if ck not in components:
                    components[ck] = CPEComponentUndefined()

            # #######################
            #  Storage of CPE name  #
            # #######################

            part_comp = components[CPEComponent.ATT_PART]
            if isinstance(part_comp, CPEComponentLogical):
                elements = []
                elements.append(components)
                self[CPE.KEY_UNDEFINED] = elements
            else:
                # Create internal structure of CPE name in parts:
                # one of them is filled with identified components,
                # the rest are empty
                part_value = part_comp.get_value()
                # Del double quotes of value
                system = part_value[1:-1]
                if system in CPEComponent.SYSTEM_VALUES:
                    self._createCPEParts(system, components)
                else:
                    self._createCPEParts(CPEComponent.VALUE_PART_UNDEFINED,
                                         components)

        # Fills the empty parts of internal structure of CPE name
        for pk in CPE.CPE_PART_KEYS:
            if pk not in self.keys():
                self[pk] = []

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
            errmsg = "Invalid attribute name '{0}'".format(att_name)
            raise ValueError(errmsg)

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                comp = elem.get(att_name)

                if (isinstance(comp, CPEComponentAnyValue) or
                   isinstance(comp, CPEComponentUndefined)):
                    value = CPEComponent2_3_WFN.VALUE_ANY
                elif isinstance(comp, CPEComponentNotApplicable):
                    value = CPEComponent2_3_WFN.VALUE_NA
                else:
                    value = comp.get_value()

                lc.append(value)

        return lc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe2_3_wfn.txt")
