# -*- coding: utf-8 -*-

from .cpe import CPE

VERSION = (1, 0, 5)
PACKAGE_NAME = u'cpe'
DESCRIPTION = u'Implementation of versions 1.1, 2.2 and 2.3 of CPE specification.'
AUTHORS = u"{0}, {1}".format(
    u'Alejandro Galindo García',
    u'Roberto Abdelkader Martínez Pérez')
EMAILS = "{0}, {1}".format(
    'alejandro.galindo@i4s.com',
    'juandiego.gonzalez.contractor@bbva.com')


def get_version():
    """
    Returns the package version.

    :returns: The package version
    :rtype: string
    """

    return u"{x}.{y}.{z}".format(x=VERSION[0], y=VERSION[1], z=VERSION[2])


def get_release():
    """
    Returns the package release.

    :returns: The package release
    :rtype: string
    """

    return u"{x}.{y}".format(x=VERSION[0], y=VERSION[1])
