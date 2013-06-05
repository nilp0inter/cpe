#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module is an implementation of factory
of CPE objects for creating various types of CPE names of version 2.3
of CPE (Common Platform Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo

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
