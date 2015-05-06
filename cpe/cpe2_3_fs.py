#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with binding style formatted string of version 2.3 of CPE
(Common Platform Enumeration) specification.

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
from .cpe2_3 import CPE2_3
from .comp.cpecomp import CPEComponent
from .comp.cpecomp_logical import CPEComponentLogical
from .comp.cpecomp2_3_fs import CPEComponent2_3_FS
from .comp.cpecomp_anyvalue import CPEComponentAnyValue
from .comp.cpecomp_notapplicable import CPEComponentNotApplicable

import re


class CPE2_3_FS(CPE2_3):
    """
    Implementation of binding style formatted string of version 2.3
    of CPE specification.

    Each name starts with the prefix 'cpe:2.3:'.

    Each platform can be broken down into many distinct parts.
    A CPE Name specifies a simple part and is used to identify
    any platform that matches the description of that part.

    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE Name syntax:

        cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Style of CPE Name
    STYLE = CPE2_3.STYLE_FS

    ###############
    #  VARIABLES  #
    ###############
    COMP_RE = "(?P<{0}>.*?)(?<!\\\\)"

    # Compilation of regular expression associated with parts of CPE Name
    _logical = "\\{0}|\\{1}".format(
        CPEComponent2_3_FS.VALUE_ANY, CPEComponent2_3_FS.VALUE_NA)
    _typesys = "(?P<{0}>(h|o|a|{1}))".format(
        CPEComponent.ATT_PART, _logical)
    _vendor = COMP_RE.format(CPEComponent.ATT_VENDOR)
    _product = COMP_RE.format(CPEComponent.ATT_PRODUCT)
    _version = COMP_RE.format(CPEComponent.ATT_VERSION)
    _update = COMP_RE.format(CPEComponent.ATT_UPDATE)
    _edition = COMP_RE.format(CPEComponent.ATT_EDITION)
    _language = COMP_RE.format(CPEComponent.ATT_LANGUAGE)
    _sw_edition = COMP_RE.format(CPEComponent.ATT_SW_EDITION)
    _target_sw = COMP_RE.format(CPEComponent.ATT_TARGET_SW)
    _target_hw = COMP_RE.format(CPEComponent.ATT_TARGET_HW)
    _other = COMP_RE.format(CPEComponent.ATT_OTHER)

    _parts_pattern = "^cpe:2.3:{0}\:{1}\:{2}\:{3}\:{4}\:{5}\:{6}\:{7}\:{8}\:{9}\:{10}$".format(
        _typesys, _vendor, _product, _version, _update, _edition,
        _language, _sw_edition, _target_sw, _target_hw, _other)

    _parts_rxc = re.compile(_parts_pattern, re.IGNORECASE)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __len__(self):
        """
        Returns the number of components of CPE Name. This CPE Name always
        have eleven components set.

        :returns: count of components of CPE Name
        :rtype: int
        """

        return 11

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE Name of version 2.3 with formatted string style.

        :param string cpe_str: CPE Name string
        :returns: CPE object of version 2.3 of CPE specification with
            formatted string style.
        :rtype: CPE2_3_FS
        """

        return dict.__new__(cls)

    def _parse(self):
        """
        Checks if the CPE Name is valid.

        :returns: None
        :exception: ValueError - bad-formed CPE Name
        """

        # CPE Name must not have whitespaces
        if (self._str.find(" ") != -1):
            msg = "Bad-formed CPE Name: it must not have whitespaces"
            raise ValueError(msg)

        # Partitioning of CPE Name
        parts_match = CPE2_3_FS._parts_rxc.match(self._str)

        # Validation of CPE Name parts
        if (parts_match is None):
            msg = "Bad-formed CPE Name: validation of parts failed"
            raise ValueError(msg)

        components = dict()
        parts_match_dict = parts_match.groupdict()

        for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
            if ck in parts_match_dict:
                value = parts_match.group(ck)

                if (value == CPEComponent2_3_FS.VALUE_ANY):
                    comp = CPEComponentAnyValue()
                elif (value == CPEComponent2_3_FS.VALUE_NA):
                    comp = CPEComponentNotApplicable()
                else:
                    try:
                        comp = CPEComponent2_3_FS(value, ck)
                    except ValueError:
                        errmsg = "Bad-formed CPE Name: not correct value: {0}".format(
                            value)
                        raise ValueError(errmsg)
            else:
                errmsg = "Component {0} should be specified".format(ck)
                raise ValueError(ck)

            components[ck] = comp

        # #######################
        #  Storage of CPE Name  #
        # #######################

        part_comp = components[CPEComponent.ATT_PART]
        if isinstance(part_comp, CPEComponentLogical):
            elements = []
            elements.append(components)
            self[CPE.KEY_UNDEFINED] = elements
        else:
            # Create internal structure of CPE Name in parts:
            # one of them is filled with identified components,
            # the rest are empty
            system = parts_match.group(CPEComponent.ATT_PART)
            if system in CPEComponent.SYSTEM_VALUES:
                self._create_cpe_parts(system, components)
            else:
                self._create_cpe_parts(CPEComponent.VALUE_PART_UNDEFINED,
                                       components)

        # Fills the empty parts of internal structure of CPE Name
        for pk in CPE.CPE_PART_KEYS:
            if pk not in self.keys():
                # Empty part
                self[pk] = []

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

                if isinstance(comp, CPEComponentAnyValue):
                    value = CPEComponent2_3_FS.VALUE_ANY

                elif isinstance(comp, CPEComponentNotApplicable):
                    value = CPEComponent2_3_FS.VALUE_NA

                else:
                    value = comp.get_value()

                lc.append(value)
        return lc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe2_3_fs.txt")
