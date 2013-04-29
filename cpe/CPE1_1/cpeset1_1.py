#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpeset1_1.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Implementation of matching algorithm
             in accordance with version 1.1 of specification CPE
             (Common Platform Enumeration).

             This class allows:
             - create set of CPE elements
             - match a CPE element against a set of CPE elements
'''


from cpe1_1 import CPE1_1


class CPESet1_1(object):
    """
    Represents a set of CPEs.
    """

    def __init__(self):
        """
        Create an empty set of CPEs.
        """
        self.K = []

    def append(self, cpe):
        """
        Adds a CPE element to the set.
        """

        if (cpe not in self.K):
            self.K.append(cpe)

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
        """

        return len(self.K)

    def __unicode__(self):
        """
        Returns CPE set as string.

        - TEST: empty set
        >>> s = CPESet1_1()
        >>> s.__unicode__()
        'Set contains 0 elements'

        - TEST: set with three CPE elements
        >>> uri1 = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
        >>> uri2 = 'cpe://microsoft:windows:xp!vista'
        >>> uri3 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> c3 = CPE1_1(uri3)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c3)
        >>> print s.__unicode__()
        Set contains 3 elements:
            cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52
            cpe://microsoft:windows:xp!vista
            cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise

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

    @classmethod
    def _compare_subcomp(cls, x, y):
        """
        Compares two subcomponents of CPE name.

        In next example, c1, c2 and c3 are subcomponents.
        a nd b are components with a subcomponent.

        cpe:/a:b:c1!c2!c3

        Each subcomponent has two fields:
            - operator
            - name (string alue)

        - TEST: compare two different subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
        >>> x[CPE1_1.KEY_COMP_NAME] = "cisco"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
        >>> y[CPE1_1.KEY_COMP_NAME] = "nvidia"
        >>> CPESet1_1._compare_subcomp(x, y)
        False

        - TEST: compare two equal subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
        >>> x[CPE1_1.KEY_COMP_NAME] = "cisco"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
        >>> y[CPE1_1.KEY_COMP_NAME] = "cisco"
        >>> CPESet1_1._compare_subcomp(x, y)
        True

        - TEST: compare empty and not empty subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
        >>> x[CPE1_1.KEY_COMP_NAME] = ""
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
        >>> y[CPE1_1.KEY_COMP_NAME] = "cisco"
        >>> CPESet1_1._compare_subcomp(x, y)
        False

        - TEST: compare OR and NOT subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_OR
        >>> x[CPE1_1.KEY_COMP_NAME] = "linux"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NOT
        >>> y[CPE1_1.KEY_COMP_NAME] = "cisco"
        >>> CPESet1_1._compare_subcomp(x, y)
        True
        >>> CPESet1_1._compare_subcomp(y, x)
        True

        - TEST: compare OR and NOT subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_OR
        >>> x[CPE1_1.KEY_COMP_NAME] = "linux"
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NOT
        >>> y[CPE1_1.KEY_COMP_NAME] = "linux"
        >>> CPESet1_1._compare_subcomp(x, y)
        False
        >>> CPESet1_1._compare_subcomp(y, x)
        False

        - TEST: compare ANY and NOT subcomponents
        >>> s = CPESet1_1()
        >>> x = dict()
        >>> x[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_ANY
        >>> x[CPE1_1.KEY_COMP_NAME] = ""
        >>> y = dict()
        >>> y[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NOT
        >>> y[CPE1_1.KEY_COMP_NAME] = "linux"
        >>> CPESet1_1._compare_subcomp(x, y)
        True
        >>> CPESet1_1._compare_subcomp(y, x)
        True
        """

        op_x = x[CPE1_1.KEY_COMP_OP]
        name_x = x[CPE1_1.KEY_COMP_NAME]

        op_y = y[CPE1_1.KEY_COMP_OP]
        name_y = y[CPE1_1.KEY_COMP_NAME]

        if (op_x == CPE1_1.OP_ANY):
            match = True
        elif (op_x == CPE1_1.OP_NONE):
            if (op_y == CPE1_1.OP_NOT):
                match = name_x != name_y
            else:
                match = name_x == name_y
        elif (op_x == CPE1_1.OP_NOT):
            if (op_y == CPE1_1.OP_NOT):
                match = name_x == name_y
            else:
                match = name_x != name_y
        elif (op_x == CPE1_1.OP_OR):
            if (op_y == CPE1_1.OP_NONE):
                match = name_x == name_y
            else:
                match = name_x != name_y
        else:
            raise TypeError("Operator in CPE element not valid")

        return match

    def name_matching(self, cpe):
        """
        Accepts a set of known instance CPE Names and a candidate CPE Name,
        and delivers the answer 'true' if the candidate can be shown to be
        an instance based on the content of the known instances.
        Otherwise, it returns 'false'.

        Inputs:
            - self: A set of m known CPE Names K = {K1, K2, …, Km}.
            - cpe: A candidate CPE Name X.
        Output:
            - True if X matches K, False otherwise.

        - TEST: matching (identical cpe in set)
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.name_matching(c2)
        True

        - TEST: matching with ANY values (cpe in set)
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe:/cisco'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_matching(c3)
        True

        - TEST: matching with ANY values (cpe in set)
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe://microsoft:::'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_matching(c3)
        True

        - TEST: matching with NOT (cpe in set)
        >>> uri1 = 'cpe://microsoft:windows:~xp'
        >>> c1 = CPE1_1(uri1)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> uri2 = 'cpe://microsoft:windows:vista'
        >>> c2 = CPE1_1(uri2)
        >>> s.name_matching(c2)
        True

        - TEST: matching with OR (cpe in set)
        >>> uri1 = 'cpe://microsoft:windows:xp!vista'
        >>> uri2 = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
        >>> c1 = CPE1_1(uri1)
        >>> c2 = CPE1_1(uri2)
        >>> s = CPESet1_1()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> uri3 = 'cpe://microsoft:windows:vista'
        >>> c3 = CPE1_1(uri3)
        >>> s.name_matching(c3)
        True
        """

        # An empty set not matching with any "cpe"
        if len(self) == 0:
            return False

        # If "cpe" URI string is in set of URI string
        # not do searching and matching
        for k in self.K:
            if (k.uri == cpe.uri):
                return True

        # There are not a CPE URI string in set equal to
        # "cpe" URI string
        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]
        for p in parts_key:
            elems_cpe = cpe.cpe_dict[p]
            for ec in elems_cpe:

                # Searching

                # Each element ec in cpe[p] is compared with
                # each element ek in element k[p] in set

                for k in self.K:
                    elems_k = k.cpe_dict[p]

                    if len(elems_cpe) <= len(elems_k):
                        for ek in elems_k:

                            # Matching

                            match = False

                            # Each component in element ec in "cpe"
                            # is compared with each component
                            # in element ek in k[p] in set
                            for i in range(0, min(len(ec), len(ek))):
                                comp_cpe = ec[i]
                                comp_k = ek[i]

                                if (len(comp_cpe) == len(comp_k)) and (len(comp_cpe) == 1):
                                    subcomp_cpe = comp_cpe[0]
                                    subcomp_k = comp_k[0]

                                    match = CPESet1_1._compare_subcomp(subcomp_cpe, subcomp_k)

                                else:
                                    for sc in comp_cpe:
                                        for sk in comp_k:
                                            match = CPESet1_1._compare_subcomp(sc, sk)
                                            if match:
                                                # Subcomponent matched
                                                break

                                        if not match:
                                            # Subcomponent in "cpe" component not exist
                                            # Search subcomponent in another element in k
                                            break

                                    # List of subcomponents in "cpe" component analyzed

                                if not match:
                                    # Search subcomponent in another element in k
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
            # Next part in "cpe"

        # all parts in "cpe" matched
        return True

if __name__ == "__main__":

#    uri1 = 'cpe://microsoft:windows:xp!vista'
#    uri2 = 'cpe:/cisco:55:3825;cisco:2:44/cisco:ios:12.3:enterprise'
#    c1 = CPE1_1(uri1)
#    c2 = CPE1_1(uri2)
#    s = CPESet1_1()
#    s.append(c1)
#    #s.append(c2)
#    uri3 = 'cpe://microsoft::'
#    c3 = CPE1_1(uri3)

#    print(s.__unicode__())
#    print(c3)
#    print(s.name_matching(c3))

    import doctest
    doctest.testmod()
