#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpebase.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Contiene los elementos y la funcionalidad común
             entre versiones de CPE.
'''

import pprint


class CPEBASE(object):
    """
    Represents a generic CPE identifier compatible with all CPE versions.
    """

    def __init__(self, cpe_uri):
        """
        Save input CPE identifier and create a dictionary to store its
        elements.
        """

        # Store CPE identifier URI:
        #     CPE names are case-insensitive.
        #     To reduce potential for confusion,
        #     all CPE Names should be written in lowercase
        self.cpe_uri = cpe_uri.lower()

        # Dictionary to store CPE identifier URI elements
        self.cpe_dict = {}

    def __str__(self):
        pp = pprint.PrettyPrinter(indent=5, width=80)

        return "CPE %s => %s\n\n%s\n" % (self.VERSION,
                                         self.cpe_uri,
                                         pp.pformat(self.cpe_dict))
