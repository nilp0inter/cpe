#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE Name and
compare it with others.

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

import types


class CPEComponent(object):
    """
    Represents a generic component of CPE Name,
    compatible with the components of all versions of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants of possible versions of CPE components

    #: Version 1.1 of CPE component
    COMP_1_1 = "1.1"

    #: Version 2.2 of CPE component
    COMP_2_2 = "2.2"

    #: Version 2.3 with WFN style of CPE component
    COMP_2_3_WFN = "2.3_wfn"

    #: Version 2.3 with URI style of CPE component
    COMP_2_3_URI = "2.3_uri"

    #: Version 2.3 with formatted string style of CPE component
    COMP_2_3_FS = "2.3_fs"

    # Attributes associated with components of all versions of CPE

    #: Part attribute of CPE Name that indicates the type of system
    #: associated with the product
    ATT_PART = "part"

    #: Vendor attribute of CPE Name that describes or identify the person or
    #: organization that manufactured or created the product
    ATT_VENDOR = "vendor"

    #: Product attribute of CPE Name that describes or identify the most common
    #: and recognizable title or name of the product
    ATT_PRODUCT = "product"

    #: Version attribute of CPE Name that indicates vendor-specific
    #: alphanumeric strings characterizing the particular release version
    #: of the product
    ATT_VERSION = "version"

    #: Version attribute of CPE Name that indicates vendor-specific
    #: alphanumeric strings characterizing the particular update,
    #: service pack, or point release of the product
    ATT_UPDATE = "update"

    #: Edition attribute of CPE Name that captures the edition-related terms
    #: applied by the vendor to the product
    ATT_EDITION = "edition"

    #: Language attribute of CPE Name that defines the language supported
    #: in the user interface of the product being described
    ATT_LANGUAGE = "language"

    # Attributes associated with components of version 2.3 of CPE

    #: SW_edition attribute of version 2.3 of CPE Name that characterizes
    #: how the product is tailored to a particular market or class of
    #: end users
    ATT_SW_EDITION = "sw_edition"

    #: Target_SW attribute of version 2.3 of CPE Name that characterizes the
    #: software computing environment within which the product operates
    ATT_TARGET_SW = "target_sw"

    #: Target_HW attribute of version 2.3 of CPE Name that characterizes the
    #: instruction set architecture (e.g., x86) on which the product being
    #: described or identified by the WFN operates
    ATT_TARGET_HW = "target_hw"

    #: Other attribute of version 2.3 of CPE Name that capture any other
    #: general descriptive or identifying information which is vendor-
    #: or product-specific and which does not logically fit in any other
    #: attribute value
    ATT_OTHER = "other"

    #: List of attribute names associated with CPE Name components
    #: (versions 1.1 and 2.2 of CPE specification)
    CPE_COMP_KEYS = (ATT_PART,
                     ATT_VENDOR,
                     ATT_PRODUCT,
                     ATT_VERSION,
                     ATT_UPDATE,
                     ATT_EDITION,
                     ATT_LANGUAGE)

    #: List of attribute names associated with CPE Name components
    #: of version 2.3
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

    #: Value of part attribute associated with a hardware system
    VALUE_PART_HW = "h"

    #: Value of part attribute associated with an operating system
    VALUE_PART_OS = "o"

    #: Value of part attribute associated with an application
    VALUE_PART_APP = "a"

    #: Value of part attribute that indicates a CPE Name with
    #: undefined type of system
    VALUE_PART_UNDEFINED = "u"

    #: Possible values of a type of system in CPE specification:
    #: hardware, operating system, software and undefined
    SYSTEM_VALUES = (VALUE_PART_HW,
                     VALUE_PART_OS,
                     VALUE_PART_APP,
                     VALUE_PART_UNDEFINED)

    ###############
    #  VARIABLES  #
    ###############

    #: Order of attributes of CPE Name components
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

        :param string att_name: attribute name to check
        :returns: True is attribute name is valid, otherwise False
        :rtype: boolean

        TEST: a wrong attribute

        >>> from .cpecomp import CPEComponent
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

        :param CPEComponent item: component to find in self
        :returns: True if item is included in set of self, otherwise False
        :rtype: boolean
        """

        from .cpecomp_undefined import CPEComponentUndefined
        from .cpecomp_empty import CPEComponentEmpty
        from .cpecomp_anyvalue import CPEComponentAnyValue

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

        :param CPEComponent other: component to compare
        :returns: True if other == self, False otherwise
        :rtype: boolean
        """

        len_self = len(self._standard_value)
        len_other = len(other._standard_value)

        if isinstance(self._standard_value, list):
            # Self is version 1.1 of CPE Name
            if isinstance(other._standard_value, list):
                # Other is version 1.1 of CPE Name
                value_self = self._standard_value
                value_other = other._standard_value

            # Other is higher version than to 1.1 of CPE Name
            elif len_self == 1:
                value_self = self._standard_value[0]
                value_other = other._standard_value

            else:
                # The comparation between components is impossible
                return False
        else:
            # Self is higher version than 1.1 of CPE Name
            if isinstance(other._standard_value, list):
                # Other is version 1.1 of CPE Name
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

        :param string comp_str: value of component value
        :returns: None
        """

        self._is_negated = False
        self._encoded_value = comp_str
        self._standard_value = [comp_str]

    def __ne__(self, other):
        """
        Returns True if other (first element of operation) and
        self (second element of operation) are not equal components,
        false otherwise.

        :param CPEComponent other: component to compare
        :returns: True if other != self, False otherwise
        :rtype: boolean
        """

        return not (self == other)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        :returns: Representation of CPE component as string
        :rtype: string
        """

        return "{0}()".format(self.__class__.__name__)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('../tests/testfile_cpecomp.txt')
