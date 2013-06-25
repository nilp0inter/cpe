#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file is part of cpe package.

This module contains the common characteristics of
any name matching algorithm, associated with a version of Common Platform
Enumeration (CPE) specification.

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
from comp.cpecomp import CPEComponent


class CPESet(object):
    """
    Represents a set of CPE names.

    This class allows:
        - create a set of CPE names.
        - match a CPE name against a set of CPE names.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __getitem__(self, i):
        """
        Returns the i'th CPE name of set.

        INPUT:
            - i: index of CPE name of set to return
        OUTPUT:
            - CPE name found
        EXCEPTION:
            - IndexError: list index out of range
        """

        return self.K[i]

    def __init__(self):
        """
        Creates an empty set of CPE names.
        """
        self.K = []

    def __len__(self):
        """
        Returns the count of CPE names of set.

        - TEST: empty set
        >>> from cpeset1_1 import CPESet1_1
        >>> s = CPESet1_1()
        >>> len(s)
        0
        """

        return len(self.K)

    def __str__(self):
        """
        Returns a human-readable representation of CPE set.

        INPUT:
            - None
        OUTPUT:
            - Representation of CPE component as string
        """

        setlen = self.__len__()

        str = []
        str.append("CPE Set version {0} contains {1} elements".format(
            self.VERSION, setlen))
        if setlen > 0:
            str.append(":")

            for i in range(0, setlen):
                str.append("    {0}".format(self.K[i].__str__()))

        return "\n".join(str)

    def append(self, cpe):
        """
        Adds a CPE name to the set if not already.

        INPUT:
            - cpe: CPE name to store in set
        OUTPUT:
            - None
        """

        errmsg = "Class method not implemented. Use the method of some child class"
        raise NotImplementedError(errmsg)

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
        """

        # An empty set not matching with any CPE
        if len(self) == 0:
            return False

        # If input CPE name string is in set of CPE name strings
        # not do searching more because there is a matching
        for k in self.K:
            if (k.cpe_str == cpe.cpe_str):
                return True

        # If "cpe" is an empty CPE name any system matches
        if len(cpe) == 0:
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
                                key = CPEComponent.ordered_comp_parts[c]
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
