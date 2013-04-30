#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpeset2_2.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Implementation of matching algorithm
             in accordance with version 2.2 of specification CPE
             (Common Platform Enumeration).

             This class allows:
             - create set of CPE elements
             - match a CPE element against a set of CPE elements
'''


from cpe2_2 import CPE2_2


class CPESet2_2(object):
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

        for k in self.K:
            if cpe == k:
                return None

        self.K.append(cpe)

    def __len__(self):
        """
        Returns the count of CPE elements of set.

        - TEST: empty set
        >>> s = CPESet2_2()
        >>> len(s)
        0

        - TEST: set with two CPE elements
        >>> uri1 = 'cpe:/o:sun:solaris:5.8'
        >>> uri2 = 'cpe:/a:microsoft:office:2003'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> len(s)
        2

        - TEST: set with three CPE elements and one repeated
        >>> uri1 = 'cpe:/o:sun:solaris:5.8'
        >>> uri2 = 'cpe:/a:microsoft:office:2003'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> c3 = CPE2_2(uri2)
        >>> s = CPESet2_2()
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
        >>> s = CPESet2_2()
        >>> s.__unicode__()
        'Set contains 0 elements'

        - TEST: set with three CPE elements
        >>> uri1 = 'cpe:/o:sun:solaris:5.8'
        >>> uri2 = 'cpe:/a:microsoft:office:2003'
        >>> uri3 = 'cpe:/a:adobe:reader'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> c3 = CPE2_2(uri3)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.append(c3)
        >>> print s.__unicode__()
        Set contains 3 elements:
            cpe:/o:sun:solaris:5.8
            cpe:/a:microsoft:office:2003
            cpe:/a:adobe:reader
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

    def name_matching(self, cpe):
        """
        Accepts a set of CPE Names K and a candidate CPE Name X. It returns
        'True' if X matches any member of K, and 'False' otherwise.

        Inputs:
            - self: A list of m CPE Names K = {K1, K2, …, Km}.
            - cpe: A candidate CPE Name X.
        Output:
            - True if X matches K, False otherwise.

        - TEST: matching (identical cpe in set)
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
        >>> s.name_matching(m)
        True

        - test: matching with any values (cpe in set)
        >>> uri1 = 'cpe:/o:redhat:enterprise_linux:3'
        >>> uri2 = 'cpe:/o:sun:sunos:5.8'
        >>> uri3 = 'cpe:/o:sun'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> m = CPE2_2(uri3)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.name_matching(m)
        True

        - test: not matching
        >>> uri1 = 'cpe:/o:redhat:enterprise_linux:3'
        >>> uri2 = 'cpe:/o:sun:sunos:5.8'
        >>> uri3 = 'cpe:/a:microsoft:ie:9'
        >>> c1 = CPE2_2(uri1)
        >>> c2 = CPE2_2(uri2)
        >>> m = CPE2_2(uri3)
        >>> s = CPESet2_2()
        >>> s.append(c1)
        >>> s.append(c2)
        >>> s.name_matching(m)
        False
        """

        match = False

        for n in self.K:
            if (len(n) >= len(cpe)):
                for c in range(0, len(cpe)):
                    key = CPE2_2.order_parts_dict[c]
                    comp_cpe = cpe.cpe_dict[key]
                    comp_n = n.cpe_dict[key]

                    match = ((comp_cpe == comp_n) or
                             (comp_cpe == "") or
                             (comp_cpe is None))

                    if not match:
                        break

                if match:
                    break
                #match = comp_cpe == comp_n

               # print(comp_cpe)
               # print(comp_n)
               # print("")

               # if not match:

               #     # comp_cpe is simple text?

               #     cpe_is_text = ((comp_cpe is not None) and
               #                    (comp_cpe != "-") and
               #                    (comp_cpe != ""))

               #     match = cpe_is_text and (comp_n != "-")

               #     if not match:

               #         # comp_cpe is None?

               #         cpe_is_none = ((comp_cpe == "") or
               #                        (comp_cpe is None))

               #         match = cpe_is_none and (comp_n != "-")

               #         if not match:

               #             # Search another n CPE name
               #             break

           # if match:
           #     break

        return match

if __name__ == "__main__":

#    uri1 = 'cpe:/o:redhat:enterprise_linux:3'
#    uri2 = 'cpe:/o:sun:sunos:5.8'
#    c1 = CPE2_2(uri1)
#    c2 = CPE2_2(uri2)
#    s = CPESet2_2()
#    s.append(c1)
#    s.append(c2)
#    uri3 = 'cpe:/a:microsoft:ie:9'
#    c3 = CPE2_2(uri3)
#
#    print(s.__unicode__())
#    print(c3)
#    print(s.name_matching(c3))

    import doctest
    doctest.testmod()
