#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to create a empty component of CPE name, that is,
a component without value.

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


class EmptyCPEComponent(CPEComponent):
    """
    Represents a empty component of CPE name compatible with
    the components of all versions of CPE specification.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str=CPEComponent.EMPTY_COMP_VALUE):
        """
        Store the empty value of component.

        INPUT:
            - comp_str: empty value of component
        OUPUT:
            - None
        """

        super(EmptyCPEComponent, self).__init__(comp_str)
