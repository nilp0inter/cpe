#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe2_3.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Module for the treatment of identifiers in accordance with
             version 2.3 of specification CPE (Common Platform Enumeration).
'''

from cpe.cpebase import CPEBASE


class CPE2_3_BASE(CPEBASE):
    """
    Implementation of CPE 2.3 specification.
    """

    # CPE version
    VERSION = '2.3'

    # Constants of valid CPE name styles of 2.3 version
    STYLE_URI = "URI"
    STYLE_WFN = "WFN"
    STYLE_FS = "formatted string"

    # Constants associated with regular expressions
    ALPHA = "a-zA-Z"
    DIGIT = "\d"

    # Constants associated with dictionary keys that
    # store CPE name elements
    KEY_PART = "part"
    KEY_VENDOR = "vendor"
    KEY_PRODUCT = "product"
    KEY_VERSION = "version"
    KEY_UPDATE = "update"
    KEY_EDITION = "edition"
    KEY_LANGUAGE = "language"
    KEY_SW_EDITION = "sw_edition"
    KEY_TARGET_SW = "target_sw"
    KEY_TARGET_HW = "target_hw"
    KEY_OTHER = "other"

    VALUE_PART_HW = "h"
    VALUE_PART_OS = "o"
    VALUE_PART_APP = "a"

    # List of part keys of binding style URI
    uri_part_keys = [KEY_PART,
                     KEY_VENDOR,
                     KEY_PRODUCT,
                     KEY_VERSION,
                     KEY_UPDATE,
                     KEY_EDITION,
                     KEY_LANGUAGE]

    # List of part keys of binding style WFN
    extend_part_keys = [KEY_SW_EDITION,
                        KEY_TARGET_SW,
                        KEY_TARGET_HW,
                        KEY_OTHER]

    # Mapping between order of parts and its value
    uri_order_parts_dict = {
        0: KEY_PART,
        1: KEY_VENDOR,
        2: KEY_PRODUCT,
        3: KEY_VERSION,
        4: KEY_UPDATE,
        5: KEY_EDITION,
        6: KEY_LANGUAGE
    }

    extend_order_parts_dict = {
        7: KEY_SW_EDITION,
        8: KEY_TARGET_SW,
        9: KEY_TARGET_HW,
        10: KEY_OTHER
    }

    def __init__(self, cpe_str):
        """
        TODO
        """

        CPEBASE.__init__(self, cpe_str)
