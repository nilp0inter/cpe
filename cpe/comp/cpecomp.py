#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name and
compare it with others.

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

import types


class CPEComponent(object):
    """
    Represents a generic component of CPE name,
    compatible with the components of all versions of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants of possible versions of CPE components
    COMP_1_1 = "1.1"
    COMP_2_2 = "2.2"
    COMP_2_3_WFN = "2.3_wfn"
    COMP_2_3_URI = "2.3_uri"
    COMP_2_3_FS = "2.3_fs"

    # Attributes associated with components of all versions of CPE
    ATT_PART = "part"
    ATT_VENDOR = "vendor"
    ATT_PRODUCT = "product"
    ATT_VERSION = "version"
    ATT_UPDATE = "update"
    ATT_EDITION = "edition"
    ATT_LANGUAGE = "language"

    # Attributes associated with components of version 2.3 of CPE
    ATT_SW_EDITION = "sw_edition"
    ATT_TARGET_SW = "target_sw"
    ATT_TARGET_HW = "target_hw"
    ATT_OTHER = "other"

    # List of attribute names associated with CPE name components
    # Versions 1.1 and 2.2
    CPE_COMP_KEYS = (ATT_PART,
                     ATT_VENDOR,
                     ATT_PRODUCT,
                     ATT_VERSION,
                     ATT_UPDATE,
                     ATT_EDITION,
                     ATT_LANGUAGE)

    # List of attribute names associated with CPE name components
    # Versions 2.3
    CPE_COMP_KEYS_EXTENDED = (ATT_PART,
                              ATT_VENDOR,
                              ATT_PRODUCT,
                              ATT_VERSION,
                              ATT_UPDATE,
                              ATT_EDITION,
                              ATT_LANGUAGE,
                              ATT_SW_EDITION,
                              ATT_TARGET_SW,
                              ATT_TARGET_HW,
                              ATT_OTHER)

    # Possible values of "part" attribute of CPE (type of system)
    VALUE_PART_HW = "h"
    VALUE_PART_OS = "o"
    VALUE_PART_APP = "a"
    VALUE_PART_UNDEFINED = "u"

    # Types of systems in CPE specification:
    # hardware, operating system, software and undefined
    SYSTEM_VALUES = (VALUE_PART_HW,
                     VALUE_PART_OS,
                     VALUE_PART_APP,
                     VALUE_PART_UNDEFINED)

    ###############
    #  VARIABLES  #
    ###############

    # Order of attributes of CPE name components
    ordered_comp_parts = {0: ATT_PART,
                          1: ATT_VENDOR,
                          2: ATT_PRODUCT,
                          3: ATT_VERSION,
                          4: ATT_UPDATE,
                          5: ATT_EDITION,
                          6: ATT_LANGUAGE,
                          7: ATT_SW_EDITION,
                          8: ATT_TARGET_SW,
                          9: ATT_TARGET_HW,
                          10: ATT_OTHER}

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def is_valid_attribute(cls, att_name):
        """
        Check if input attribute name is correct.

        INPUT:
            - att_name: attribute name to check
        OUTPUT:
            - True is attribute name is valid, otherwise False

        TEST: a wrong attribute
        >>> from cpecomp import CPEComponent
        >>> att = CPEComponent.ATT_PRODUCT
        >>> CPEComponent.is_valid_attribute(att)
        True
        """

        return att_name in CPEComponent.CPE_COMP_KEYS_EXTENDED

    ####################
    #  OBJECT METHODS  #
    ####################

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        INPUT:
            - item: component to find in self
        OUTPUT:
            - True if item is included in set of self, otherwise False
        """

        from cpecomp_undefined import CPEComponentUndefined
        from cpecomp_empty import CPEComponentEmpty
        from cpecomp_anyvalue import CPEComponentAnyValue

        if ((self == item) or
           isinstance(self, CPEComponentUndefined) or
           isinstance(self, CPEComponentEmpty) or
           isinstance(self, CPEComponentAnyValue)):

            return True

        return False

    def __eq__(self, other):
        """
        Returns True if other (first element of operation) and
        self (second element of operation) are equal components,
        false otherwise.

        INPUT:
            - other: component to compare
        OUTPUT:
            True if other == self, False otherwise
        """

        len_self = len(self._standard_value)
        len_other = len(other._standard_value)

        if isinstance(self._standard_value, types.ListType):
            # Self is version 1.1 of CPE name
            if isinstance(other._standard_value, types.ListType):
                # Other is version 1.1 of CPE name
                value_self = self._standard_value
                value_other = other._standard_value

            # Other is higher version than to 1.1 of CPE name
            elif len_self == 1:
                value_self = self._standard_value[0]
                value_other = other._standard_value

            else:
                # The comparation between components is impossible
                return False
        else:
            # Self is higher version than 1.1 of CPE name
            if isinstance(other._standard_value, types.ListType):
                # Other is version 1.1 of CPE name
                if len_other == 1:
                    value_self = self._standard_value
                    value_other = other._standard_value[0]

                else:
                    # The comparation between components is impossible
                    return False
            else:
                value_self = self._standard_value
                value_other = other._standard_value

        return ((value_self == value_other) and
               (self._is_negated == other._is_negated))

    def __init__(self, comp_str):
        """
        Store the value of component.

        INPUT:
            - comp_str: value of component value
        OUPUT:
            - None
        """

        self._is_negated = False
        self._encoded_value = comp_str
        self._standard_value = [comp_str]

    def __ne__(self, other):
        """
        Returns True if other (first element of operation) and
        self (second element of operation) are not equal components,
        false otherwise.

        INPUT:
            - other: component to compare
        OUTPUT:
            True if other != self, False otherwise
        """

        return not (self == other)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        return "{0}()".format(self.__class__.__name__)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('../tests/testfile_cpecomp.txt')
