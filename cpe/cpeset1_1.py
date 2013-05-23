#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpeset1_1.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Implementation of matching algorithm
             in accordance with version 1.1 of specification CPE
             (Common Platform Enumeration).

             This class allows:
             - create set of CPE elements
             - match a CPE element against a set of CPE elements
"""


from cpe1_1 import CPE1_1


class CPESet1_1(object):
    """
    Represents a set of CPEs.
    """

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _compare_subcomp(cls, x, y):
        """
        Compares two subcomponents of CPE name.

        In next example, a and b are components with a subcomponent.
        c1, c2 and c3 are subcomponents of last component.
        
        cpe:/a:b:c1!c2!c3

        Each subcomponent has two fields:
            - operator
            - name (string value)

        - TEST: compare two different subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NONE
        >>> x[CPE1_1.KEY_COMP_STR] = "cisco"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NONE
        >>> y[CPE1_1.KEY_COMP_STR] = "nvidia"
        >>> CPESet1_1._compare_subcomp(x, y)
        False

        - TEST: compare two equal subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NONE
        >>> x[CPE1_1.KEY_COMP_STR] = "cisco"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NONE
        >>> y[CPE1_1.KEY_COMP_STR] = "cisco"
        >>> CPESet1_1._compare_subcomp(x, y)
        True

        - TEST: compare empty and not empty subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NONE
        >>> x[CPE1_1.KEY_COMP_STR] = ""
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NONE
        >>> y[CPE1_1.KEY_COMP_STR] = "cisco"
        >>> CPESet1_1._compare_subcomp(x, y)
        False

        - TEST: compare OR and NOT subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_OR
        >>> x[CPE1_1.KEY_COMP_STR] = "linux"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NOT
        >>> y[CPE1_1.KEY_COMP_STR] = "cisco"
        >>> CPESet1_1._compare_subcomp(x, y)
        True
        >>> CPESet1_1._compare_subcomp(y, x)
        True

        - TEST: compare OR and NOT subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_OR
        >>> x[CPE1_1.KEY_COMP_STR] = "linux"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NOT
        >>> y[CPE1_1.KEY_COMP_STR] = "linux"
        >>> CPESet1_1._compare_subcomp(x, y)
        False
        >>> CPESet1_1._compare_subcomp(y, x)
        False

        - TEST: compare ANY and NOT subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_ANY
        >>> x[CPE1_1.KEY_COMP_STR] = ""
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.VALUE_COMP_OP_NOT
        >>> y[CPE1_1.KEY_COMP_STR] = "linux"
        >>> CPESet1_1._compare_subcomp(x, y)
        True
        >>> CPESet1_1._compare_subcomp(y, x)
        True
        """

        op_x = x[CPE1_1.KEY_COMP_OP]
        name_x = x[CPE1_1.KEY_COMP_STR]

        op_y = y[CPE1_1.KEY_COMP_OP]
        name_y = y[CPE1_1.KEY_COMP_STR]

        if ((op_x == CPE1_1.VALUE_COMP_OP_ANY) or
            (op_y == CPE1_1.VALUE_COMP_OP_ANY)):
            match = True
        elif (op_x == CPE1_1.VALUE_COMP_OP_NONE):
            if (op_y == CPE1_1.VALUE_COMP_OP_NOT):
                match = name_x != name_y
            else:
                match = name_x == name_y
        elif (op_x == CPE1_1.VALUE_COMP_OP_NOT):
            if (op_y == CPE1_1.VALUE_COMP_OP_NOT):
                match = name_x == name_y
            else:
                match = name_x != name_y
        elif (op_x == CPE1_1.VALUE_COMP_OP_OR):
            if (op_y == CPE1_1.VALUE_COMP_OP_NOT):
                match = name_x != name_y
            else:
                match = name_x == name_y
        else:
            msg = "Malformed subcomponent: operator '%s' in '%s' not valid" % (op_x, name_x)
            raise ValueError(msg)

        return match

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self):
        """
        Create an empty set of CPEs.
        """
        self.K = []

    def __len__(self):
        """
        Returns the count of CPE elements of set.

        - TEST: empty set
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

    def __unicode__(self):
        """
        Returns CPE set as string.

        - TEST: empty set
        >>> s = CPESet1_1()
        >>> s.__unicode__()
        'Set contains 0 elements'
        """

        len = self.__len__()

        str = "Set contains %s elements" % len
        if len > 0:
            str += ":\n"

            for i in range(0, len):
                str += "    %s" % self.K[i].__unicode__()

                if i+1 < len:
                    str += "\n"

        return str

    def __getitem__(self, i):
        """
        Returns the i'th CPE element of set.
        """

        return self.K[i]

    def append(self, cpe):
        """
        Adds a CPE element to the set if not already.
        """

        for k in self.K:
            if cpe.str == k.str:
                return None

        self.K.append(cpe)

    def name_match(self, cpe):
        """
        Accepts a set of known instance CPE Names and a candidate CPE Name,
        and delivers the answer 'True' if the candidate can be shown to be
        an instance based on the content of the known instances.
        Otherwise, it returns 'False'.

        Inputs:
            - self: A set of m known CPE Names K = {K1, K2, …, Km}.
            - cpe: A candidate CPE Name X.
        Output:
            - True if X matches K, otherwise False.

        - TEST: matching with identical CPE in set
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
        True
        """

        # An empty set not matching with any CPE
        if len(self) == 0:
            return False

        # If input CPE name string is in set of CPE name strings
        # not do searching more because there is a matching
        for k in self.K:
            if (k.str == cpe.str):
                return True

        # There are not a CPE name string in set equal to
        # input CPE name string
        for p in CPE1_1.cpe_part_keys:
            elems_cpe = cpe._cpe_dict[p]
            for ec in elems_cpe:

                # Search of element of part of input CPE

                # Each element ec of input cpe[p] is compared with
                # each element ek of k[p] in set K

                for k in self.K:
                    elems_k = k._cpe_dict[p]

                    if len(elems_cpe) <= len(elems_k):
                        for ek in elems_k:

                            # Matching

                            match = False

                            # Each component in element ec is compared with
                            # each component in element ek
                            for i in range(0, min(len(ec), len(ek))):
                                comp_cpe = ec[i]
                                comp_k = ek[i]

                                if ((len(comp_cpe) == len(comp_k)) and
                                    (len(comp_cpe) == 1)):

                                    # Components have a only subcomponent
                                    subcomp_cpe = comp_cpe[0]
                                    subcomp_k = comp_k[0]

                                    match = CPESet1_1._compare_subcomp(subcomp_cpe, subcomp_k)

                                else:
                                    # Several subcomponents to evaluate
                                    for sc in comp_cpe:
                                        for sk in comp_k:
                                            match = CPESet1_1._compare_subcomp(sc, sk)
                                            if match:
                                                # Subcomponent matched
                                                break

                                        # If subcomponent found then exit,
                                        # otherwise, the search continues
                                        if match:
                                            break

                                    # List of subcomponents analyzed

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
