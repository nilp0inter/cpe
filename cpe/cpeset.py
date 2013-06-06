#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module contains the common characteristics of
any name matching algorithm, associated with a version of Common Platform
Enumeration (CPE) specification.

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


class CPESet(object):
    """
    Represents a set of CPE names.

    This class allows:
        - create set of CPE elements.
        - match a CPE element against a set of CPE elements.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self):
        """
        Creates an empty set of CPE names.
        """
        self.K = []

    def __len__(self):
        """
        Returns the count of CPE elements of set.

        - TEST: empty set
        >>> from cpe1_1 import CPE1_1
        >>> from cpeset1_1 import CPESet1_1
        >>> s = CPESet1_1()
        >>> len(s)
        0

        - TEST: set with two CPE elements
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> len(s)
        2

        - TEST: set with three CPE elements and one repeated
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c2)
        >>> len(s)
        2

        - TEST: set with three CPE elements and one repeated
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> c3 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c3)
        >>> len(s)
        2
        """

        return len(self.K)

    def __getitem__(self, i):
        """
        Returns the i'th CPE element of set.

        INPUT:
            - i: index of CPE element of set to return
        OUTPUT:
            - i'th CPE element of set found
        """

        return self.K[i]

    def __str__(self):
        """
        Returns a CPE set as string.
        """

        len = self.__len__()

        str = "Set contains %s elements" % len
        if len > 0:
            str += ":\n"

            for i in range(0, len):
                str += "    %s" % self.K[i].__str__()

                if i+1 < len:
                    str += "\n"

        return str

    def append(self, cpe):
        """
        Adds a CPE element to the set if not already.

        INPUT:
            - cpe: CPE name to store in set
        OUTPUT:
            - None
        """
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

        - TEST: matching (identical cpe in set)
        >>> from cpe2_2 import CPE2_2
        >>> from cpeset2_2 import CPESet2_2
        >>> uri1 = 'cpe:/o:redhat:enterprise_linux:3'
        >>> uri2 = 'cpe:/o:sun:sunos:5.8'
        >>> uri3 = 'cpe:/o:microsoft:windows_2003'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> m = CPE2_2(uri3)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(m)
        >>> s.name_match(m)
        True

        - TEST: matching with any values (cpe in set)
        >>> uri1 = 'cpe:/o:redhat:enterprise_linux:3'
        >>> uri2 = 'cpe:/o:sun:sunos:5.8'
        >>> uri3 = 'cpe:/o:sun'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> m = CPE2_2(uri3)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.name_match(m)
        True

        - TEST: not matching
        >>> uri1 = 'cpe:/o:redhat:enterprise_linux:3'
        >>> uri2 = 'cpe:/o:sun:sunos:5.8'
        >>> uri3 = 'cpe:/a:microsoft:ie:9'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> m = CPE2_2(uri3)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.name_match(m)
        False
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
                    if (len(k) >= len(cpe)):
                        elems_k = k.get(p)

                        for ek in elems_k:
                            # Matching

                            # Each component in element ec is compared with
                            # each component in element ek
                            for c in range(0, len(cpe)):
                                key = CPE.ORDERED_COMP_PARTS[c]
                                comp_cpe = ec.get(key)
                                comp_k = ek.get(key)

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
