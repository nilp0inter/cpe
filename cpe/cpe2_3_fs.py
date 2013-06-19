#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with binding style formatted string of version 2.3 of CPE
(Common Platform Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo

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
from cpe2_3 import CPE2_3
from cpecomp import CPEComponent
from cpecomp_logical import CPEComponentLogical
from cpecomp2_3_fs import CPEComponent2_3_FS
from cpecomp_anyvalue import CPEComponentAnyValue
from cpecomp_notapplicable import CPEComponentNotApplicable

import re


class CPE2_3_FS(CPE2_3):
    """
    Implementation of binding style formatted string of version 2.3
    of CPE specification.

    Each name starts with the prefix 'cpe:2.3:'.

    Each platform can be broken down into many distinct parts.
    A CPE Name specifies a single part and is used to identify
    any platform that matches the description of that part.
    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE name syntax:

    cpe:2.3: part : vendor : product : version : update : edition :
    language : sw_edition : target_sw : target_hw : other
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Style of CPE name
    STYLE = CPE2_3.STYLE_FS

    ####################
    #  OBJECT METHODS  #
    ####################

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE name of version 2.3 with formatted string style.
        """

        return dict.__new__(cls)

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "CPE v%s (%s): %s" % (CPE2_3.VERSION,
                                     CPE2_3_FS.STYLE,
                                     self.cpe_str)

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

        # Compilation of regular expression associated with parts of CPE name
        logical = "\\%s|\\%s" % (CPEComponent2_3_FS.VALUE_ANY,
                                 CPEComponent2_3_FS.VALUE_NA)
        typesys = "(?P<%s>(h|o|a|%s))" % (CPEComponent.ATT_PART, logical)
        aux_pattern = "(?P<%s>[^\:]+)"
        vendor = aux_pattern % (CPEComponent.ATT_VENDOR)
        product = aux_pattern % (CPEComponent.ATT_PRODUCT)
        version = aux_pattern % (CPEComponent.ATT_VERSION)
        update = aux_pattern % (CPEComponent.ATT_UPDATE)
        edition = aux_pattern % (CPEComponent.ATT_EDITION)
        language = aux_pattern % (CPEComponent.ATT_LANGUAGE)
        sw_edition = aux_pattern % (CPEComponent.ATT_SW_EDITION)
        target_sw = aux_pattern % (CPEComponent.ATT_TARGET_SW)
        target_hw = aux_pattern % (CPEComponent.ATT_TARGET_HW)
        other = aux_pattern % (CPEComponent.ATT_OTHER)

        parts_pattern = "^cpe:2.3:%s" % typesys

        aux_parts_pattern = "\:%s"
        parts_pattern += aux_parts_pattern % vendor
        parts_pattern += aux_parts_pattern % product
        parts_pattern += aux_parts_pattern % version
        parts_pattern += aux_parts_pattern % update
        parts_pattern += aux_parts_pattern % edition
        parts_pattern += aux_parts_pattern % language
        parts_pattern += aux_parts_pattern % sw_edition
        parts_pattern += aux_parts_pattern % target_sw
        parts_pattern += aux_parts_pattern % target_hw
        parts_pattern += aux_parts_pattern % other
        parts_pattern += "$"

        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE name
        parts_match = parts_rxc.match(self._str)

        # Validation of CPE name parts
        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        components = dict()
        parts_match_dict = parts_match.groupdict()

        for ck in CPEComponent.CPE_COMP_KEYS_EXTEND:
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
                        errmsg = "Malformed CPE name: "
                        errmsg += "not correct value '%s'" % value

                        raise ValueError(errmsg)
            else:
                errmsg = "Component %s should be specified" % ck
                raise ValueError(ck)

            components[ck] = comp

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
            system = parts_match.group(CPEComponent.ATT_PART)
            if system in CPEComponent.SYSTEM_VALUES:
                self._createCPEParts(system, components)
            else:
                self._createCPEParts(CPEComponent.VALUE_PART_UNDEFINED,
                                     components)

        # Fills the empty parts of internal structure of CPE name
        for pk in CPE.CPE_PART_KEYS:
            if pk not in self.keys():
                # Empty part
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
            errmsg = "Invalid attribute name '%s'" % att_name
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
