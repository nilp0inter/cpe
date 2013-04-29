#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpebase.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Common elements and functions among CPE specification versions.
'''

import pprint


class CPEBASE(object):
    """
    Represents a generic CPE name compatible with
    all CPE specification versions.
    """

    def __init__(self):
        """
        Creates a dictionary to store CPE elements.
        """

        self.cpe_dict = {}

    def __str__(self):
        """
        Returns CPE name elements information as string.
        """

        pp = pprint.PrettyPrinter(indent=4, width=80)

        return "CPE %s => %s\n\n%s\n" % (self.VERSION,
                                         self.uri,
                                         pp.pformat(self.cpe_dict))
