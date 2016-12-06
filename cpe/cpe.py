#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module contains the common characteristics of
any type of CPE Name, associated with a version of Common Platform
Enumeration (CPE) specification.

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
from collections import OrderedDict

from .comp.cpecomp import CPEComponent
from .comp.cpecomp2_3_uri import CPEComponent2_3_URI
from .comp.cpecomp2_3_wfn import CPEComponent2_3_WFN
from .comp.cpecomp2_3_fs import CPEComponent2_3_FS
from .comp.cpecomp2_3_uri_edpacked import CPEComponent2_3_URI_edpacked
from .comp.cpecomp_logical import CPEComponentLogical
from .comp.cpecomp_empty import CPEComponentEmpty
from .comp.cpecomp_anyvalue import CPEComponentAnyValue
from .comp.cpecomp_undefined import CPEComponentUndefined
from .comp.cpecomp_notapplicable import CPEComponentNotApplicable


class CPE(dict):
    """
    Represents a generic CPE Name compatible with
    all versions of CPE specification.

    Parts of CPE are stored in a dictionary.

    CPE structure (dictionary):
        └─ part {hw, os, sw, undefined}
            └─ element list (list)
                └─ component list (dictionary)
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants used to paint the representation of CPE Name
    _PREFIX_ELEM = "   ["
    _PREFIX_ELEMENTS = " ["
    _SUFFIX_ELEM = "   ]"
    _SUFFIX_ELEMENTS = " ]"

    # Type of systems included in CPE specification

    #: Type of system "application"
    KEY_APP = "app"
    #: Type of system "hardware"
    KEY_HW = "hw"
    #: Type of system "operating system"
    KEY_OS = "os"
    #: Undefined type of system
    KEY_UNDEFINED = "undef"

    #: List of keys associated with the types of system
    #: included in CPE specification
    CPE_PART_KEYS = (KEY_HW, KEY_OS, KEY_APP, KEY_UNDEFINED)

    # Constants of possible versions of CPE specification

    #: Version 1.1 of CPE specification
    VERSION_1_1 = "1.1"
    #: Version 2.2 of CPE specification
    VERSION_2_2 = "2.2"
    #: Version 2.3 of CPE specification
    VERSION_2_3 = "2.3"
    #: Version not set
    VERSION_UNDEFINED = "undefined"

    #: Version of CPE Name
    VERSION = VERSION_UNDEFINED

    ###############
    #  VARIABLES  #
    ###############

    #: Dictionary with the relation between the values of "part"
    #: component and the part name in internal structure of CPE Name
    _system_and_parts = OrderedDict((
        (CPEComponent.VALUE_PART_HW, KEY_HW),
        (CPEComponent.VALUE_PART_OS, KEY_OS),
        (CPEComponent.VALUE_PART_APP, KEY_APP),
        (CPEComponent.VALUE_PART_UNDEFINED, KEY_UNDEFINED)))

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _trim(cls, s):
        """
        Remove trailing colons from the URI back to the first non-colon.

        :param string s: input URI string
        :returns: URI string with trailing colons removed
        :rtype: string

        TEST: trailing colons necessary

        >>> s = '1:2::::'
        >>> CPE._trim(s)
        '1:2'

        TEST: trailing colons not necessary

        >>> s = '1:2:3:4:5:6'
        >>> CPE._trim(s)
        '1:2:3:4:5:6'
        """
        reverse = s[::-1]
        idx = 0
        for i in range(0, len(reverse)):
            if reverse[i] == ":":
                idx += 1
            else:
                break

        # Return the substring after all trailing colons,
        # reversed back to its original character order.
        new_s = reverse[idx: len(reverse)]
        return new_s[::-1]

    ####################
    #  OBJECT METHODS  #
    ####################

    def __eq__(self, other):
        """
        Returns True if other (first element of operation) and
        self (second element of operation) are equal CPE Names,
        false otherwise.

        :param CPE other: CPE Name to compare
        :returns: True if other == self, False otherwise
        :rtype: boolean
        """

        for part in CPE.CPE_PART_KEYS:
            elements_self = self.get(part)
            elements_other = other.get(part)

            len_self = len(elements_self)
            if len_self != len(elements_other):
                return False

            for i in range(0, len(elements_self)):
                elem_self = elements_self[i]
                elem_other = elements_other[i]

                for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                    if (elem_self[ck] != elem_other[ck]):
                        return False

        return True

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE Name.

        :param int i: component index to find
        :returns: component string found
        :rtype: CPEComponent
        :exception: IndexError - index not found in CPE Name

        TEST: good index

        >>> str = 'cpe:///sun_microsystem:sun@os:5.9:#update'
        >>> c = CPE(str)
        >>> c[0]
        CPEComponent1_1(sun_microsystem)
        """

        count = 0
        errmsg = "Component index of CPE Name out of range"

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                    comp = elem.get(ck)
                    if (count == i):
                        if not isinstance(comp, CPEComponentUndefined):
                            return comp
                        else:
                            raise IndexError(errmsg)
                    else:
                        count += 1

        raise IndexError(errmsg)

    def __init__(self, cpe_str, *args, **kwargs):
        """
        Store the CPE Name.

        :param string cpe_str: CPE Name
        :returns: None
        """

        # The original CPE Name as string
        self.cpe_str = cpe_str

        # Store CPE Name in lower-case letters:
        # CPE Names are case-insensitive.
        # To reduce potential for confusion,
        # all CPE Names should be written in lowercase.
        self._str = cpe_str.lower()

        # Check if CPE Name is correct
        self._parse()

    def __len__(self):
        """
        Returns the number of components of CPE Name.

        :returns: count of components of CPE Name
        :rtype: int

        TEST: a CPE Name with two parts (hw and os) and
        some elements empty and with values

        >>> str = "cpe:/cisco::3825/cisco:ios:12.3"
        >>> c = CPE(str)
        >>> len(c)
        6
        """

        count = 0

        for part in CPE.CPE_PART_KEYS:
            elements = self.get(part)
            for elem in elements:
                for ck in CPEComponent.CPE_COMP_KEYS_EXTENDED:
                    comp = elem.get(ck)
                    if not isinstance(comp, CPEComponentUndefined):
                        count += 1

        return count

    def __new__(cls, cpe_str, version=None, *args, **kwargs):
        """
        Generator of CPE Names.

        :param string cpe_str: CPE Name string
        :param string version: version of CPE specification of CPE Name
        :returns: CPE object with version of CPE detected correctly
        :rtype: CPE
        :exception: NotImplementedError - incorrect CPE Name or
            version of CPE not implemented

        This class implements the factory pattern, that is,
        this class centralizes the creation of objects of a particular
        CPE version, hiding the user the requested object instance.
        """

        from .cpe1_1 import CPE1_1
        from .cpe2_2 import CPE2_2
        from .cpe2_3 import CPE2_3

        # List of implemented versions of CPE Names
        #
        # Note: Order matters here, because some regexp can parse
        #       multiple versions at once.
        _CPE_VERSIONS = OrderedDict((
            (CPE.VERSION_2_3, CPE2_3),
            (CPE.VERSION_2_2, CPE2_2),
            (CPE.VERSION_1_1, CPE1_1),))

        errmsg = 'Version of CPE not implemented'

        if version is None:
            # Detect CPE version of input CPE Name
            for v in _CPE_VERSIONS:
                try:
                    # Validate CPE Name
                    c = _CPE_VERSIONS[v](cpe_str)
                except ValueError:
                    # Test another version
                    continue
                except NotImplementedError:
                    # Test another version
                    continue
                else:
                    # Version detected
                    return c

            raise NotImplementedError(errmsg)

        elif version in _CPE_VERSIONS:
            # Correct input version, validate CPE Name
            return _CPE_VERSIONS[version](cpe_str)
        else:
            # Invalid CPE version
            raise NotImplementedError(errmsg)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE Name.

        :returns: Representation of CPE Name as string
        :rtype: string
        """

        txtParts = []

        for pk in CPE.CPE_PART_KEYS:
            txtParts.append(pk)

            txtElements = []
            txtElements.append(CPE._PREFIX_ELEMENTS)

            elements = self.get(pk)

            for elem in elements:
                txtElem = []
                txtElem.append(CPE._PREFIX_ELEM)

                for i in range(0, len(CPEComponent.CPE_COMP_KEYS_EXTENDED)):
                    txtComp = []
                    ck = CPEComponent.ordered_comp_parts.get(i)
                    comp = elem.get(ck)

                    if isinstance(comp, CPEComponentLogical):
                        value = comp.__str__()
                    else:
                        value = comp.get_value()

                    txtComp.append("     ")
                    txtComp.append(ck)
                    txtComp.append(" = ")
                    txtComp.append(value)

                    txtElem.append("".join(txtComp))

                if len(txtElem) == 1:
                    # There are no components
                    txtElem = []
                    txtElem.append(" []")
                else:
                    txtElem.append(CPE._SUFFIX_ELEM)

                txtElements.append("\n".join(txtElem))

            if len(txtElements) == 1:
                # There are no elements
                txtElements = []
                txtElements.append(" []")
            else:
                txtElements.append(CPE._SUFFIX_ELEMENTS)

            txtParts.append("\n".join(txtElements))

        return "\n".join(txtParts)

    def __str__(self):
        """
        Returns a human-readable representation of CPE Name.

        :returns: Representation of CPE Name as string
        :rtype: string
        """

        return "CPE v{0}: {1}".format(self.VERSION, self.cpe_str)

    def _create_cpe_parts(self, system, components):
        """
        Create the structure to store the input type of system associated
        with components of CPE Name (hardware, operating system and software).

        :param string system: type of system associated with CPE Name
        :param dict components: CPE Name components to store
        :returns: None
        :exception: KeyError - incorrect system
        """

        if system not in CPEComponent.SYSTEM_VALUES:
            errmsg = "Key '{0}' is not exist".format(system)
            raise ValueError(errmsg)

        elements = []
        elements.append(components)

        pk = CPE._system_and_parts[system]
        self[pk] = elements

    def _get_attribute_components(self, att):
        """
        Returns the component list of input attribute.

        :param string att: Attribute name to get
        :returns: List of Component objects of the attribute in CPE Name
        :rtype: list
        :exception: ValueError - invalid attribute name
        """

        lc = []

        if not CPEComponent.is_valid_attribute(att):
            errmsg = "Invalid attribute name '{0}' is not exist".format(att)
            raise ValueError(errmsg)

        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                lc.append(elem.get(att))

        return lc

    def _pack_edition(self):
        """
        Pack the values of the five arguments into the simple edition
        component. If all the values are blank, just return a blank.

        :returns: "edition", "sw_edition", "target_sw", "target_hw" and "other"
            attributes packed in a only value
        :rtype: string
        :exception: TypeError - incompatible version with pack operation
        """

        COMP_KEYS = (CPEComponent.ATT_EDITION,
                     CPEComponent.ATT_SW_EDITION,
                     CPEComponent.ATT_TARGET_SW,
                     CPEComponent.ATT_TARGET_HW,
                     CPEComponent.ATT_OTHER)

        separator = CPEComponent2_3_URI_edpacked.SEPARATOR_COMP

        packed_ed = []
        packed_ed.append(separator)

        for ck in COMP_KEYS:
            lc = self._get_attribute_components(ck)
            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE Name
                errmsg = "Incompatible version {0} with URI".format(
                    self.VERSION)
                raise TypeError(errmsg)

            comp = lc[0]
            if (isinstance(comp, CPEComponentUndefined) or
               isinstance(comp, CPEComponentEmpty) or
               isinstance(comp, CPEComponentAnyValue)):

                value = ""
            elif (isinstance(comp, CPEComponentNotApplicable)):
                value = CPEComponent2_3_URI.VALUE_NA
            else:
                # Component has some value; transform this original value
                # in URI value
                value = comp.as_uri_2_3()

            # Save the value of edition attribute
            if ck == CPEComponent.ATT_EDITION:
                ed = value

            # Packed the value of component
            packed_ed.append(value)
            packed_ed.append(separator)

        # Del the last separator
        packed_ed_str = "".join(packed_ed[:-1])

        only_ed = []
        only_ed.append(separator)
        only_ed.append(ed)
        only_ed.append(separator)
        only_ed.append(separator)
        only_ed.append(separator)
        only_ed.append(separator)

        only_ed_str = "".join(only_ed)

        if (packed_ed_str == only_ed_str):
            # All the extended attributes are blank,
            # so don't do any packing, just return ed
            return ed
        else:
            # Otherwise, pack the five values into a simple string
            # prefixed and internally delimited with the tilde
            return packed_ed_str

    def as_dict(self):
        """
        Returns the CPE Name dict as string.

        :returns: CPE Name dict as string
        :rtype: string
        """

        return super(CPE, self).__str__()

    def as_uri_2_3(self):
        """
        Returns the CPE Name as URI string of version 2.3.

        :returns: CPE Name as URI string of version 2.3
        :rtype: string
        :exception: TypeError - incompatible version
        """

        uri = []
        uri.append("cpe:/")

        ordered_comp_parts = {
            0: CPEComponent.ATT_PART,
            1: CPEComponent.ATT_VENDOR,
            2: CPEComponent.ATT_PRODUCT,
            3: CPEComponent.ATT_VERSION,
            4: CPEComponent.ATT_UPDATE,
            5: CPEComponent.ATT_EDITION,
            6: CPEComponent.ATT_LANGUAGE}

        # Indicates if the previous component must be set depending on the
        # value of current component
        set_prev_comp = False
        prev_comp_list = []

        for i in range(0, len(ordered_comp_parts)):
            ck = ordered_comp_parts[i]
            lc = self._get_attribute_components(ck)

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE Name
                errmsg = "Incompatible version {0} with URI".format(
                    self.VERSION)
                raise TypeError(errmsg)

            if ck == CPEComponent.ATT_EDITION:
                # Call the pack() helper function to compute the proper
                # binding for the edition element
                v = self._pack_edition()
                if not v:
                    set_prev_comp = True
                    prev_comp_list.append(CPEComponent2_3_URI.VALUE_ANY)
                    continue
            else:
                comp = lc[0]

                if (isinstance(comp, CPEComponentEmpty) or
                   isinstance(comp, CPEComponentAnyValue)):

                    # Logical value any
                    v = CPEComponent2_3_URI.VALUE_ANY

                elif isinstance(comp, CPEComponentNotApplicable):

                    # Logical value not applicable
                    v = CPEComponent2_3_URI.VALUE_NA
                elif isinstance(comp, CPEComponentUndefined):
                    set_prev_comp = True
                    prev_comp_list.append(CPEComponent2_3_URI.VALUE_ANY)
                    continue
                else:
                    # Get the value of component encoded in URI
                    v = comp.as_uri_2_3()

            # Append v to the URI and add a separator
            uri.append(v)
            uri.append(CPEComponent2_3_URI.SEPARATOR_COMP)

            if set_prev_comp:
                # Set the previous attribute as logical value any
                v = CPEComponent2_3_URI.VALUE_ANY
                pos_ini = max(len(uri) - len(prev_comp_list) - 1, 1)
                increment = 2  # Count of inserted values

                for p, val in enumerate(prev_comp_list):
                    pos = pos_ini + (p * increment)
                    uri.insert(pos, v)
                    uri.insert(pos + 1, CPEComponent2_3_URI.SEPARATOR_COMP)

                set_prev_comp = False
                prev_comp_list = []

        # Return the URI string, with trailing separator trimmed
        return CPE._trim("".join(uri[:-1]))

    def as_wfn(self):
        """
        Returns the CPE Name as Well-Formed Name string of version 2.3.

        :return: CPE Name as WFN string
        :rtype: string
        :exception: TypeError - incompatible version
        """

        from .cpe2_3_wfn import CPE2_3_WFN

        wfn = []
        wfn.append(CPE2_3_WFN.CPE_PREFIX)

        for i in range(0, len(CPEComponent.ordered_comp_parts)):
            ck = CPEComponent.ordered_comp_parts[i]
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

                if isinstance(comp, CPEComponentAnyValue):

                    # Logical value any
                    v.append(CPEComponent2_3_WFN.VALUE_ANY)

                elif isinstance(comp, CPEComponentNotApplicable):

                    # Logical value not applicable
                    v.append(CPEComponent2_3_WFN.VALUE_NA)

                elif (isinstance(comp, CPEComponentUndefined) or
                      isinstance(comp, CPEComponentEmpty)):
                    # Do not set the attribute
                    continue
                else:
                    # Get the simple value of WFN of component
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

    def as_fs(self):
        """
        Returns the CPE Name as formatted string of version 2.3.

        :returns: CPE Name as formatted string
        :rtype: string
        :exception: TypeError - incompatible version
        """

        fs = []
        fs.append("cpe:2.3:")

        for i in range(0, len(CPEComponent.ordered_comp_parts)):
            ck = CPEComponent.ordered_comp_parts[i]
            lc = self._get_attribute_components(ck)

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE Name
                errmsg = "Incompatible version {0} with formatted string".format(
                    self.VERSION)
                raise TypeError(errmsg)

            else:
                comp = lc[0]

                if (isinstance(comp, CPEComponentUndefined) or
                   isinstance(comp, CPEComponentEmpty) or
                   isinstance(comp, CPEComponentAnyValue)):

                    # Logical value any
                    v = CPEComponent2_3_FS.VALUE_ANY

                elif isinstance(comp, CPEComponentNotApplicable):

                    # Logical value not applicable
                    v = CPEComponent2_3_FS.VALUE_NA
                else:
                    # Get the value of component encoded in formatted string
                    v = comp.as_fs()

            # Append v to the formatted string then add a separator.
            fs.append(v)
            fs.append(CPEComponent2_3_FS.SEPARATOR_COMP)

        # Return the formatted string
        return CPE._trim("".join(fs[:-1]))

    def get_edition(self):
        """
        Returns the edition of product of CPE Name as a list.
        According to the CPE version,
        this list can contains one or more items.

        :returns: Value of edition attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_EDITION)

    def get_language(self):
        """
        Returns the internationalization information of CPE Name as a list.
        According to the CPE version, this list can contains one or more items.

        :returns: Value of language attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_LANGUAGE)

    def get_other(self):
        """
        Returns the other information part of CPE Name.

        :returns: Value of other attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_OTHER)

    def get_part(self):
        """
        Returns the part component of CPE Name as a list.
        According to the CPE version,
        this list can contains one or more items.

        :returns: Value of part attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_PART)

    def get_product(self):
        """
        Returns the product name of CPE Name as a list.
        According to the CPE version,
        this list can contains one or more items.

        :returns: Value of product attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_PRODUCT)

    def get_software_edition(self):
        """
        Returns the software edition of CPE Name.

        :returns: Value of sw_edition attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_SW_EDITION)

    def get_target_hardware(self):
        """
        Returns the arquitecture of CPE Name.

        :returns: Value of target_hw attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_TARGET_HW)

    def get_target_software(self):
        """
        Returns the software computing environment of CPE Name
        within which the product operates.

        :returns: Value of target_sw attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_TARGET_SW)

    def get_update(self):
        """
        Returns the update or service pack information of CPE Name as a list.
        According to the CPE version, this list can contains one or more items.

        :returns: Value of update attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_UPDATE)

    def get_vendor(self):
        """
        Returns the vendor name of CPE Name as a list.
        According to the CPE version,
        this list can contains one or more items.

        :returns: Value of vendor attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_VENDOR)

    def get_version(self):
        """
        Returns the version of product of CPE Name as a list.
        According to the CPE version,
        this list can contains one or more items.

        :returns: Value of version attribute as string list.
        :rtype: list
        """

        return self.get_attribute_values(CPEComponent.ATT_VERSION)

    def is_application(self):
        """
        Returns True if CPE Name corresponds to application elem.

        :returns: True if CPE Name corresponds to application elem, False
            otherwise.
        :rtype: boolean
        """

        elements = self.get(CPE.KEY_APP)
        return len(elements) > 0

    def is_hardware(self):
        """
        Returns True if CPE Name corresponds to hardware elem.

        :returns: True if CPE Name corresponds to hardware elem, False
            otherwise.
        :rtype: boolean
        """

        elements = self.get(CPE.KEY_HW)
        return len(elements) > 0

    def is_operating_system(self):
        """
        Returns True if CPE Name corresponds to operating system elem.

        :returns: True if CPE Name corresponds to operating system elem, False
            otherwise.
        :rtype: boolean
        """

        elements = self.get(CPE.KEY_OS)
        return len(elements) > 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('tests/testfile_cpe.txt')
