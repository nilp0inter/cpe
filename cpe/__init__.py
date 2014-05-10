# -*- coding: utf-8 -*-

from .cpe import CPE

VERSION = (1, 1, 0)
PACKAGE_NAME = u'cpe'
DESCRIPTION = u'CPE: Common Platform Enumeration for Python'
AUTHORS = u", ".join((
    u'Roberto Abdelkader Martínez Pérez',
    u'Alejandro Galindo García',))
EMAILS = u", ".join((
    'robertomartinezp@gmail.com',
    'alejandro.galindo@i4s.com',
    'juandiego.gonzalez.contractor@bbva.com'))


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
