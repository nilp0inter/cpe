#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module of is an implementation of name matching
algorithm in accordance with version 2.2 of CPE (Common Platform
Enumeration) specification.

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

from cpe import CPE
from cpeset import CPESet


class CPESet2_2(CPESet):
    """
    Represents a set of CPE names.

    This class allows:
        - create set of CPE names.
        - match a CPE element against a set of CPE names.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Version of CPE set
    VERSION = "2.2"

    ####################
    #  OBJECT METHODS  #
    ####################

    def append(self, cpe):
        """
        Adds a CPE name to the set if not already.

        INPUT:
            - cpe: CPE name to store in set
        OUTPUT:
            - None
        EXCEPTIONS:
            - ValueError: Invalid version of CPE name

        - TEST:
        >>> from cpeset2_2 import CPESet2_2
        >>> from cpe2_2 import CPE2_2
        >>> uri1 = 'cpe:/h:hp'
        >>> c1 = CPE2_2(uri1)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        """

        if cpe.VERSION != CPE.VERSION_2_2:
            errmsg = "CPE name version {0} not valid, version 2.2 expected".format(
                cpe.VERSION)
            raise ValueError(errmsg)

        for k in self.K:
            if cpe.cpe_str == k.cpe_str:
                return None

        self.K.append(cpe)

    def name_match(self, cpe):
        """
        Accepts a set of known instances of CPE names and a candidate CPE name,
        and returns 'True' if the candidate can be shown to be
        an instance based on the content of the known instances.
        Otherwise, it returns 'False'.

        INPUT:
            - self: A set of m known CPE names K = {K1, K2, …, Km}.
            - cpe: A candidate CPE name X.
        OUTPUT:
            - True if X matches K, otherwise False.

        - TEST: matching with ANY values explicit
        >>> from cpe2_2 import CPE2_2
        >>> uri1 = 'cpe:/o:microsoft:windows:vista'
        >>> uri2 = 'cpe:/o:cisco:ios:12.3:enterprise'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe:/o:microsoft::vista'
        >>> c3 = CPE2_2(uri3)
        >>> s.name_match(c3)
        True
        """

        return super(CPESet2_2, self).name_match(cpe)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpeset2_2.txt")
