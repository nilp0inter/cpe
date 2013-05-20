#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe2_3.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Module for the treatment of identifiers in accordance with
             version 2.3 of specification CPE (Common Platform Enumeration).
'''

from cpe2_3_uri import CPE2_3_URI
from cpe2_3_wfn import CPE2_3_WFN
from cpe2_3_fs import CPE2_3_FS


class CPE2_3(object):
    """
    Implementation of CPE 2.3 specification.
    """

    # CPE version
    VERSION = '2.3'

    # Constants of valid CPE name styles of 2.3 version
    STYLE_URI = "URI"
    STYLE_WFN = "WFN"
    STYLE_FS = "formatted string"

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
            msg = u'Invalid binding style of 2.3 version CPE name'
            raise NotImplementedError(msg)
