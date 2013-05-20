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
from cpe2_3_uri import CPE2_3_URI
from cpe2_3_wfn import CPE2_3_WFN
from cpe2_3_fs import CPE2_3_FS


class CPE2_3(CPEBASE):
    """
    Implementation of CPE 2.3 specification.
    """

    # CPE version
    VERSION = '2.3'

    # Constants of valid CPE name styles of 2.3 version
    STYLE_URI = "URI"
    STYLE_WFN = "WFN"
    STYLE_FS = "formatted string"

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

    KEY_PART_HW = "h"
    KEY_PART_OS = "o"
    KEY_PART_APP = "a"

    # List of part keys of binding style uri
    uri_part_keys = [KEY_PART,
                     KEY_VENDOR,
                     KEY_PRODUCT,
                     KEY_VERSION,
                     KEY_UPDATE,
                     KEY_EDITION,
                     KEY_LANGUAGE]

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

    # Binding style dictionary
    binding_styles = {
        STYLE_URI: CPE2_3_URI,
        STYLE_WFN: CPE2_3_WFN,
        STYLE_FS: CPE2_3_FS
    }

    def __new__(cls, style=STYLE_URI, *args, **kwargs):
        try:
            return CPE2_3.binding_styles[style](*args, **kwargs)
        except KeyError:
            raise NotImplementedError(u'Invalid binding style of 2.3 version CPE name')
