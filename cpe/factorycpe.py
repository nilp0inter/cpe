#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module is an implementation of factory
of CPE objects for creating various types of CPE names,

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

from cpe import CPE
from cpe1_1 import CPE1_1
from cpe2_2 import CPE2_2
from cpe2_3 import CPE2_3
from factorycpe2_3 import FactoryCPE2_3


class FactoryCPE(object):
    """
    Generator of CPE objects.

    This class implements the factory pattern, that is, this class centralizes
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
    def get_cpe(version=CPE.VERSION_2_3,
                style=CPE2_3.STYLE_WFN, cpe_str="wfn:[]"):
        """
        Create a CPE name object associated with cpe_str string,
        accordance to a version of CPE specification. If version is 2.3 then
        CPE name will have input style (WFN, formatted string or URI).

        - TEST: good CPE name with 2.3 version and WFN style
        >>> FactoryCPE.get_cpe() # doctest: +ELLIPSIS
        <cpe2_3_wfn.CPE2_3_WFN object at 0x...>

        - TEST: good CPE name with 1.1 version
        >>> FactoryCPE.get_cpe("1.1", "", "cpe:///") # doctest: +ELLIPSIS
        <cpe1_1.CPE1_1 object at 0x...>

        - TEST: good CPE name with 2.2 version
        >>> FactoryCPE.get_cpe("2.2", "", "cpe:/h:hp") # doctest: +ELLIPSIS
        <cpe2_2.CPE2_2 object at 0x...>

        - TEST: bad CPE name
        >>> FactoryCPE.get_cpe("5.0", "", "cpe:/h:hp") # doctest: +IGNORE_EXCEPTION_DETAIL
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
    doctest.testmod()
