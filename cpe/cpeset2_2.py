#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module of is an implementation of name matching
algorithm in accordance with version 2.2 of CPE (Common Platform
Enumeration) specification.

Copyright (C) 2013  Roberto A. Martínez, Alejandro Galindo

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

from cpe import CPE
from cpeset import CPESet


class CPESet2_2(CPESet):
    """
    Represents a set of CPEs.

    This class allows:
        - create set of CPE elements.
        - match a CPE element against a set of CPE elements.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def append(self, cpe):
        """
        Adds a CPE element to the set if not already.

        INPUT:
            - cpe: CPE name to store in set
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: Invalid version of CPE name

        - TEST: set with invalid CPE name
        >>> from cpe1_1 import CPE1_1
        >>> uri = 'cpe:///'
        >>> c = CPE1_1(uri)
        >>> s = CPESet2_2()
        >>> s.append(c)  #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: CPE name version 1.1 not valid, version 2.2 expected
        """

        if cpe.VERSION != CPE.VERSION_2_2:
            msg = "CPE name version %s not valid, " % cpe.VERSION
            msg += "version 2.2 expected"
            raise ValueError(msg)

        for k in self.K:
            if cpe.cpe_str == k.cpe_str:
                return None

        self.K.append(cpe)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
