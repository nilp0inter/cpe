#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe2_2.py
Author: Alejandro Galindo
Date: 23-04-2013
Description: Module for the treatment of identifiers in accordance with
             version 2.2 of specification CPE (Common Platform Enumeration).
'''


from cpe.cpebase import CPEBASE

import re


class CPE2_2(CPEBASE):
    """
    Implementation of CPE 2.2 specification.

    - TEST: bad URI
    >>> uri = 'baduri'
    >>> CPE2_2(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_2/cpe2_2.py", line 131, in __init__
        self._validate_uri()
      File "cpe/CPE2_2/cpe2_2.py", line 202, in _validate_uri
        raise TypeError(msg)
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: URI with whitespaces
    >>> uri = 'cpe con espacios'
    >>> CPE2_2(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_2/cpe2_2.py", line 131, in __init__
        self._validate_uri()
      File "cpe/CPE2_2/cpe2_2.py", line 170, in _validate_uri
        raise TypeError(msg)
    TypeError: Malformed CPE, it must not have whitespaces

    - TEST: an empty CPE.
    >>> uri = 'cpe:/'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an empty CPE with five parts
    >>> uri = 'cpe:/::::'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an empty CPE with bad part name
    >>> uri = 'cpe:/b::::'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_2/cpe2_2.py", line 131, in __init__
        1: CPE2_2.KEY_VENDOR,
      File "cpe/CPE2_2/cpe2_2.py", line 202, in _validate_uri
        CPE2_2.KEY_VERSION,
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: an CPE with too many components
    >>> uri = 'cpe:/a:1:2:3:4:5:6:7'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_2/cpe2_2.py", line 131, in __init__
        1: CPE2_2.KEY_VENDOR,
      File "cpe/CPE2_2/cpe2_2.py", line 202, in _validate_uri
        CPE2_2.KEY_VERSION,
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: an application CPE
    >>> uri = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an operating system CPE
    >>> uri = 'cpe:/o:microsoft:windows_xp:::pro'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an hardware CPE
    >>> uri = 'cpe:/h:nvidia'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an CPE with special characters
    >>> uri = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
    >>> CPE2_2(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>
    """

    # CPE version
    VERSION = '2.2'

    # Constants associated with dictionary keys that
    # store CPE name elements
    KEY_TYPE = "type"
    KEY_VENDOR = "vendor"
    KEY_PRODUCT = "product"
    KEY_VERSION = "version"
    KEY_UPDATE = "update"
    KEY_EDITION = "edition"
    KEY_LANGUAGE = "language"

    KEY_TYPE_HW = "h"
    KEY_TYPE_OS = "o"
    KEY_TYPE_APP = "a"

    def __init__(self, cpe_uri):
        """
        Checks that a CPE name defined with URI style is valid and,
        if so, stores the components in a dictionary.
        """

        CPEBASE.__init__(self)

        # Store CPE identifier URI:
        #     CPE names are case-insensitive.
        #     To reduce potential for confusion,
        #     all CPE Names should be written in lowercase
        self.uri = cpe_uri.lower()

        self._validate_uri()

        # Mapping between order of parts and its value
        self.order_parts_dict = {
            0: CPE2_2.KEY_TYPE,
            1: CPE2_2.KEY_VENDOR,
            2: CPE2_2.KEY_PRODUCT,
            3: CPE2_2.KEY_VERSION,
            4: CPE2_2.KEY_UPDATE,
            5: CPE2_2.KEY_EDITION,
            6: CPE2_2.KEY_LANGUAGE
        }

    def _validate_uri(self):
        """
        Checks CPE name with URI style is valid.

        A CPE Name is a percent-encoded URI with each name
        starting with the prefix (the URI scheme name) 'cpe:'.

        Each platform can be broken down into many distinct parts.
        A CPE Name specifies a single part and is used to identify
        any platform that matches the description of that part.
        The distinct parts are:

        - Hardware part: the physical platform supporting the IT system.
        - Operating system part: the operating system controls and manages the
          IT hardware.
        - Application part: software systems, services, servers, and packages
          installed on the system.

        CPE name syntax:
        cpe:/ {part} : {vendor} : {product} : {version} :
            {update} : {edition} : {language}
        """

        # CPE ID must not have whitespaces
        if (self.uri.find(" ") != -1):
            msg = "Malformed CPE, it must not have whitespaces"
            raise TypeError(msg)

        # #####################
        #  CHECK CPE ID PARTS
        # #####################

        # Compilation of regular expression associated with parts of CPE ID
        typesys = "?P<%s>(h|o|a)" % CPE2_2.KEY_TYPE
        vendor = "?P<%s>[^:]+" % CPE2_2.KEY_VENDOR
        product = "?P<%s>[^:]+" % CPE2_2.KEY_PRODUCT
        version = "?P<%s>[^:]+" % CPE2_2.KEY_VERSION
        update = "?P<%s>[^:]+" % CPE2_2.KEY_UPDATE
        edition = "?P<%s>[^:]+" % CPE2_2.KEY_EDITION
        language = "?P<%s>[^:]+" % CPE2_2.KEY_LANGUAGE

        parts_pattern = "^cpe:/"
        parts_pattern += "(%s)?" % typesys
        parts_pattern += "(:(%s)?)?" % vendor
        parts_pattern += "(:(%s)?)?" % product
        parts_pattern += "(:(%s)?)?" % version
        parts_pattern += "(:(%s)?)?" % update
        parts_pattern += "(:(%s)?)?" % edition
        parts_pattern += "(:(%s)?)?$" % language
        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE ID
        parts_match = parts_rxc.match(self.uri)

        # Validation of CPE ID parts
        if (parts_match is None):
            msg = "Input identifier is not a valid CPE ID: "
            msg += "Error to split CPE ID parts"
            raise TypeError(msg)

        parts_key = [CPE2_2.KEY_TYPE,
                     CPE2_2.KEY_VENDOR,
                     CPE2_2.KEY_PRODUCT,
                     CPE2_2.KEY_VERSION,
                     CPE2_2.KEY_UPDATE,
                     CPE2_2.KEY_EDITION,
                     CPE2_2.KEY_LANGUAGE]

        # Compilation of regular expression associated with value of CPE part
        part_value_pattern = "[\d\w\._\-~%]+"
        part_value_rxc = re.compile(part_value_pattern, re.IGNORECASE)

        for pk in parts_key:
            value = parts_match.group(pk)

            if (value is not None):
                if (part_value_rxc.match(value) is None):
                    msg = "Malformed CPE, part value must have "
                    msg += "only the following characters:"
                    msg += " alfanumeric, '.', '_', '-', '~', '%'"

                    raise TypeError(msg)
            else:
                value = ""

            self.cpe_dict[pk] = value

        return self.cpe_dict

    def __len__(self):
        """
        Returns the number of parts of CPE ID.

        - TEST: a CPE name without components
        >>> uri = "cpe:/"
        >>> c = CPE2_2(uri)
        >>> len(c)
        7

        - TEST: a CPE name with some elements
        >>> uri = "cpe:/a:i4s:javas"
        >>> c = CPE2_2(uri)
        >>> len(c)
        7

        - TEST: a component with all subcomponents
        >>> uri = "cpe:/a:acme:product:1.0:update2:-:en-us"
        >>> c = CPE2_2(uri)
        >>> len(c)
        7
        """

        return len(self.cpe_dict.keys())

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE ID as a string.

        - TEST: existing item
        >>> uri = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(uri)
        >>> c[2] == '11.0'
        True

        - TEST: existing empty item
        >>> uri = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0::'
        >>> c = CPE2_2(uri)
        >>> c[4] == ""
        True

        - TEST: nonexistent item
        >>> uri = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(uri)
        >>> c[11]
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "cpe/CPE2_2/cpe2_2.py", line 283, in __getitem__
            raise KeyError(msg)
        KeyError: 'index not exists. Possible values: 0-6'
        """

        if i not in self.order_parts_dict.keys():
            max_index = len(self.order_parts_dict.keys()) - 1
            msg = "index not exists. Possible values: 0-%s" % max_index
            raise KeyError(msg)

        part_key = self.order_parts_dict[i]

        return self.cpe_dict[part_key]

    def isHardware(self):
        """
        Returns True if CPE ID corresponds to hardware elem.
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_2.KEY_TYPE]

        isHW = type_value == CPE2_2.KEY_TYPE_HW
        isEmpty = type_value == ""

        return (isHW or isEmpty)

    def isOperatingSystem(self):
        """
        Returns True if CPE ID corresponds to operating system elem.
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_2.KEY_TYPE]

        isOS = type_value == CPE2_2.KEY_TYPE_OS
        isEmpty = type_value == ""

        return (isOS or isEmpty)

    def isApplication(self):
        """
        Returns True if CPE ID corresponds to application elem.
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_2.KEY_TYPE]

        isApp = type_value == CPE2_2.KEY_TYPE_APP
        isEmpty = type_value == ""

        return (isApp or isEmpty)

    def getVendor(self):
        """
        Returns the vendor name of CPE ID.
        """

        return self.cpe_dict[CPE2_2.KEY_VENDOR]

    def getProduct(self):
        """
        Returns the product name of CPE ID.
        """

        return self.cpe_dict[CPE2_2.KEY_PRODUCT]

    def getVersion(self):
        """
        Returns the version of product of CPE ID.
        """

        return self.cpe_dict[CPE2_2.KEY_VERSION]

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE ID.
        """

        return self.cpe_dict[CPE2_2.KEY_UPDATE]

    def getEdition(self):
        """
        Returns the edition of product of CPE ID.
        """

        return self.cpe_dict[CPE2_2.KEY_EDITION]

    def getLanguage(self):
        """
        Returns the internationalization information of CPE ID.
        """

        return self.cpe_dict[CPE2_2.KEY_LANGUAGE]

    def __unicode__(self):
        """
        Print CPE URI as string.
        """

        return self.uri

if __name__ == "__main__":
#    #uri = 'cpe:/'
#    uri = 'cpe:/::::::'
#    #uri = 'cpe:/o:microsoft:windows_xp:::pro'
#    #uri = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
#    #uri = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
#
#    ce = CPE2_2(uri)
#    print("")
#    print(ce)
#    print("Elements: %s") % len(ce)
#    print("")
#    for i in range(len(ce)):
#        print("Element %s: %s") % (i, ce[i])
#    print("")
#    print("IS HARDWARE: %s") % ce.isHardware()
#    print("IS OS: %s") % ce.isOperatingSystem()
#    print("IS APPLICATION: %s") % ce.isApplication()
#    print("")
#    print("VENDOR: %s") % ce.getVendor()
#    print("PRODUCT: %s") % ce.getProduct()
#    print("VERSION: %s") % ce.getVersion()
#    print("UPDATE: %s") % ce.getUpdate()
#    print("EDITION: %s") % ce.getEdition()
#    print("LANGUAGE: %s") % ce.getLanguage()
#    print("")

    import doctest
    doctest.testmod()
