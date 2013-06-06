#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module is an implementation of name matching
algorithm in accordance with version 1.1 of CPE (Common Platform
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


class CPESet1_1(CPESet):
    """
    Represents a set of CPE names.

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
        >>> from cpe2_2 import CPE2_2
        >>> uri = 'cpe:/o:sun:solaris:5.8'
        >>> c = CPE2_2(uri)
        >>> s = CPESet1_1()
        >>> s.append(c)  #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: CPE name version 2.2 not valid, version 1.1 expected
        """

        if cpe.VERSION != CPE.VERSION_1_1:
            msg = "CPE name version %s not valid, " % cpe.VERSION
            msg += "version 1.1 expected"
            raise ValueError(msg)

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

        Inputs:
            - self: A set of m known CPE names K = {K1, K2, …, Km}.
            - cpe: A candidate CPE name X.
        Output:
            - True if X matches K, otherwise False.

        - TEST: matching with identical CPE in set
        >>> from cpe1_1 import CPE1_1
        >>> from cpeset1_1 import CPESet1_1
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.name_match(c2)
        True

        - TEST: matching with ANY values implicit
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe:/cisco'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_match(c3)
        True

        - TEST: matching with empty CPE name
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe:/'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_match(c3)
        True

        - TEST: not matching with CPE name
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe://noexists'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_match(c3)
        False

        - TEST: matching with ANY values explicit
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe://microsoft:::'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_match(c3)
        True

        - TEST: matching with NOT
        >>> uri1 = 'cpe://microsoft:windows:~xp'
        >>> c1 = CPE1_1(uri1)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> uri2 = 'cpe://microsoft:windows:vista'
        >>> c2 = CPE1_1(uri2)
        >>> s.name_match(c2)
        False

        - TEST: matching with NOT
        >>> uri1 = 'cpe://microsoft:windows:xp'
        >>> c1 = CPE1_1(uri1)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> uri2 = 'cpe://microsoft:windows:~vista'
        >>> c2 = CPE1_1(uri2)
        >>> s.name_match(c2)
        True

        - TEST: matching with OR
        >>> uri1 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> uri2 = 'cpe://microsoft:windows:xp!vista'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe://microsoft:windows:vista'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_match(c3)
        False

        - TEST: matching with OR
        >>> uri1 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> uri2 = 'cpe://microsoft:windows:vista'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe://microsoft:windows:xp!vista'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_match(c3)
        True
        """

        # An empty set not matching with any CPE
        if len(self) == 0:
            return False

        # If input CPE name string is in set of CPE name strings
        # not do searching more because there is a matching
        for k in self.K:
            if (k.cpe_str == cpe.cpe_str):
                return True

        # There are not a CPE name string in set equal to
        # input CPE name string
        match = False

        for p in CPE.CPE_PART_KEYS:
            elems_cpe = cpe.get(p)
            for ec in elems_cpe:
                # Search of element of part of input CPE

                # Each element ec of input cpe[p] is compared with
                # each element ek of k[p] in set K

                for k in self.K:
                    elems_k = k.get(p)

                    for ek in elems_k:
                        # Matching

                        # Each component in element ec is compared with
                        # each component in element ek
                        for ck in CPE.CPE_COMP_KEYS:
                            comp_cpe = ec.get(ck)
                            comp_k = ek.get(ck)

                            match = comp_k in comp_cpe

                            if not match:
                                # Search compoment in another element ek[p]
                                break

                            # Component analyzed

                        if match:
                            # Element matched
                            break
                    if match:
                        break
                # Next element in part in "cpe"

                if not match:
                    # cpe part not match with parts in set
                    return False

            # Next part in input CPE name

        # All parts in input CPE name matched
        return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
