#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the logical components
of a CPE name and compare it with others.

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

from cpecomp import CPEComponent
from abc import ABCMeta
from abc import abstractmethod


class CPEComponentLogical(CPEComponent):
    """
    Represents a generic logical component of CPE name,
    compatible with the components of all versions of CPE specification.
    """

    __metaclass__ = ABCMeta

    ###############
    #  CONSTANTS  #
    ###############

    # Logical values in integer format

    # Value of an undefined component. For example, edition attribute in the
    # CPE name cpe:/cisco::2345 of version 1.1 of CPE specification
    _VALUE_INT_UNDEFINED = -1

    # Value of an empty component. For example, product attribute in the
    # CPE name cpe:/cisco::2345 of version 1.1 of CPE specification
    _VALUE_INT_EMPTY = 0

    # Value of a component "any value". For example, product attribute in the
    # CPE name cpe:/h:cisco:*:2345 of version 2.3 of CPE specification
    _VALUE_INT_ANY = 1

    # Value of a not applicable component. For example, product attribute in
    # the CPE name cpe:/h:cisco:-:2345 of version 2.3 of CPE specification
    _VALUE_INT_NA = 2

    ####################
    #  OBJECT METHODS  #
    ####################

    @abstractmethod
    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        INPUT:
            - item: component to find in self
        OUTPUT:
            - True if item is included in set of self
        """

        return True

    @abstractmethod
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

        pass

    @abstractmethod
    def __init__(self, comp_str):
        """
        Store the value of component.

        INPUT:
            - comp_str: value of component value
        OUPUT:
            - None
        EXCEPTIONS:
            - ValueError: incorrect value of component
        """

        return super(CPEComponentLogical, self).__init__(comp_str)

    @abstractmethod
    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        pass

    @abstractmethod
    def __str__(self):
        """
        Returns a human-readable representation of CPE component.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        pass
