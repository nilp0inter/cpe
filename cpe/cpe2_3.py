#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpe2_3.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Contains the common characteristics of any style of CPE name
             of version 2.3 of CPE (Common Platform Enumeration)
             specification.
"""

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

    # Constants of valid CPE name styles of 2.3 version
    STYLE_URI = "URI"
    STYLE_WFN = "WFN"
    STYLE_FS = "formatted string"

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