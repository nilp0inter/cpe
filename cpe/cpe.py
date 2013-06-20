#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module contains the common characteristics of
any type of CPE name, associated with a version of Common Platform
Enumeration (CPE) specification.

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

from cpecomp import CPEComponent
from cpecomp2_3_uri import CPEComponent2_3_URI
from cpecomp2_3_wfn import CPEComponent2_3_WFN
from cpecomp2_3_fs import CPEComponent2_3_FS
from cpecomp2_3_uri_edpacked import CPEComponent2_3_URI_edpacked
from cpecomp_logical import CPEComponentLogical
from cpecomp_empty import CPEComponentEmpty
from cpecomp_anyvalue import CPEComponentAnyValue
from cpecomp_undefined import CPEComponentUndefined
from cpecomp_notapplicable import CPEComponentNotApplicable


class CPE(dict):
    """
    Represents a generic CPE name compatible with
    all versions of CPE specification.

    Parts of CPE are stored in a dictionary.

    CPE structure (dictionary):
        |- part {hw, os, sw, undefined}
            |- element list (list)
                |- component list (dictionary)
    """

    ###############
    #  CONSTANTS  #
    ###############

    # included in CPE specification
    KEY_APP = "app"
    KEY_HW = "hw"
    KEY_OS = "os"
    KEY_UNDEFINED = "undef"

    # List of keys associated with the three types of system
    # included in CPE specification
    CPE_PART_KEYS = (KEY_HW, KEY_OS, KEY_APP, KEY_UNDEFINED)

    # Constants used to paint the representation of CPE name
    PREFIX_ELEM = "   ["
    PREFIX_ELEMENTS = " ["
    SUFFIX_ELEM = "   ]"
    SUFFIX_ELEMENTS = " ]"

    # Constants of possible versions of CPE specification
    VERSION_1_1 = "1.1"
    VERSION_2_2 = "2.2"
    VERSION_2_3 = "2.3"
    VERSION_UNDEFINED = "undefined"

    # Version of CPE name
    VERSION = VERSION_UNDEFINED

    ###############
    #  VARIABLES  #
    ###############

    # Dictionary keys associated with the three types of system
    # Relation between the values of "part" component and the part name in
    # internal structure of CPE name
    system_and_parts = {
        CPEComponent.VALUE_PART_HW: KEY_HW,
        CPEComponent.VALUE_PART_OS: KEY_OS,
        CPEComponent.VALUE_PART_APP: KEY_APP,
        CPEComponent.VALUE_PART_UNDEFINED: KEY_UNDEFINED}

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _trim(cls, s):
        """
        Remove trailing colons from the URI back to the first non-colon.

        - TEST: trailing colons necessary
        >>> s = '1:2::::'
        >>> CPE._trim(s)
        '1:2'

        - TEST: trailing colons not necessary
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
        self (second element of operation) are equal CPE names,
        false otherwise.

        INPUT:
            - other: CPE name to compare
        OUTPUT:
            True if other == self, False otherwise
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
        Store the CPE name.

        INPUT:
            - cpe_str: CPE name as string
        OUPUT:
            - None
        """

        # The original CPE name as string
        self.cpe_str = cpe_str

        # Store CPE name in lower-case letters:
        # CPE names are case-insensitive.
        # To reduce potential for confusion,
        # all CPE Names should be written in lowercase.
        self._str = cpe_str.lower()

        # Check if CPE name is correct
        self._parse()

    def __len__(self):
        """
        Returns the number of components of CPE name.
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
        Generator of CPE names.

        INPUT:
            - cpe_str: CPE name string
            - version: version of CPE specification of CPE name
        OUTPUT:
            - CPE object with version of CPE detected correctly.
        EXCEPTIONS:
            - NotImplementedError: Incorrect CPE name or
                version of CPE not implemented

        This class implements the factory pattern, that is,
        this class centralizes the creation of objects of a particular
        CPE version, hiding the user the requested object instance.
        """

        from cpe1_1 import CPE1_1
        from cpe2_2 import CPE2_2
        from cpe2_3 import CPE2_3

        # List of implemented versions of CPE names
        _CPE_VERSIONS = {
            CPE.VERSION_1_1: CPE1_1,
            CPE.VERSION_2_2: CPE2_2,
            CPE.VERSION_2_3: CPE2_3}

        errmsg = 'Version of CPE not implemented'

        if version is None:
            # Detect CPE version of input CPE name
            for v in _CPE_VERSIONS:
                try:
                    # Validate CPE name
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
            # Correct input version, validate CPE name
            return _CPE_VERSIONS[version](cpe_str)
        else:
            # Invalid CPE version
            raise NotImplementedError(errmsg)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        txtParts = []

        for pk in CPE.CPE_PART_KEYS:
            txtParts.append(pk)

            txtElements = []
            txtElements.append(CPE.PREFIX_ELEMENTS)

            elements = self.get(pk)

            for elem in elements:
                txtComp = []
                txtComp.append(CPE.PREFIX_ELEM)

                for i in range(0, len(CPEComponent.CPE_COMP_KEYS_EXTENDED)):
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

                if len(txtComp) == 1:
                    # There are no components
                    txtElements = []
                    txtElements.append(" []")
                else:
                    txtElements.append(CPE.SUFFIX_ELEM)
                txtElements = "\n".join(txtComp)

            if len(txtElements) == 1:
                    # There are no elements
                    txtParts = []
                    txtParts.append(" []")
            else:
                txtParts = "\n".join(txtElements)

        return "".join(txtParts)

    def __str__(self):
        """
        Returns a human-readable representation of CPE name.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "CPE v{0}: {1}".format(self.VERSION, self.cpe_str)

    def _createCPEParts(self, system, components):
        """
        Create the structure to store the input type of system associated
        with components of CPE name (hardware, operating system and software).

        INPUT:
            - system: type of system associated with CPE name
            - components: CPE name components to store
        OUTPUT:
            - None
        EXCEPTIONS:
            - KeyError: incorrect system
        """

        if system not in CPEComponent.SYSTEM_VALUES:
            errmsg = "Key '{0}' is not exist".format(system)
            raise ValueError(errmsg)

        elements = []
        elements.append(components)

        pk = CPE.system_and_parts[system]
        self[pk] = elements

    def _getAttributeComponents(self, att):
        """
        Returns the component list of attribute "att".

        INPUT:
            - att: Attribute name to get
        OUTPUT:
            - The component list of the attribute in CPE name
        EXCEPTIONS:
            - ValueError: invalid attribute name
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

    def _hasOneElement(self):
        """
        Returns True if CPE name has a only element with components.
        """

        return (self._numElements() == 1)

    def _hasNoElement(self):
        """
        Returns True if CPE name has a only element with components.
        """

        return (self._numElements() == 0)

    def _numElements(self):
        """
        Returns the count of elements of CPE name.
        """

        count = 0
        for pk in CPE.CPE_PART_KEYS:
            elements = self.get(pk)
            count += len(elements)

        return count

    def _pack_edition(self):
        """
        Pack the values of the five arguments into the single edition
        component. If all the values are blank, just return a blank.

        INPUT:
            - None
        OUTPUT:
            - "edition", "sw_edition", "target_sw", "target_hw" and "other"
            attributes packed in a only value
        EXCEPTIONS:
            TypeError: incompatible version with pack operation
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
            lc = self._getAttributeComponents(ck)
            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE name
                errmsg = "Incompatible version {0} with URI".format(
                    self.VERSION)
                raise TypeError(errmsg)

            comp = lc[0]
            if (isinstance(comp, CPEComponentUndefined) or
               isinstance(comp, CPEComponentEmpty) or
               isinstance(comp, CPEComponentAnyValue)):

                value = ""

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
            # Otherwise, pack the five values into a single string
            # prefixed and internally delimited with the tilde
            return packed_ed_str

    def as_dict(self):
        """
        Returns the CPE name dict as string.
        """

        return self.__str__()

    def as_uri_2_3(self):
        """
        Returns the CPE name as URI string of version 2.3.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - TypeError: incompatible version
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
            lc = self._getAttributeComponents(ck)

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE name
                errmsg = "Incompatible version {0} with URI".format(
                    self.VERSION)
                raise TypeError(errmsg)

            if ck == CPEComponent.ATT_EDITION:
                # Call the pack() helper function to compute the proper
                # binding for the edition element
                v = self._pack_edition()

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
                pos_ini = len(uri) - len(prev_comp_list) - 1
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
        Returns the CPE name as WFN string of version 2.3.

        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - TypeError: incompatible version
        """

        from cpe2_3_wfn import CPE2_3_WFN

        wfn = []
        wfn.append(CPE2_3_WFN.CPE_PREFIX)

        for i in range(0, len(CPEComponent.ordered_comp_parts)):
            ck = CPEComponent.ordered_comp_parts[i]
            lc = self._getAttributeComponents(ck)

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE name
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
                    # Get the single value of WFN of component
                    v.append('"')
                    v.append(comp.as_wfn())
                    v.append('"')

                # Append v to the WFN and add a separator
                wfn.append("".join(v))
                wfn.append(CPEComponent2_3_WFN.SEPARATOR_COMP)

        # Del the last separator
        wfn = wfn[:-1]

        # Return the WFN string
        wfn.append("]")

        return "".join(wfn)

    def as_fs(self):
        """
        Returns the CPE name as formatted string of version 2.3.
        INPUT:
            - None
        OUTPUT:
            - None
        EXCEPTIONS:
            - TypeError: incompatible version
        """

        fs = []
        fs.append("cpe:2.3:")

        for i in range(0, len(CPEComponent.ordered_comp_parts)):
            ck = CPEComponent.ordered_comp_parts[i]
            lc = self._getAttributeComponents(ck)

            if len(lc) > 1:
                # Incompatible version 1.1, there are two or more elements
                # in CPE name
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

    def getEdition(self):
        """
        Returns the edition of product of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_EDITION)

    def getLanguage(self):
        """
        Returns the internationalization information of CPE name as a list.
        According to the CPE version, this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_LANGUAGE)

    def getOther(self):
        """
        Returns the other information part of CPE name.
        """

        return self.getAttributeValues(CPEComponent.ATT_OTHER)

    def getPart(self):
        """
        Returns the part component of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_PART)

    def getProduct(self):
        """
        Returns the product name of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_PRODUCT)

    def getSoftwareEdition(self):
        """
        Returns the software edition of CPE name.
        """

        return self.getAttributeValues(CPEComponent.ATT_SW_EDITION)

    def getTargetHardware(self):
        """
        Returns the arquitecture of CPE name.
        """

        return self.getAttributeValues(CPEComponent.ATT_TARGET_HW)

    def getTargetSoftware(self):
        """
        Returns the software computing environment of CPE name
        within which the product operates.
        """

        return self.getAttributeValues(CPEComponent.ATT_TARGET_SW)

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE name as a list.
        According to the CPE version, this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_UPDATE)

    def getVendor(self):
        """
        Returns the vendor name of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_VENDOR)

    def getVersion(self):
        """
        Returns the version of product of CPE name as a list.
        According to the CPE version,
        this list can contains one or more items.
        """

        return self.getAttributeValues(CPEComponent.ATT_VERSION)

    def isApplication(self):
        """
        Returns True if CPE name corresponds to application elem.
        """

        elements = self.get(CPE.KEY_APP)
        return len(elements) > 0

    def isHardware(self):
        """
        Returns True if CPE name corresponds to hardware elem.
        """

        elements = self.get(CPE.KEY_HW)
        return len(elements) > 0

    def isOperatingSystem(self):
        """
        Returns True if CPE name corresponds to operating system elem.
        """

        elements = self.get(CPE.KEY_OS)
        return len(elements) > 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('tests/testfile_cpe.txt')
