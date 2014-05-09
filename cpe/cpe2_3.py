#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with version 2.3 of CPE (Common Platform Enumeration)
specification.

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


class CPE2_3(CPE):
    """
    Represents a generic CPE name compatible with
    all CPE name style of version 2.3 of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants of possible CPE name styles of 2.3 version

    #: Formatted string style of version 2.3 of CPE specification
    STYLE_FS = "FS"

    #: Uniform Resource Identifier(URI) style of version 2.3
    #: of CPE specification
    STYLE_URI = "URI"

    #: Well-Formed Name (WFN) style of version 2.3 of CPE specification
    STYLE_WFN = "WFN"

    #: Style of version 2.3 of CPE specification not set
    STYLE_UNDEFINED = "undefined"

    #: Version of CPE name
    VERSION = CPE.VERSION_2_3

    #: Style of CPE name
    STYLE = STYLE_UNDEFINED

    ####################
    #  OBJECT METHODS  #
    ####################

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Generator of CPE Names according to version 2.3.

        :param string cpe_str: CPE Name string
        :returns: CPE object of version 2.3 with style
            detected correctly
        :rtype: CPE2_3
        :exception: NotImplementedError - incorrect CPE Name or
            version of CPE not implemented

        This class implements the factory pattern, that is,
        this class centralizes the creation of objects of a particular
        CPE style of version 2.3, hiding the user the requested
        object instance.
        """

        from .cpe2_3_fs import CPE2_3_FS
        from .cpe2_3_uri import CPE2_3_URI
        from .cpe2_3_wfn import CPE2_3_WFN

        # List of implemented styles of version 2.3 of CPE names
        _CPE_STYLES = {
            CPE2_3.STYLE_FS: CPE2_3_FS,
            CPE2_3.STYLE_URI: CPE2_3_URI,
            CPE2_3.STYLE_WFN: CPE2_3_WFN}

        errmsg = 'Style of version 2.3 of CPE not implemented'

        # Detect CPE version of input CPE name
        for s in _CPE_STYLES:
            try:
                # Validate CPE name
                c = _CPE_STYLES[s](cpe_str)
            except ValueError:
                # Test another style
                continue
            else:
                # Style detected
                return c

        raise NotImplementedError(errmsg)

    def __str__(self):
        """
        Returns a human-readable representation of CPE Name.

        :returns: Representation of CPE Name as string
        :rtype: string
        """

        return "CPE v{0} ({1}): {2}".format(CPE2_3.VERSION,
                                            self.STYLE,
                                            self.cpe_str)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile('tests/testfile_cpe2_3.txt')
