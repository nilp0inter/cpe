#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: factorycpe.py
Author: Alejandro Galindo
Date: 23-04-2013
Description: Factory of CPE objects for creating various types of CPE name,
             associated with the different versions of specification
             Common Platform Enumeration (CPE).
"""

from cpe import CPE
from cpe1_1 import CPE1_1
from cpe2_2 import CPE2_2
from cpe2_3 import CPE2_3
from factorycpe2_3 import FactoryCPE2_3


class FactoryCPE(object):
    """
    This class implements the factory pattern that makes a class centralizes
    the creation of objects of a particular common subtype,
    hiding the user the requested object instance.
    """

    ###############
    #  VARIABLES  #
    ###############

    #List of implemented versions of CPE names
    _cpe_versions = {
        CPE.VERSION_1_1: CPE1_1,
        CPE.VERSION_2_2: CPE2_2,
        CPE.VERSION_2_3: CPE2_3
    }

    ###################
    #  CLASS METHODS  #
    ###################

    @staticmethod
    def get_cpe(version=CPE.VERSION_2_3, style=CPE2_3.STYLE_WFN, cpe_str="wfn:[]"):
        """
        Create a CPE name object associated with cpe_str string,
        accordance to a version of CPE specification. If version is 2.3 then
        CPE name will have input style (WFN, formatted string or URI).

        - TEST: good CPE name with 2.3 version and WFN style
        >>> FactoryCPE.get_cpe() # doctest: +ELLIPSIS
        <__main__.CPE2_3_WFN at 0x...>

        - TEST: good CPE name with 1.1 version
        >>> FactoryCPE.get_cpe("1.1", "", "cpe:///") # doctest: +ELLIPSIS
        <__main__.CPE1_1 at 0x...>

        - TEST: good CPE name with 2.2 version
        >>> FactoryCPE.get_cpe("2.2", "", "cpe:/h:hp") # doctest: +ELLIPSIS
        <__main__.CPE2_2 at 0x...>

        - TEST: bad CPE name
        >>> FactoryCPE.get_cpe("5.0", "", "cpe:/h:hp")
        Traceback (most recent call last):
        NotImplementedError: Version of CPE name not implemented
        """

        if version not in FactoryCPE._cpe_versions:
            raise NotImplementedError('Version of CPE name not implemented')

        if version == CPE.VERSION_2_3:
            return FactoryCPE2_3.get_cpe(style, cpe_str)
        else:
            return FactoryCPE._cpe_versions[version](cpe_str)

if __name__ == "__main__":

    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
