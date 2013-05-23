#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpe2_2.py
Author: Alejandro Galindo
Date: 23-04-2013
Description: Module for the treatment of identifiers of IT platforms
             (hardware, operating systems or applications of system)
             in accordance with version 2.2 of CPE
             (Common Platform Enumeration) specification.
"""


from cpe import CPE

import re


class CPE2_2(CPE):
    """
    Implementation of version 2.2 of CPE specification.

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
    - cpe:/{part}:{vendor}:{product}:{version}:{update}:{edition}:{language}

    - TEST: bad URI
    >>> str = 'baduri'
    >>> CPE2_2(str)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: validation of parts failed

    - TEST: URI with whitespaces
    >>> str = 'cpe con espacios'
    >>> CPE2_2(str)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: it must not have whitespaces

    - TEST: an empty CPE.
    >>> str = 'cpe:/'
    >>> CPE2_2(str) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an empty CPE with five parts
    >>> str = 'cpe:/::::'
    >>> CPE2_2(str) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an empty CPE with bad part name
    >>> str = 'cpe:/b::::'
    >>> CPE2_2(str)
    Traceback (most recent call last):
    ValueError: Input identifier is not a valid CPE name: Error to split CPE name parts

    - TEST: an CPE with too many components
    >>> str = 'cpe:/a:1:2:3:4:5:6:7'
    >>> CPE2_2(str)
    Traceback (most recent call last):
    ValueError: Input identifier is not a valid CPE name: Error to split CPE name parts

    - TEST: an application CPE
    >>> str = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
    >>> CPE2_2(str) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an operating system CPE
    >>> str = 'cpe:/o:microsoft:windows_xp:::pro'
    >>> CPE2_2(str) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an hardware CPE
    >>> str = 'cpe:/h:nvidia'
    >>> CPE2_2(str) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>

    - TEST: an CPE with special characters
    >>> str = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
    >>> CPE2_2(str) # doctest: +ELLIPSIS
    <__main__.CPE2_2 object at 0x...>
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Value of empty component
    EMPTY_COMP_VALUE = ""

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str='cpe:/'):
        """
        Checks that a CPE name defined with URI style is valid and,
        if so, stores the components in a dictionary.
        """

        CPE.__init__(self, cpe_str)
        CPE.version = CPE.VERSION_2_2
        self._validate()

    def __len__(self):
        """
        Returns the number of components of CPE name.

        - TEST: a CPE name without components
        >>> str = "cpe:/"
        >>> c = CPE2_2(str)
        >>> len(c)
        0

        - TEST: a CPE name with some full components
        >>> str = "cpe:/a:i4s:javas"
        >>> c = CPE2_2(str)
        >>> len(c)
        3

        - TEST: a CPE name with some empty components
        >>> str = "cpe:/a:i4s:::javas"
        >>> c = CPE2_2(str)
        >>> len(c)
        5

        - TEST: a CPE name with all components
        >>> str = "cpe:/a:acme:product:1.0:update2:-:en-us"
        >>> c = CPE2_2(str)
        >>> len(c)
        7
        """

        count = self.cpe_str.count(":")
        if count > 1:
            return count
        else:
            return 0

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE name as a string.

        - TEST: existing item
        >>> str = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(str)
        >>> c[2]
        '11.0'

        - TEST: existing empty item
        >>> str = 'cpe:/h:nvidia.buena_2~~pero_rara::sp2'
        >>> c = CPE2_2(str)
        >>> c[2]
        ''

        - TEST: not existing valid item
        >>> str = 'cpe:/h:nvidia.buena_2~~pero_rara::sp2'
        >>> c = CPE2_2(str)
        >>> c[6] == CPE2_2.EMPTY_COMP_VALUE
        True

        - TEST: not valid item
        >>> str = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(str)
        >>> c[11]
        Traceback (most recent call last):
        IndexError: 'Component index of CPE name out of range'
        """

        if i not in CPE.uri_ordered_part_dict.keys():
            msg = "Component index of CPE name out of range"
            raise IndexError(msg)

        comp_key = CPE.uri_ordered_part_dict[i]

        return self._cpe_dict[comp_key]

    def __eq__(self, cpe):
        """
        Return True if input CPE name is equal to self CPE name,
        otherwise False.

        - TEST: is application
        >>> str = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE2_2(str)
        >>> c == c
        True

        - TEST: is application
        >>> str = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE2_2(str)
        >>> str2 = 'cpe:/a:mozilla'
        >>> c2 = CPE2_2(str2)
        >>> c == c2
        False
        """

        eqPart = self.getPart() == cpe.getPart()
        eqVendor = self.getVendor() == cpe.getVendor()
        eqProduct = self.getProduct() == cpe.getProduct()
        eqVersion = self.getVersion() == cpe.getVersion()
        eqUpdate = self.getUpdate() == cpe.getUpdate()
        eqEdition = self.getEdition() == cpe.getEdition()
        eqLanguage = self.getLanguage() == cpe.getLanguage()

        return (eqPart and eqVendor and eqProduct and eqVersion and
                eqUpdate and eqEdition and eqLanguage)

    def _validate(self):
        """
        Checks if CPE name with URI style is valid.
        """

        # CPE name must not have whitespaces
        if (self.str.find(" ") != -1):
            msg = "Malformed CPE name: it must not have whitespaces"
            raise ValueError(msg)

        # Compilation of regular expression associated with components
        # of CPE name
        typesys = "?P<%s>(h|o|a)" % CPE.KEY_PART
        vendor = "?P<%s>[^:]+" % CPE.KEY_VENDOR
        product = "?P<%s>[^:]+" % CPE.KEY_PRODUCT
        version = "?P<%s>[^:]+" % CPE.KEY_VERSION
        update = "?P<%s>[^:]+" % CPE.KEY_UPDATE
        edition = "?P<%s>[^:]+" % CPE.KEY_EDITION
        language = "?P<%s>[^:]+" % CPE.KEY_LANGUAGE

        parts_pattern = "^cpe:/"
        parts_pattern += "(%s)?" % typesys
        parts_pattern += "(:(%s)?)?" % vendor
        parts_pattern += "(:(%s)?)?" % product
        parts_pattern += "(:(%s)?)?" % version
        parts_pattern += "(:(%s)?)?" % update
        parts_pattern += "(:(%s)?)?" % edition
        parts_pattern += "(:(%s)?)?$" % language
        parts_rxc = re.compile(parts_pattern)

        # Partitioning of CPE name
        parts_match = parts_rxc.match(self.str)

        # #####################################
        #  Validation of CPE name components  #
        # #####################################

        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        # Compilation of regular expression associated with value of CPE part
        part_value_pattern = "[\d\w\._\-~%]+"
        part_value_rxc = re.compile(part_value_pattern)

        for i, pk in enumerate(CPE.uri_part_keys):
            value = parts_match.group(pk)

            if (value is None):
                value = CPE2_2.EMPTY_COMP_VALUE
            else:
                if (part_value_rxc.match(value) is None):
                    msg = "Malformed CPE name: part value must have "
                    msg += "only alphanumeric and the following characters:"
                    msg += " '.', '_', '-', '~', '%'"

                    raise ValueError(msg)

            self._cpe_dict[pk] = value

        return self._cpe_dict

    def isHardware(self):
        """
        Returns True if CPE name corresponds to hardware elem.

        - TEST: is HW
        >>> str = 'cpe:/h:nvidia:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(str)
        >>> c.isHardware() == True
        True

        - TEST: is not HW
        >>> str = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE2_2(str)
        >>> c.isHardware() == False
        True

        - TEST: is not HW
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.isHardware() == False
        True
        """

        # Value of part type of CPE name
        type_value = self._cpe_dict[CPE.KEY_PART]

        isHW = type_value == CPE.VALUE_PART_HW
        isEmpty = type_value == ""

        return (isHW or isEmpty)

    def isOperatingSystem(self):
        """
        Returns True if CPE name corresponds to operating system elem.

        - TEST: is not OS
        >>> str = 'cpe:/h:nvidia:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(str)
        >>> c.isOperatingSystem() == False
        True

        - TEST: is OS
        >>> str = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE2_2(str)
        >>> c.isOperatingSystem() == True
        True

        - TEST: is not OS
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.isOperatingSystem() == False
        True
        """

        # Value of part type of CPE name
        type_value = self._cpe_dict[CPE.KEY_PART]

        isOS = type_value == CPE.VALUE_PART_OS
        isEmpty = type_value == ""

        return (isOS or isEmpty)

    def isApplication(self):
        """
        Returns True if CPE name corresponds to application elem.

        - TEST: is not application
        >>> str = 'cpe:/h:nvidia:nvidia.buena_2~~pero_rara:11.0'
        >>> c = CPE2_2(str)
        >>> c.isApplication() == False
        True

        - TEST: is not application
        >>> str = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE2_2(str)
        >>> c.isApplication() == False
        True

        - TEST: is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.isApplication() == True
        True
        """

        # Value of part type of CPE name
        type_value = self._cpe_dict[CPE.KEY_PART]

        isApp = type_value == CPE.VALUE_PART_APP
        isEmpty = (type_value == "") or (type_value is None)

        return (isApp or isEmpty)

    def getPart(self):
        """
        Returns the part component of CPE name.

        - TEST: is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.getPart()
        'a'

        - TEST: is operating system
        >>> str = 'cpe:/o:microsoft:xp'
        >>> c = CPE2_2(str)
        >>> c.getPart()
        'o'

        - TEST: is hardware
        >>> str = 'cpe:/h:cisco'
        >>> c = CPE2_2(str)
        >>> c.getPart()
        'h'
        """

        return self._cpe_dict[CPE.KEY_PART]

    def getVendor(self):
        """
        Returns the vendor name of CPE name.

        - TEST: is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.getVendor()
        'microsoft'
        """

        return self._cpe_dict[CPE.KEY_VENDOR]

    def getProduct(self):
        """
        Returns the product name of CPE name.

        - TEST: is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.getProduct()
        'ie'
        """

        return self._cpe_dict[CPE.KEY_PRODUCT]

    def getVersion(self):
        """
        Returns the version of product of CPE name.

        - TEST: is application
        >>> str = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_2(str)
        >>> c.getVersion()
        '10'
        """

        return self._cpe_dict[CPE.KEY_VERSION]

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE name.

        - TEST: is operating system
        >>> str = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE2_2(str)
        >>> c.getUpdate()
        'sp2'
        """

        return self._cpe_dict[CPE.KEY_UPDATE]

    def getEdition(self):
        """
        Returns the edition of product of CPE name.

        - TEST: is operating system
        >>> str = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE2_2(str)
        >>> c.getEdition()
        'pro'
        """

        return self._cpe_dict[CPE.KEY_EDITION]

    def getLanguage(self):
        """
        Returns the internationalization information of CPE name.

        - TEST: is application
        >>> str = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE2_2(str)
        >>> c.getLanguage()
        'es-es'
        """

        return self._cpe_dict[CPE.KEY_LANGUAGE]


if __name__ == "__main__":

    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
