#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe.py
Author: Alejandro Galindo
Date: 17-04-2013
Description: TODO.
'''

from CPE1_1.cpe1_1 import CPE1_1
from CPE2_2.cpe2_2 import CPE2_2
from CPE2_3.cpe2_3 import CPE2_3


class CPE(object):
    """
    TODO
    """

    cpe_versions = {
        '1.1': CPE1_1,
        '2.2': CPE2_2,
        '2.3': CPE2_3
    }

    def __new__(cls, version='2.3', *args, **kwargs):
        try:
            return CPE.cpe_versions[version](*args, **kwargs)
        except KeyError:
            raise NotImplementedError(u'Versión de CPE no implementada')
