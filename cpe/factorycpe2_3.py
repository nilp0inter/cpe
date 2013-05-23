#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: factorycpe2_3.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Factory of CPE objects for creating various types of CPE name,
             of version 2.3 of Common Platform Enumeration (CPE)
             specification.
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
        if style not in FactoryCPE2_3._cpe_styles:
            raise NotImplementedError(u'CPE name style not implemented')

        return FactoryCPE2_3._cpe_styles[style](cpe_str)
