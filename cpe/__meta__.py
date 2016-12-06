# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import namedtuple

# Developer definition.
# AFAIK: A human being capable of turn pizza & coke into code.
Developer = namedtuple("Developer", ("name", "email"))


__all__ = [
    "__packagename__",
    "__version__",
    "__summary__",
    "__url__",
    "__author__",
    "__email__",
    "__license__"
]

DEVELOPERS = {
    "nilp0inter": Developer("Roberto Abdelkader Martínez Pérez",
                            "robertomartinezp@gmail.com"),
    "galindale": Developer("Alejandro Galindo García",
                           "alejandro.galindo@i4s.com"),
}

__packagename__ = "cpe"
__version__ = "1.2.1"
__summary__ = "CPE: Common Platform Enumeration for Python"
__keywords__ = "cpe identification naming matching standard specification mitre nist"
__url__ = "https://github.com/nilp0inter/cpe"
__author__ = ", ".join([
    DEVELOPERS["nilp0inter"].name,
    DEVELOPERS["galindale"].name])
__email__ = ", ".join([
    DEVELOPERS["nilp0inter"].email,
    DEVELOPERS["galindale"].email])
__maintainer__ = DEVELOPERS["nilp0inter"].name
__maintainer_email__ = DEVELOPERS["nilp0inter"].email
__license__ = "LGPLv3"
