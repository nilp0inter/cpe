#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: factorycpe.py
Author: Alejandro Galindo
Date: 23-04-2013
Description: Factory of CPE objects for creating various types of CPE name,
             associated with the different versions of specification
             Common Platform Enumeration (CPE).
'''

from cpe import CPE
from cpe1_1 import CPE1_1
from cpe2_2 import CPE2_2
from cpe2_3 import CPE2_3
from factorycpe2_3 import FactoryCPE2_3


class FactoryCPE(object):
    """
    This class implements the factory pattern that makes a class centralizes
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
    def get_cpe(version=CPE.VERSION_2_3, style=CPE2_3.STYLE_WFN, cpe_str="wfn:[]"):
        if version not in FactoryCPE._cpe_versions:
            raise NotImplementedError('Version of CPE name not implemented')

        if version == CPE.VERSION_2_3:
            return FactoryCPE2_3.get_cpe(style, cpe_str)
        else:
            return FactoryCPE._cpe_versions[version](cpe_str)
