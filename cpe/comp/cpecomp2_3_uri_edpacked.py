#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to store the value of the packed edition component
of a CPE name of version 2.3 of CPE (Common Platform Enumeration)
specification with Universal Resource Identifier (URI) style.

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

from .cpecomp2_3_uri import CPEComponent2_3_URI


class CPEComponent2_3_URI_edpacked(CPEComponent2_3_URI):
    """
    Represents a packd edition component of version 2.3 of CPE
    specification with URI style.
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Separator of components of an edition attribute packed
    SEPARATOR_COMP = "~"

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, comp_str):
        """
        Store the value of component.

        :param string comp_str: value of component value
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        self.set_value(comp_str)

    def _decode(self):
        """
        The decoding of the value of this type of component is not necesaary.
        """

        pass

    def _is_valid_edition(self):
        """
        This function is not necesaary in this component.

        :returns: True
        :rtype: boolean
        """

        True

    def _is_valid_value(self):
        """
        This function is not necesaary in this component.

        :returns: True
        :rtype: boolean
        """

        True

    def set_value(self, comp_str):
        """
        Set the value of component.

        :param string comp_str: value of component
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        self._is_negated = False
        self._encoded_value = comp_str
        self._standard_value = super(
            CPEComponent2_3_URI_edpacked, self)._decode()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
