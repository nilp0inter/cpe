#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module allows to create an undefined component of CPE name.

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


class UndefinedCPEComponent(CPEComponent):
    """
    Represents an undefined component of CPE name compatible with
    the components of all versions of CPE specification.

    For example, in version 1.1 of CPE specification, an undefined component
    is edition in CPE name cpe:/microsft:windows:xp.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str=CPEComponent.UNDEFINED_VALUE):
        """
        Store the empty value of component.

        INPUT:
            - comp_str: empty value of component
        OUPUT:
            - None
        """

        super(UndefinedCPEComponent, self).__init__(comp_str)
