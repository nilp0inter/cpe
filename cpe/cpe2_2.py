#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with version 2.2 of CPE (Common Platform Enumeration)
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
from .comp.cpecomp2_2 import CPEComponent2_2
from .comp.cpecomp2_3_wfn import CPEComponent2_3_WFN
from .comp.cpecomp_empty import CPEComponentEmpty
from .comp.cpecomp_undefined import CPEComponentUndefined

import re


class CPE2_2(CPE):
    """
    Implementation of version 2.2 of CPE specification.

    A CPE Name is a percent-encoded URI with each name
    starting with the prefix (the URI scheme name) 'cpe:'.

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

        cpe:/{part}:{vendor}:{product}:{version}:{update}:{edition}:{language}
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Version of CPE Name
    VERSION = CPE.VERSION_2_2

    ###############
    #  VARIABLES  #
    ###############

    # Compilation of regular expression associated with components
    # of CPE Name
    _part = "?P<{0}>(h|o|a)".format(CPEComponent.ATT_PART)
    _vendor = "?P<{0}>[^:]+".format(CPEComponent.ATT_VENDOR)
    _product = "?P<{0}>[^:]+".format(CPEComponent.ATT_PRODUCT)
    _version = "?P<{0}>[^:]+".format(CPEComponent.ATT_VERSION)
    _update = "?P<{0}>[^:]+".format(CPEComponent.ATT_UPDATE)
    _edition = "?P<{0}>[^:]+".format(CPEComponent.ATT_EDITION)
    _language = "?P<{0}>[^:]+".format(CPEComponent.ATT_LANGUAGE)

    _parts_pattern = "^cpe:/({0})?(:({1})?)?(:({2})?)?(:({3})?)?(:({4})?)?(:({5})?)?(:({6})?)?$".format(
        _part, _vendor, _product, _version, _update, _edition, _language)
    _parts_rxc = re.compile(_parts_pattern)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __len__(self):
        """
        Returns the number of components of CPE Name.

        :returns: count of components of CPE Name
        :rtype: int
        """

        prefix = "cpe:/"
        data = self.cpe_str[len(prefix):]

        if data == "":
            return 0

        count = data.count(CPEComponent2_2.SEPARATOR_COMP)

        return count + 1

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE Name of version 2.2.

        :param string cpe_str: CPE Name string
        :returns: CPE object of version 2.2 of CPE specification.
        :rtype: CPE2_2
        """

        return dict.__new__(cls)

    def _parse(self):
        """
        Checks if CPE Name is valid.

        :returns: None
        :exception: ValueError - bad-formed CPE Name
        """

        # CPE Name must not have whitespaces
        if (self._str.find(" ") != -1):
            msg = "Bad-formed CPE Name: it must not have whitespaces"
            raise ValueError(msg)

        # Partitioning of CPE Name
        parts_match = CPE2_2._parts_rxc.match(self._str)

        # Validation of CPE Name parts
        if (parts_match is None):
            msg = "Bad-formed CPE Name: validation of parts failed"
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
                        errmsg = "Bad-formed CPE Name: not correct value: {0}".format(
                            value)
                        raise ValueError(errmsg)
            else:
                # Component not exist in this version of CPE
                comp = CPEComponentUndefined()

            components[ck] = comp

        # Adds the components of version 2.3 of CPE not defined in version 2.2
        for ck2 in CPEComponent.CPE_COMP_KEYS_EXTENDED:
            if ck2 not in components.keys():
                components[ck2] = CPEComponentUndefined()

        # #######################
        #  Storage of CPE Name  #
        # #######################

        # If part component is undefined, store it in the part without name
        if components[CPEComponent.ATT_PART] == CPEComponentUndefined():
            system = CPEComponent.VALUE_PART_UNDEFINED
        else:
            system = parts_match.group(CPEComponent.ATT_PART)

        self._create_cpe_parts(system, components)

        # Adds the undefined parts
        for sys in CPEComponent.SYSTEM_VALUES:
            if sys != system:
                pk = CPE._system_and_parts[sys]
                self[pk] = []

    def as_wfn(self):
        """
        Returns the CPE Name as WFN string of version 2.3.
        Only shows the first seven components.

        :return: CPE Name as WFN string
        :rtype: string
        :exception: TypeError - incompatible version
        """

        wfn = []
        wfn.append(CPE2_3_WFN.CPE_PREFIX)

        for ck in CPEComponent.CPE_COMP_KEYS:
            lc = self._get_attribute_components(ck)

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

                    value = CPEComponent2_2.VALUE_EMPTY
                else:
                    value = comp.get_value()

                lc.append(value)
        return lc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe2_2.txt")
