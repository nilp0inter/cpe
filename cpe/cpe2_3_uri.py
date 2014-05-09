#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with binding style URI of version 2.3 of CPE
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
from .cpe2_3_wfn import CPE2_3_WFN
from .comp.cpecomp import CPEComponent
from .comp.cpecomp_logical import CPEComponentLogical
from .comp.cpecomp2_3_uri import CPEComponent2_3_URI
from .comp.cpecomp2_3_wfn import CPEComponent2_3_WFN
from .comp.cpecomp2_3_uri_edpacked import CPEComponent2_3_URI_edpacked
from .comp.cpecomp_anyvalue import CPEComponentAnyValue
from .comp.cpecomp_empty import CPEComponentEmpty
from .comp.cpecomp_undefined import CPEComponentUndefined
from .comp.cpecomp_notapplicable import CPEComponentNotApplicable

import re


class CPE2_3_URI(CPE2_3):
    """
    Implementation of binding style URI of version 2.3 of CPE specification.

    A CPE Name is a percent-encoded URI with each name
    starting with the prefix (the URI scheme name) 'cpe:'.

    Each platform can be broken down into many distinct parts.
    A CPE Name specifies a simple part and is used to identify
    any platform that matches the description of that part.

    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages
      the IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE Name syntax:

        cpe:/{part}:{vendor}:{product}:{version}:{update}:{edition}:{language}
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Style of CPE Name
    STYLE = CPE2_3.STYLE_URI

    ###############
    #  VARIABLES  #
    ###############

    # Compilation of regular expression associated with parts of CPE Name
    _typesys = "?P<{0}>(h|o|a)".format(CPEComponent.ATT_PART)
    _vendor = "?P<{0}>[^:]+".format(CPEComponent.ATT_VENDOR)
    _product = "?P<{0}>[^:]+".format(CPEComponent.ATT_PRODUCT)
    _version = "?P<{0}>[^:]+".format(CPEComponent.ATT_VERSION)
    _update = "?P<{0}>[^:]+".format(CPEComponent.ATT_UPDATE)
    _edition = "?P<{0}>[^:]+".format(CPEComponent.ATT_EDITION)
    _language = "?P<{0}>[^:]+".format(CPEComponent.ATT_LANGUAGE)

    _parts_pattern = "^cpe:/({0})?(:({1})?)?(:({2})?)?(:({3})?)?(:({4})?)?(:({5})?)?(:({6})?)?$".format(
        _typesys, _vendor, _product, _version, _update, _edition, _language)

    _parts_rxc = re.compile(_parts_pattern, re.IGNORECASE)

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _create_component(cls, att, value):
        """
        Returns a component with value "value".

        :param string att: Attribute name
        :param string value: Attribute value
        :returns: Component object created
        :rtype: CPEComponent
        :exception: ValueError - invalid value of attribute
        """

        if value == CPEComponent2_3_URI.VALUE_UNDEFINED:
            comp = CPEComponentUndefined()
        elif (value == CPEComponent2_3_URI.VALUE_ANY or
              value == CPEComponent2_3_URI.VALUE_EMPTY):
            comp = CPEComponentAnyValue()
        elif (value == CPEComponent2_3_URI.VALUE_NA):
            comp = CPEComponentNotApplicable()
        else:
            comp = CPEComponentNotApplicable()
            try:
                comp = CPEComponent2_3_URI(value, att)
            except ValueError:
                errmsg = "Invalid value of attribute '{0}': {1} ".format(att,
                                                                         value)
                raise ValueError(errmsg)

        return comp

    @classmethod
    def _unpack_edition(cls, value):
        """
        Unpack its elements and set the attributes in wfn accordingly.
        Parse out the five elements:

        ~ edition ~ software edition ~ target sw ~ target hw ~ other

        :param string value: Value of edition attribute
        :returns: Dictionary with parts of edition attribute
        :exception: ValueError - invalid value of edition attribute
        """

        components = value.split(CPEComponent2_3_URI.SEPARATOR_PACKED_EDITION)
        d = dict()

        ed = components[1]
        sw_ed = components[2]
        t_sw = components[3]
        t_hw = components[4]
        oth = components[5]

        ck = CPEComponent.ATT_EDITION
        d[ck] = CPE2_3_URI._create_component(ck, ed)
        ck = CPEComponent.ATT_SW_EDITION
        d[ck] = CPE2_3_URI._create_component(ck, sw_ed)
        ck = CPEComponent.ATT_TARGET_SW
        d[ck] = CPE2_3_URI._create_component(ck, t_sw)
        ck = CPEComponent.ATT_TARGET_HW
        d[ck] = CPE2_3_URI._create_component(ck, t_hw)
        ck = CPEComponent.ATT_OTHER
        d[ck] = CPE2_3_URI._create_component(ck, oth)

        return d

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
        """

        count = 0
        errmsg = "Component index of CPE Name out of range"

        packed_ed = self._pack_edition()

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                for ck in CPEComponent.CPE_COMP_KEYS:
                    if (count == i):
                        if ck == CPEComponent.ATT_EDITION:
                            empty_ed = elem.get(ck) == CPEComponentUndefined()
                            k = CPEComponent.ATT_SW_EDITION
                            empty_sw_ed = elem.get(k) == CPEComponentUndefined()
                            k = CPEComponent.ATT_TARGET_SW
                            empty_tg_sw = elem.get(k) == CPEComponentUndefined()
                            k = CPEComponent.ATT_TARGET_HW
                            empty_tg_hw = elem.get(k) == CPEComponentUndefined()
                            k = CPEComponent.ATT_OTHER
                            empty_oth = elem.get(k) == CPEComponentUndefined()

                            if (empty_ed and empty_sw_ed and empty_tg_sw and
                               empty_tg_hw and empty_oth):

                                # Edition component undefined
                                raise IndexError(errmsg)
                            else:
                                # Some part of edition component defined.
                                # Pack the edition component
                                return CPEComponent2_3_URI_edpacked(packed_ed)
                        else:
                            comp = elem.get(ck)

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
        """

        prefix = "cpe:/"
        data = self.cpe_str[len(prefix):]

        if data == "":
            return 0

        count = data.count(CPEComponent2_3_URI.SEPARATOR_COMP)

        return count + 1

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE Name of version 2.3 with URI style.

        :param string cpe_str: CPE Name string
        :returns: CPE object of version 2.3 of CPE specification with
            URI style.
        :rtype: CPE2_3_URI
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
        parts_match = CPE2_3_URI._parts_rxc.match(self._str)

        # Validation of CPE Name parts
        if (parts_match is None):
            msg = "Bad-formed CPE Name: validation of parts failed"
            raise ValueError(msg)

        components = dict()
        edition_parts = dict()

        for ck in CPEComponent.CPE_COMP_KEYS:
            value = parts_match.group(ck)

            try:
                if (ck == CPEComponent.ATT_EDITION and value is not None):
                    if value[0] == CPEComponent2_3_URI.SEPARATOR_PACKED_EDITION:
                        # Unpack the edition part
                        edition_parts = CPE2_3_URI._unpack_edition(value)
                    else:
                        comp = CPE2_3_URI._create_component(ck, value)
                else:
                    comp = CPE2_3_URI._create_component(ck, value)
            except ValueError:
                errmsg = "Bad-formed CPE Name: not correct value '{0}'".format(
                    value)
                raise ValueError(errmsg)
            else:
                components[ck] = comp

        components = dict(components, **edition_parts)

        # Adds the components of version 2.3 of CPE not defined in version 2.2
        for ck2 in CPEComponent.CPE_COMP_KEYS_EXTENDED:
            if ck2 not in components.keys():
                components[ck2] = CPEComponentUndefined()

        # Exchange the undefined values in middle attributes of CPE Name for
        # logical value ANY
        check_change = True

        # Start in the last attribute specififed in CPE Name
        for ck in CPEComponent.CPE_COMP_KEYS[::-1]:
            if ck in components:
                comp = components[ck]
                if check_change:
                    check_change = ((ck != CPEComponent.ATT_EDITION) and
                                   (comp == CPEComponentUndefined()) or
                                   (ck == CPEComponent.ATT_EDITION and
                                   (len(edition_parts) == 0)))
                elif comp == CPEComponentUndefined():
                    comp = CPEComponentAnyValue()

                components[ck] = comp

        #  Storage of CPE Name
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

    def as_wfn(self):
        """
        Returns the CPE Name as Well-Formed Name string of version 2.3.
        If edition component is not packed, only shows the first seven
        components, otherwise shows all.

        :return: CPE Name as WFN string
        :rtype: string
        :exception: TypeError - incompatible version
        """

        if self._str.find(CPEComponent2_3_URI.SEPARATOR_PACKED_EDITION) == -1:
            # Edition unpacked, only show the first seven components

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

                    v = []
                    v.append(ck)
                    v.append("=")

                    if (isinstance(comp, CPEComponentUndefined) or
                       isinstance(comp, CPEComponentEmpty)):

                        # Do not set the attribute
                        continue

                    elif isinstance(comp, CPEComponentAnyValue):

                        # Logical value any
                        v.append(CPEComponent2_3_WFN.VALUE_ANY)

                    elif isinstance(comp, CPEComponentNotApplicable):

                        # Logical value not applicable
                        v.append(CPEComponent2_3_WFN.VALUE_NA)

                    else:
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

        else:
            # Shows all components
            return super(CPE2_3_URI, self).as_wfn()

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
            errmsg = "Invalid attribute name '{0}'".format(att_name)
            raise ValueError(errmsg)

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                comp = elem.get(att_name)

                if (isinstance(comp, CPEComponentAnyValue) or
                   isinstance(comp, CPEComponentUndefined)):
                    value = CPEComponent2_3_URI.VALUE_ANY
                elif isinstance(comp, CPEComponentNotApplicable):
                    value = CPEComponent2_3_URI.VALUE_NA
                else:
                    value = comp.get_value()

                lc.append(value)
        return lc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe2_3_uri.txt")
