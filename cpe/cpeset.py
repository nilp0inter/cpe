#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module contains the common characteristics of
any name matching algorithm, associated with a version of Common Platform
Enumeration (CPE) specification.

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

from .cpe import CPE
from .comp.cpecomp import CPEComponent


class CPESet(object):
    """
    Represents a set of CPE Names.

    This class allows:

        - create a set of CPE Names.
        - match a CPE Name against a set of CPE Names.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __getitem__(self, i):
        """
        Returns the i'th CPE Name of set.

        :param int i: CPE Name index to find
        :returns: CPE Name found
        :rtype: CPE
        :exception: IndexError - list index out of range
        """

        return self.K[i]

    def __init__(self):
        """
        Creates an empty set of CPE Names.

        :returns: None
        """
        self.K = []

    def __len__(self):
        """
        Returns the count of CPE Names of set.

        :returns: count of components of CPE Name
        :rtype: int

        TEST: empty set

        >>> from .cpeset1_1 import CPESet1_1
        >>> s = CPESet1_1()
        >>> len(s)
        0
        """

        return len(self.K)

    def __str__(self):
        """
        Returns a human-readable representation of CPE set.

        :returns: Representation of CPE set as string
        :rtype: string
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
        Adds a CPE Name to the set if not already.

        :param CPE cpe: CPE Name to store in set
        :returns: None
        :exception: NotImplementedError - Method not implemented
        """

        errmsg = "Method not implemented. Use the method of some child class"
        raise NotImplementedError(errmsg)

    def name_match(self, cpe):
        """
        Accepts a set of known instances of CPE Names and a candidate CPE Name,
        and returns 'True' if the candidate can be shown to be
        an instance based on the content of the known instances.
        Otherwise, it returns 'False'.

        :param CPESet self: A set of m known CPE Names K = {K1, K2, …, Km}.
        :param CPE cpe: A candidate CPE Name X.
        :returns: True if X matches K, otherwise False.
        :rtype: boolean
        """

        # An empty set not matching with any CPE
        if len(self) == 0:
            return False

        # If input CPE Name string is in set of CPE Name strings
        # not do searching more because there is a matching
        for k in self.K:
            if (k.cpe_str == cpe.cpe_str):
                return True

        # If "cpe" is an empty CPE Name any system matches
        if len(cpe) == 0:
            return True

        # There are not a CPE Name string in set equal to
        # input CPE Name string
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

            # Next part in input CPE Name

        # All parts in input CPE Name matched
        return True
