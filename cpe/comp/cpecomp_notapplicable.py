#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module allows to create a component of CPE name with a
not applicable value.

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

from .cpecomp_logical import CPEComponentLogical


class CPEComponentNotApplicable(CPEComponentLogical):
    """
    Represents a component of CPE name with a not applicable value,
    compatible with the components of all versions of CPE specification.

    For example, in version 2.3 of CPE specification, an component "not
    applicable" is update attribute in CPE name cpe:/a:microsft:windows:me:-.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __contains__(self, item):
        """
        Returns True if item is included in set of values of self.

        :param CPEComponent item: component to find in self
        :returns: True if item is included in set of self
        :rtype: boolean
        """

        return (self == item)

    def __eq__(self, other):
        """
        Returns True if other (first element of operation) and
        self (second element of operation) are equal components,
        false otherwise.

        :param CPEComponent other: component to compare
        :returns: True if other == self, False otherwise
        :rtype: boolean
        """

        return isinstance(other, CPEComponentNotApplicable)

    def __init__(self):
        """
        Initializes the component.
        """

        super(CPEComponentNotApplicable, self).__init__(
            CPEComponentLogical._VALUE_INT_NA)

    def __str__(self):
        """
        Returns a human-readable representation of CPE component.

        :returns: Representation of CPE component as string
        :rtype: string
        """

        return "<NA>"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('../tests/testfile_cpecomp_notapplicable.txt')
