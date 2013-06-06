#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to store the value of the components of a CPE name and
compare two components to know if they are equal.

Copyright (C) 2013  Alejandro Galindo, Roberto A. Martínez

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


class CPEComponent(object):
    """
    Represents a generic component of CPE name compatible with
    the components of all versions of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Value that represents the logical value ANY in CPE specification.
    ANY_VALUE = None

    # Value of a empty component
    EMPTY_COMP_VALUE = ""

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str):
        """
        Store the value of component.

        INPUT:
            - comp_str: value of component
        OUPUT:
            - None
        """

        self._data = comp_str
        self._is_negated = False

    def __eq__(self, other):
        """
        Returns True if self and other are equal components.
        """

        if (self._data is CPEComponent.ANY_VALUE or
           other._data is CPEComponent.ANY_VALUE):

            return True

        return ((self._data == other._data) and
                (self._is_negated == other._is_negated))

    def __str__(self):
        """
        Returns a readable representation of CPE component.
        """

        txt = "Negated: %s    " % self._is_negated
        txt += "Data: %s" % self._data

        return txt
