#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpeset.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Contains the common characteristics of any set of CPE names
             associated with a version of Common Platform Enumeration (CPE)
             specification.

             This class allows:
             - create set of CPE elements
             - add elements
"""


from cpe import CPE

class CPESet(object):
    """
    Represents a set of CPEs.
    """

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, version):
        """
        Create an empty set of CPEs.
        """
        
        if version not in CPE._cpe_versions:
            msg = "Version of CPE name set not implemented"
            raise NotImplementedError(msg)

        self.version = version
        self.K = []

    def __len__(self):
        """
        Returns the count of CPE elements of set.
        """

        return len(self.K)

    def __unicode__(self):
        """
        Returns CPE set as string.
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

if __name__ == "__main__":

    import doctest
    doctest.testmod()
