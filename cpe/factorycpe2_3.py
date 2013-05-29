#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: factorycpe2_3.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Factory of CPE objects for creating various types of CPE name,
             of version 2.3 of Common Platform Enumeration (CPE)
             specification.
"""

from cpe2_3 import CPE2_3
from cpe2_3_uri import CPE2_3_URI
from cpe2_3_wfn import CPE2_3_WFN
from cpe2_3_fs import CPE2_3_FS


class FactoryCPE2_3(object):
    """
    This class implements the factory pattern that makes a class centralizes
    the creation of objects of a particular common subtype,
    hiding the user the requested object instance.

    - TEST: good CPE name with 2.3 version and WFN style
    >>> FactoryCPE2_3.get_cpe() # doctest: +ELLIPSIS
    <cpe2_3_wfn.CPE2_3_WFN object at 0x...>

    - TEST: good CPE name with 2.3 version and URI style:
    >>> FactoryCPE2_3.get_cpe("URI", "cpe:/a:acme:product:1.0:pro:en-us") # doctest: +ELLIPSIS
    <cpe2_3_uri.CPE2_3_URI object at 0x...>

    - TEST: good CPE name with 2.3 version and formatted string style
    >>> FactoryCPE2_3.get_cpe("FS", "cpe:2.3:o:linux:suse:*:*:*:*:*:*:*:*") # doctest: +ELLIPSIS
    <cpe2_3_fs.CPE2_3_FS object at 0x...>

    - TEST: bad CPE name
    >>> FactoryCPE2_3.get_cpe("bad style", "cpe:/h:hp")
    Traceback (most recent call last):
    NotImplementedError: Style of CPE name not implemented
    """

    ###############
    #  VARIABLES  #
    ###############

    _cpe_styles = {
        CPE2_3.STYLE_URI: CPE2_3_URI,
        CPE2_3.STYLE_WFN: CPE2_3_WFN,
        CPE2_3.STYLE_FS: CPE2_3_FS
    }

    ###################
    #  CLASS METHODS  #
    ###################

    @staticmethod
    def get_cpe(style=CPE2_3.STYLE_WFN, cpe_str="wfn:[]"):
        """
        Create a CPE name object associated with cpe_str string,
        accordance to style of 2.3 version of CPE specification.
        """

        if style not in FactoryCPE2_3._cpe_styles:
            raise NotImplementedError('Style of CPE name not implemented')

        return FactoryCPE2_3._cpe_styles[style](cpe_str)

if __name__ == "__main__":

    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
