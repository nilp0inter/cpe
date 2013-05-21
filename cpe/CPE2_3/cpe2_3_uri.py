#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe2_3_uri.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Module for the treatment of identifiers in accordance with
             binding style URI of version 2.3 of specification CPE
             (Common Platform Enumeration).
'''

from cpe2_3_base import CPE2_3_BASE

import re


class CPE2_3_URI(CPE2_3_BASE):
    """
    Implementation of binding style uri of CPE 2.3 specification.

    - TEST: bad URI
    >>> uri = 'baduri'
    >>> CPE2_3_URI(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_uri.py", line 131, in __init__
        self._validate_uri()
      File "cpe/CPE2_3/cpe2_3_uri.py", line 202, in _validate_uri
        raise TypeError(msg)
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: URI with whitespaces
    >>> uri = 'cpe con espacios'
    >>> CPE2_3_URI(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_uri.py", line 131, in __init__
        self._validate_uri()
      File "cpe/CPE2_3/cpe2_3_uri.py", line 170, in _validate_uri
        raise TypeError(msg)
    TypeError: Malformed CPE, it must not have whitespaces

    - TEST: an empty CPE.
    >>> uri = 'cpe:/'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_3_URI object at 0x...>

    - TEST: an empty CPE with five parts
    >>> uri = 'cpe:/::::'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_3_URI object at 0x...>

    - TEST: an empty CPE with bad part name
    >>> uri = 'cpe:/b::::'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_uri.py", line 131, in __init__
        1: CPE2_3_BASE.KEY_VENDOR,
      File "cpe/CPE2_3/cpe2_3_uri.py", line 202, in _validate_uri
        CPE2_3_BASE.KEY_VERSION,
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: an CPE with too many components
    >>> uri = 'cpe:/a:1:2:3:4:5:6:7'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_uri.py", line 131, in __init__
        1: CPE2_3_BASE.KEY_VENDOR,
      File "cpe/CPE2_3/cpe2_3_uri.py", line 202, in _validate_uri
        CPE2_3_BASE.KEY_VERSION,
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: an application CPE
    >>> uri = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_3_URI object at 0x...>

    - TEST: an operating system CPE
    >>> uri = 'cpe:/o:microsoft:windows_xp:::pro'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_3_URI object at 0x...>

    - TEST: an hardware CPE
    >>> uri = 'cpe:/h:nvidia'
    >>> CPE2_3_URI(uri) # doctest: +ELLIPSIS
    <__main__.CPE2_3_URI object at 0x...>

    - TEST: an CPE with special characters
    >>> uri = 'cpe:/h:nvidia.buena_2~~pero_rara:11.0'
    >>> CPE2_3_URI(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe2_3_uri.py", line 120, in __init__
        self._validate_uri()
      File "cpe2_3_uri.py", line 240, in _validate_uri
        raise TypeError(msg)
    TypeError: Malformed CPE, vendor value is invalid
    """

    # Separator of edition part components in CPE uri
    PACKED_EDITION_SEPARATOR = "~"

    def __init__(self, cpe_str):
        """
        Checks that input CPE name string is valid according to binding
        style URI and, if so, stores the component in a dictionary.
        """

        CPE2_3_BASE.__init__(self, cpe_str)

        # Store CPE identifier:
        #     CPE names are case-insensitive.
        #     To reduce potential for confusion,
        #     all CPE Names should be written in lowercase
        self.uri = cpe_str.lower()

        self._validate_uri()

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
        typesys = "?P<%s>(h|o|a)" % CPE2_3_BASE.KEY_PART
        vendor = "?P<%s>[^:]+" % CPE2_3_BASE.KEY_VENDOR
        product = "?P<%s>[^:]+" % CPE2_3_BASE.KEY_PRODUCT
        version = "?P<%s>[^:]+" % CPE2_3_BASE.KEY_VERSION
        update = "?P<%s>[^:]+" % CPE2_3_BASE.KEY_UPDATE
        edition = "?P<%s>[^:]+" % CPE2_3_BASE.KEY_EDITION
        language = "?P<%s>[^:]+" % CPE2_3_BASE.KEY_LANGUAGE

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

        # Compilation of regular expression associated with value of CPE part
        ALPHA = "a-zA-Z"
        DIGIT = "\d"

        region = "([%s]{2}|[%s]{3})" % (ALPHA, DIGIT)
        language = "[%s]{2,3}" % ALPHA
        LANGTAG = "%s(\-%s)?" % (language, region)

        #pct_encoded = "\!\"\#\$\%\&\'\(\)"
        #pct_encoded += "\*\+\,\/"
        #pct_encoded += "\:\;\<\=\>\?"
        #pct_encoded += "\@\[\\\]\^"
        #pct_encoded += "\`\{\|\}\~"
        pct_encoded = "%21|%22|%23|%24|%25|%26|%27|%28|%29"
        pct_encoded += "|%2a|%2b|%2c|%2f"
        pct_encoded += "|%3a|%3b|%3c|%3d|%3e|%3f"
        pct_encoded += "|%40|%5b|%5c|%5d|%5e"
        pct_encoded += "|%60|%7b|%7c|%7d|%7e"
        unreserved = "[%s%s\-\._]" % (ALPHA, DIGIT)
        spec_chrs = "(\?+|\*)"
        str_w_special = "(%s?(%s|%s)+%s?)" % (spec_chrs, unreserved,
                                              pct_encoded, spec_chrs)
        str_wo_special = "(%s|%s)*" % (unreserved, pct_encoded)

        string = "(%s|%s)" % (str_wo_special, str_w_special)
        value_string_pattern = "^%s$" % string
        packed = "(%s%s){5}" % (CPE2_3_URI.PACKED_EDITION_SEPARATOR, string)

        value_edition_pattern = "^(%s|%s)$" % (string, packed)
        value_lang_pattern = "^%s?$" % LANGTAG

        part_value_rxc = re.compile(value_string_pattern)
        edition_value_rxc = re.compile(value_edition_pattern)
        lang_value_rxc = re.compile(value_lang_pattern)

        # Count of parts in CPE ID
        count = self.__len__()

        for i, pk in enumerate(CPE2_3_BASE.uri_part_keys):
            value = parts_match.group(pk)

            if (value is None):
                if (i < count):
                    value = ""
            else:
                if pk == CPE2_3_BASE.KEY_EDITION:
                    if (edition_value_rxc.match(value) is None):
                        msg = "Malformed CPE, edition value is invalid"
                        raise TypeError(msg)

                elif pk == CPE2_3_BASE.KEY_LANGUAGE:
                    if (lang_value_rxc.match(value) is None):
                        msg = "Malformed CPE, language value is invalid"
                        raise TypeError(msg)

                else:
                    if (part_value_rxc.match(value) is None):
                        msg = "Malformed CPE, %s value is invalid " % pk
                        raise TypeError(msg)

            self.cpe_dict[pk] = value

        return self.cpe_dict

    def __len__(self):
        """
        Returns the number of parts of CPE ID.

        - TEST: a CPE name without components
        >>> uri = "cpe:/"
        >>> c = CPE2_3_URI(uri)
        >>> len(c)
        0

        - TEST: a CPE name with some elements
        >>> uri = "cpe:/a:i4s:javas"
        >>> c = CPE2_3_URI(uri)
        >>> len(c)
        3

        - TEST: a CPE name with some elements
        >>> uri = "cpe:/a:i4s:::javas"
        >>> c = CPE2_3_URI(uri)
        >>> len(c)
        5

        - TEST: a component with all subcomponents
        >>> uri = "cpe:/a:acme:product:1.0:update2:-:en-us"
        >>> c = CPE2_3_URI(uri)
        >>> len(c)
        7
        """

        count = self.uri.count(":")
        if count == 1:
            return 0
        else:
            return count

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE ID as a string.

        - TEST: existing item
        >>> uri = 'cpe:/h:nvidia.buena_2pero_rara:11.0'
        >>> c = CPE2_3_URI(uri)
        >>> c[2] == '11.0'
        True

        - TEST: existing empty item
        >>> uri = 'cpe:/h:nvidia.buena_2pero_rara::sp2'
        >>> c = CPE2_3_URI(uri)
        >>> c[2] == ""
        True

        - TEST: not existing valid item
        >>> uri = 'cpe:/h:nvidia.buena_2pero_rara::sp2'
        >>> c = CPE2_3_URI(uri)
        >>> c[5] == None
        True

        - TEST: not valid item
        >>> uri = 'cpe:/h:nvidia.buena_2pero_rara:11.0'
        >>> c = CPE2_3_URI(uri)
        >>> c[11]
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "cpe/CPE2_3/cpe2_3_uri.py", line 283, in __getitem__
            raise KeyError(msg)
        KeyError: 'index not exists. Possible values: 0-6'
        """

        keys = CPE2_3_BASE.uri_order_parts_dict.keys()
        if i not in keys:
            max_index = len(keys) - 1
            msg = "index not exists. Possible values: 0-%s" % max_index
            raise KeyError(msg)

        part_key = CPE2_3_BASE.uri_order_parts_dict[i]

        return self.cpe_dict[part_key]

    def isHardware(self):
        """
        Returns True if CPE ID corresponds to hardware elem.

        - TEST: is HW
        >>> uri = 'cpe:/h:nvidia:nvidia.buena_2pero_rara:11.0'
        >>> c = CPE2_3_URI(uri)
        >>> c.isHardware() == True
        True

        - TEST: is not HW
        >>> uri = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE2_3_URI(uri)
        >>> c.isHardware() == False
        True

        - TEST: is not HW
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.isHardware() == False
        True
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_3_BASE.KEY_PART]

        isHW = type_value == CPE2_3_BASE.VALUE_PART_HW
        isEmpty = type_value == ""

        return (isHW or isEmpty)

    def isOperatingSystem(self):
        """
        Returns True if CPE ID corresponds to operating system elem.

        - TEST: is not OS
        >>> uri = 'cpe:/h:nvidia:nvidia.buena_2pero_rara:11.0'
        >>> c = CPE2_3_URI(uri)
        >>> c.isOperatingSystem() == False
        True

        - TEST: is OS
        >>> uri = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE2_3_URI(uri)
        >>> c.isOperatingSystem() == True
        True

        - TEST: is not OS
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.isOperatingSystem() == False
        True
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_3_BASE.KEY_PART]

        isOS = type_value == CPE2_3_BASE.VALUE_PART_OS
        isEmpty = type_value == ""

        return (isOS or isEmpty)

    def isApplication(self):
        """
        Returns True if CPE ID corresponds to application elem.

        - TEST: is not application
        >>> uri = 'cpe:/h:nvidia:nvidia.buena_2pero_rara:11.0'
        >>> c = CPE2_3_URI(uri)
        >>> c.isApplication() == False
        True

        - TEST: is not application
        >>> uri = 'cpe:/o:microsoft:windows:xp'
        >>> c = CPE2_3_URI(uri)
        >>> c.isApplication() == False
        True

        - TEST: is application
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.isApplication() == True
        True
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_3_BASE.KEY_PART]

        isApp = type_value == CPE2_3_BASE.VALUE_PART_APP
        isEmpty = (type_value == "") or (type_value is None)

        return (isApp or isEmpty)

    def getType(self):
        """
        Returns the part type of CPE ID.

        - TEST: is application
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.getType()
        'a'

        - TEST: is operating system
        >>> uri = 'cpe:/o:microsoft:xp'
        >>> c = CPE2_3_URI(uri)
        >>> c.getType()
        'o'

        - TEST: is hardware
        >>> uri = 'cpe:/h:cisco'
        >>> c = CPE2_3_URI(uri)
        >>> c.getType()
        'h'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_PART]

    def getVendor(self):
        """
        Returns the vendor name of CPE ID.

        - TEST: is application
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.getVendor()
        'microsoft'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_VENDOR]

    def getProduct(self):
        """
        Returns the product name of CPE ID.

        - TEST: is application
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.getProduct()
        'ie'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_PRODUCT]

    def getVersion(self):
        """
        Returns the version of product of CPE ID.

        - TEST: is application
        >>> uri = 'cpe:/a:microsoft:ie:10'
        >>> c = CPE2_3_URI(uri)
        >>> c.getVersion()
        '10'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_VERSION]

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE ID.

        - TEST: is operating system
        >>> uri = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE2_3_URI(uri)
        >>> c.getUpdate()
        'sp2'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_UPDATE]

    def getEdition(self):
        """
        Returns the edition of product of CPE ID.

        - TEST: is operating system
        >>> uri = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE2_3_URI(uri)
        >>> c.getEdition()
        'pro'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_EDITION]

    def isEditionPacked(self):
        """
        Returns TRUE if edition part contains several elements packed.

        - TEST: packed
        >>> uri = 'cpe:/o:microsoft:windows_xp::sp2:~1~2~3~4~5'
        >>> c = CPE2_3_URI(uri)
        >>> c.isEditionPacked()
        True

        - TEST: not packed
        >>> uri = 'cpe:/o:microsoft:windows_xp::sp2:pro'
        >>> c = CPE2_3_URI(uri)
        >>> c.isEditionPacked()
        False
        """

        return (self.getEdition().find(CPE2_3_URI.PACKED_EDITION_SEPARATOR) > -1)

    def getEditionElements(self):
        """
        Return a list with elements packed in edition part.
        If there are not elements packed
        it returns a list with a element.
        """

        return self.getEdition().split(CPE2_3_URI.PACKED_EDITION_SEPARATOR)

    def getLanguage(self):
        """
        Returns the internationalization information of CPE ID.

        - TEST: is application
        >>> uri = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE2_3_URI(uri)
        >>> c.getLanguage()
        'es-es'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_LANGUAGE]

    def __unicode__(self):
        """
        Print CPE URI as string.
        """

        return self.uri

    def __eq__(self, cpe):
        """
        Return True if "cpe" is equal to self object.

        - TEST: equals
        >>> uri = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE2_3_URI(uri)
        >>> c == c
        True

        - TEST: not equals
        >>> uri = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        >>> c = CPE2_3_URI(uri)
        >>> uri2 = 'cpe:/a:mozilla'
        >>> c2 = CPE2_3_URI(uri2)
        >>> c == c2
        False
        """

        eqPart = self.cpe_dict[CPE2_3_BASE.KEY_PART] == cpe.getType()
        eqVendor = self.cpe_dict[CPE2_3_BASE.KEY_VENDOR] == cpe.getVendor()
        eqProduct = self.cpe_dict[CPE2_3_BASE.KEY_PRODUCT] == cpe.getProduct()
        eqVersion = self.cpe_dict[CPE2_3_BASE.KEY_VERSION] == cpe.getVersion()
        eqUpdate = self.cpe_dict[CPE2_3_BASE.KEY_UPDATE] == cpe.getUpdate()
        eqEdition = self.cpe_dict[CPE2_3_BASE.KEY_EDITION] == cpe.getEdition()
        eqLanguage = self.cpe_dict[CPE2_3_BASE.KEY_LANGUAGE] == cpe.getLanguage()

        return (eqPart and eqVendor and eqProduct and eqVersion and
                eqUpdate and eqEdition and eqLanguage)


if __name__ == "__main__":
    ##uri = 'cpe:/'
    ##uri = 'cpe:/::::::'
    ##uri = 'cpe:/o:microsoft:windows_xp:::pro'
    ##uri = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
    ##uri = 'cpe:/a:acme:product:1.0:update2:pro:en-usss'
    ##uri = 'cpe:/a:acme:product:1.0:update2:pro:en-123'
    ##uri = 'cpe:/a:acme:product:1.0:update2:pro:e-us'
    ##uri = 'cpe:/a:acme:product:1.0:update2:pro:esss-us'
    ##uri = 'cpe:/a:acme:product:1.0:update2:~~~un~dos:es-ES'
    ##uri = 'cpe:/a:acme:product:1.0:update2:~~~un~dos~:es-ES'
    ##uri = 'cpe:/a:acme:product:1.%02:update2:~~~un~dos~:es-ES'
    #uri = 'cpe:/a:acme:product:1.%250:update2:~~~un~dos~:es-ES'
    ##uri = 'cpe:/a:acme:product:1.%80:update2:~~~un~dos~:es-ES'
    ##uri = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'

    #ce = CPE2_3_URI(uri)
    #print("")
    #print(ce)
    #print("Elements: %s") % len(ce)
    #print("")
    #for i in range(0, 7):
    #    print("Element %s: %s") % (i, ce[i])
    #print("")
    #print("IS HARDWARE: %s") % ce.isHardware()
    #print("IS OS: %s") % ce.isOperatingSystem()
    #print("IS APPLICATION: %s") % ce.isApplication()
    #print("")
    #print("VENDOR: %s") % ce.getVendor()
    #print("PRODUCT: %s") % ce.getProduct()
    #print("VERSION: %s") % ce.getVersion()
    #print("UPDATE: %s") % ce.getUpdate()
    #print("EDITION: %s") % ce.getEdition()
    #print("LANGUAGE: %s") % ce.getLanguage()
    #print("")

    import doctest
    doctest.testmod()
