#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with binding style URI of version 2.3 of CPE
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
from cpecomp2_3_uri import CPEComponent2_3_URI
from cpecomp2_3_uri_edpacked import CPEComponent2_3_URI_edpacked
from cpecomp_anyvalue import CPEComponentAnyValue
from cpecomp_empty import CPEComponentEmpty
from cpecomp_undefined import CPEComponentUndefined
from cpecomp_notapplicable import CPEComponentNotApplicable

import re


class CPE2_3_URI(CPE2_3):
    """
    Implementation of binding style URI of version 2.3 of CPE specification.

    A CPE Name is a percent-encoded URI with each name
    starting with the prefix (the URI scheme name) 'cpe:'.

    Each platform can be broken down into many distinct parts.
    A CPE Name specifies a single part and is used to identify
    any platform that matches the description of that part.
    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages
      the IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE name syntax:
    cpe:/ {part} : {vendor} : {product} : {version} :
        {update} : {edition} : {language}
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Style of CPE name
    STYLE = CPE2_3.STYLE_URI

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _create_component(cls, att, value):
        """
        Returns a component with value "value".

        INPUT:
            - Value of component
        OUTPUT:
            - Component created
        EXCEPTIONS:
            - ValueError: invalid value of component
        """

        if (value == CPEComponent2_3_URI.VALUE_UNDEFINED or
           value == CPEComponent2_3_URI.VALUE_EMPTY):
            comp = CPEComponentUndefined()
        elif (value == CPEComponent2_3_URI.VALUE_ANY):
            comp = CPEComponentAnyValue()
        elif (value == CPEComponent2_3_URI.VALUE_NA):
            comp = CPEComponentNotApplicable()
        else:
            comp = CPEComponentNotApplicable()
            try:
                comp = CPEComponent2_3_URI(value, att)
            except ValueError:
                errmsg = "Invalid value of attribute '%s': %s " % (att, value)
                raise ValueError(errmsg)

        return comp

    @classmethod
    def _unpack_edition(cls, value):
        """
        Unpack its elements and set the attributes in wfn accordingly.
        Parse out the five elements.
        ~ edition ~ software edition ~ target sw ~ target hw ~ other

        INPUT:
            - value: Value of edition component
        OUTPUT:
            - Dictionary with parts of edition component
        EXCEPTIONS:
            - ValueError: invalid value of edition component
        """

        components = value.split(CPEComponent2_3_URI.PACKED_EDITION_SEPARATOR)
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
        Returns the i'th component name of CPE name.

        INPUT:
            - i: component index to find
        OUTPUT:
            - component string found
        EXCEPTIONS:
            - IndexError: index not found in CPE name
        """

        count = 0
        errmsg = "Component index of CPE name out of range"

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
        Create a new CPE name of version 2.3 with URI style.
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
                                     CPE2_3_URI.STYLE,
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
        typesys = "?P<%s>(h|o|a)" % CPEComponent.ATT_PART
        vendor = "?P<%s>[^:]+" % CPEComponent.ATT_VENDOR
        product = "?P<%s>[^:]+" % CPEComponent.ATT_PRODUCT
        version = "?P<%s>[^:]+" % CPEComponent.ATT_VERSION
        update = "?P<%s>[^:]+" % CPEComponent.ATT_UPDATE
        edition = "?P<%s>[^:]+" % CPEComponent.ATT_EDITION
        language = "?P<%s>[^:]+" % CPEComponent.ATT_LANGUAGE

        parts_pattern = "^cpe:/"
        parts_pattern += "(%s)?" % typesys
        parts_pattern += "(:(%s)?)?" % vendor
        parts_pattern += "(:(%s)?)?" % product
        parts_pattern += "(:(%s)?)?" % version
        parts_pattern += "(:(%s)?)?" % update
        parts_pattern += "(:(%s)?)?" % edition
        parts_pattern += "(:(%s)?)?$" % language
        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE name
        parts_match = parts_rxc.match(self._str)

        # Validation of CPE name parts
        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        components = dict()
        edition_parts = dict()

        for ck in CPEComponent.CPE_COMP_KEYS:
            value = parts_match.group(ck)

            try:
                if (ck == CPEComponent.ATT_EDITION and value is not None):
                    if value[0] == CPEComponent2_3_URI.PACKED_EDITION_SEPARATOR:
                        # Unpack the edition part
                        edition_parts = CPE2_3_URI._unpack_edition(value)
                    else:
                        comp = CPE2_3_URI._create_component(ck, value)
                else:
                    comp = CPE2_3_URI._create_component(ck, value)
            except ValueError:
                errmsg = "Malformed CPE name: "
                errmsg += "not correct value '%s'" % value

                raise ValueError(errmsg)
            else:
                components[ck] = comp

        components = dict(components, **edition_parts)

        # Adds the components of version 2.3 of CPE not defined in version 2.2
        for ck2 in CPEComponent.CPE_COMP_KEYS_EXTEND:
            if ck2 not in components.keys():
                components[ck2] = CPEComponentUndefined()

        # Exchange the undefined values in middle attributes of CPE name for
        # logical value ANY
        check_change = True

        # Start in the last attribute specififed in CPE name
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

        #  Storage of CPE name
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

    def as_wfn(self):
        """
        Returns the CPE name as WFN string of version 2.3.
        If edition component is not packed, only shows the first seven
        components, otherwise shows all.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - TypeError: incompatible version
        """

        if self._str.find(CPEComponent2_3_URI.PACKED_EDITION_SEPARATOR) == -1:
            # Edition unpacked, only show the first seven components

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
                       isinstance(comp, CPEComponentEmpty) or
                       isinstance(comp, CPEComponentAnyValue)):
                        v = '%s=ANY' % (ck)
                    elif isinstance(comp, CPEComponentNotApplicable):
                        v = '%s=NA' % (ck)
                    else:
                        # Get the value of WFN of component
                        v = '%s="%s"' % (ck, comp.as_wfn())

                # Append v to the WFN then add a separator.
                wfn = "%s%s%s" % (wfn, v, separator)

            # Return the WFN string
            wfn = "%s]" % wfn[0:len(wfn) - len(separator)]
            return wfn

        else:
            # Shows all components
            return super(CPE2_3_URI, self).as_wfn()

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
