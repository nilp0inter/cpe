#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is part of cpe package.

This module contains the common characteristics of any
style of CPE name of version 2.3 of CPE (Common Platform Enumeration)
specification.

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

import itertools


class CPE2_3(CPE):
    """
    Represents a generic CPE name compatible with
    all CPE name style of version 2.3 of CPE specification.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Constants associated with regular expressions
    _ALPHA = "a-zA-Z"
    _DIGIT = "\d"

    # Constants of possible CPE name styles of 2.3 version
    STYLE_UNDEFINED = "undefined"
    STYLE_URI = "URI"
    STYLE_WFN = "WFN"
    STYLE_FS = "FS"

    # Dictionary keys associated with components of some styles of
    # version 2.3 of CPE name
    KEY_SW_EDITION = "sw_edition"
    KEY_TARGET_SW = "target_sw"
    KEY_TARGET_HW = "target_hw"
    KEY_OTHER = "other"

    ###############
    #  VARIABLES  #
    ###############

    # List of new part keys in binding style WFN
    ext_part_keys = [KEY_SW_EDITION,
                     KEY_TARGET_SW,
                     KEY_TARGET_HW,
                     KEY_OTHER]

    ext_ordered_part_dict = {
        7: KEY_SW_EDITION,
        8: KEY_TARGET_SW,
        9: KEY_TARGET_HW,
        10: KEY_OTHER
    }

    wfn_part_keys = set(itertools.chain(CPE.uri_part_keys,
                                        ext_part_keys))

    wfn_ordered_part_dict = dict(CPE.uri_ordered_part_dict,
                                 **ext_ordered_part_dict)
    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str):
        """
        Initializes the CPE name object.
        """

        CPE.__init__(self, cpe_str)
        CPE.version = CPE.VERSION_2_3
        CPE2_3.style = CPE2_3.STYLE_UNDEFINED
