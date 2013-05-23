#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpe2_3_fs.py
Author: Alejandro Galindo
Date: 20-05-2013
Description: Module for the treatment of identifiers in accordance with
             binding style formatted string of version 2.3 of CPE
             (Common Platform Enumeration) specification.
"""


from cpe2_3 import CPE2_3

import re


class CPE2_3_FS(CPE2_3):
    """
    Implementation of binding style formatted string of version 2.3
    of CPE specification.

    Each name starts with the prefix 'cpe:2.3:'.

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

    cpe:2.3: part : vendor : product : version : update : edition :
    language : sw_edition : target_sw : target_hw : other

    - TEST: bad WFN
    >>> fs = 'baduri'
    >>> CPE2_3_FS(fs)
    Traceback (most recent call last):
    ValueError: Input identifier is not a valid CPE name: Error to split CPE name parts

    - TEST: an empty CPE.
    >>> fs = 'cpe:2.3:*:*:*:*:*:*:*:*:*:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: an operating system CPE
    >>> fs = 'cpe:2.3:o:acme:producto:1.0:update2:pro:en-us:*:*:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: an application CPE
    >>> fs = 'cpe:2.3:a:hp:insight_diagnostics:7.4.0.1570:-:online:-:windows_2003:x64:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: an application CPE
    >>> fs = 'cpe:2.3:a:hp:insight_diagnostics:8.*:es?:*:-:-:x32:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: an CPE with special characters
    >>> fs = 'cpe:2.3:a:hp:insight_diagnostics:8.*:es?:*:-:-:x32\~:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: An unquoted question mark MAY be used at the beginning
    and/or the end of an attribute-value string
    >>> fs = 'cpe:2.3:a:hp:insight_diagnostics:*8.*:?es?:*:-:-:x32\~:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: A contiguous sequence of unquoted question marks MAY appear at the
    beginning and/or the end of an attribute-value string
    >>> fs = 'cpe:2.3:a:???hp**:insight_diagnostics:8.*:es:*:-:-:x32\~:*:*'
    >>> CPE2_3_FS(fs)
    Traceback (most recent call last):
    ValueError: Malformed CPE, vendor value is invalid

    - TEST: A contiguous sequence of unquoted question marks MAY appear at the
    beginning and/or the end of an attribute-value string
    >>> fs = 'cpe:2.3:a:???hp*:insight_diagnostics:8.*:es:*:-:-:x32\~:*:*'
    >>> CPE2_3_FS(fs) # doctest: +ELLIPSIS
    <__main__.CPE2_3_FS object at 0x...>

    - TEST: Unquoted question marks and asterisks MAY appear
    in the same attribute-value string
    >>> fs = 'cpe:2.3:a:hp:insight_?diagnostics:8.*:es:*:-:-:x32\~:*:*'
    >>> CPE2_3_FS(fs)
    Traceback (most recent call last):
    ValueError: Malformed CPE, product value is invalid

    - TEST: An unquoted question mark SHALL NOT be used
    in any other place in an attribute-value string
    >>> uri = 'cpe:2.3:h:?*nvidia:*:*:*:*:*:*:*:*:*'
    >>> CPE2_3_FS(uri)
    Traceback (most recent call last):
    ValueError: Malformed CPE, vendor value is invalid
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Var associated with regular expressions
    _LOGICAL = "\*|\-"

    # Logical values in integer format
    _VALUE_INT_NULL = 0
    _VALUE_INT_ANY = 1
    _VALUE_INT_NA = 2

    # Logical values in string format
    VALUE_NULL = ""
    VALUE_ANY_VALUE = "*"
    VALUE_NOT_APPLICABLE = "-"

    # Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = "*"
    # Constant associated with wildcard to indicate a character
    WILDCARD_ONE = "?"

    ###############
    #  VARIABLES  #
    ###############

    _int_to_string_logical_dict = {
        _VALUE_INT_NULL: VALUE_NULL,
        _VALUE_INT_ANY: VALUE_ANY_VALUE,
        _VALUE_INT_NA: VALUE_NOT_APPLICABLE
    }

    _string_to_int_logical_dict = {
        VALUE_NULL: _VALUE_INT_NULL,
        VALUE_ANY_VALUE: _VALUE_INT_ANY,
        VALUE_NOT_APPLICABLE: _VALUE_INT_NA
    }

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _is_valid_fs_value(cls, str_value):
        """
        Return True if the input value of CPE attribute distinct of
        "language" is valid, and otherwise False.

        - TEST: invalid value
        >>> val = 'insight_?diagnostics'
        >>> CPE2_3_FS._is_valid_fs_value(val)
        False

        >>> val = '8\.*'
        >>> CPE2_3_FS._is_valid_fs_value(val)
        False

        >>> val = '?es?'
        >>> CPE2_3_FS._is_valid_fs_value(val)
        True
        """

        # Compilation of regular expression associated with value of CPE part
        quest = "\%s" % CPE2_3_FS.WILDCARD_ONE
        asterisk = "\%s" % CPE2_3_FS.WILDCARD_MULTI
        unreserved = "\w|\.|\-"
        special = "%s|%s" % (quest, asterisk)
        spec_chrs = "%s+|%s" % (quest, asterisk)
        punc = "\!|\"|\;|\#|\$|\%|\&|\'|\(|\)|\+|\,|\/|\:|\<|\=|\>|\@|\[|\]|\^|\`|\{|\||\}|\~|\-"
        quoted = r"\\(\\" + "|%s|%s)" % (special, punc)
        avstring = "%s|%s" % (unreserved, quoted)
        value_string_pattern = "^((%s+|%s*(%s)+|%s(%s)+)(%s)?|%s)$" % (quest,
                                                                       quest, avstring,
                                                                       asterisk, avstring,
                                                                       spec_chrs,
                                                                       CPE2_3_FS._LOGICAL)

        part_value_rxc = re.compile(value_string_pattern)
        return part_value_rxc.match(str_value) is not None

    @classmethod
    def _is_valid_fs_language(cls, str_value):
        """
        Return True if the input value of WFN attribute "language" is valid,
        and otherwise False.
        """

        # Compilation of regular expression associated with value of CPE part
        region = "([%s]{2}|(%s){3})" % (CPE2_3._ALPHA, CPE2_3._DIGIT)
        language = "[%s]{2,3}" % CPE2_3._ALPHA
        LANGTAG = "%s(\-%s)?" % (language, region)

        value_lang_pattern = r"^(%s|%s)$" % (LANGTAG, CPE2_3_FS._LOGICAL)

        lang_value_rxc = re.compile(value_lang_pattern)

        return lang_value_rxc.match(str_value) is not None

    @classmethod
    def _get_str_value_dict(cls, v):
        """
        Returns the textual logical value associated with the value v.
        If v is not a logical value it returns v.
        """

        result = v

        if v in CPE2_3_FS._int_to_string_logical_dict:
            result = CPE2_3_FS._int_to_string_logical_dict[v]

        return result

    @classmethod
    def _get_int_value_dict(cls, v):
        """
        Returns the internal logical value associated with the value v.
        If v is not a logical value it returns v.
        """

        result = v

        if v in CPE2_3_FS._string_to_int_logical_dict:
            result = CPE2_3_FS._string_to_int_logical_dict[v]

        return result

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str="cpe:2.3:::::::::::"):
        """
        Checks that input CPE name string is valid according to binding
        style formatted string and, if so, stores the component
        in a dictionary.
        """

        CPE2_3.__init__(self, cpe_str)
        CPE2_3_FS.style = CPE2_3.STYLE_FS
        self._validate()

    def __len__(self):
        """
        Returns the number of parts of CPE name.

        - TEST: a CPE name without components
        >>> fs = "cpe:2.3:*:*:*:*:*:*:*:*:*:*:*"
        >>> c = CPE2_3_FS(fs)
        >>> len(c)
        11

        - TEST: a CPE name with some elements
        >>> fs = 'cpe:2.3:a:microsoft:windows:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> len(c)
        11

        - TEST: a CPE name with all elements
        >>> fs = 'cpe:2.3:a:hp:insight_diagnostics:7.4.0.1570:online:windows_2000:es-es:x64:*:-:-'
        >>> c = CPE2_3_FS(fs)
        >>> len(c)
        11
        """

        return len(CPE2_3.wfn_part_keys)

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE name as a string.

        - TEST: existing item
        >>> fs = 'cpe:2.3:a:hp:insight:7.4.0.1570:-:*:*:online:win2003:x64:*'
        >>> c = CPE2_3_FS(fs)
        >>> c[0] == 'a'
        True

        - TEST: existing item
        >>> fs = 'cpe:2.3:a:hp:insight:7.4.0.1570:-:*:*:online:win2003:x64:*'
        >>> c = CPE2_3_FS(fs)
        >>> c[9] == "x64"
        True

        - TEST: not existing valid item
        >>> fs = 'cpe:2.3:a:hp:insight:7.4.0.1570:-:*:*:online:win2003:x64:*'
        >>> c = CPE2_3_FS(fs)
        >>> c[10]
        '*'

        - TEST: not valid item
        >>> fs = 'cpe:2.3:a:hp:insight:7.4.0.1570:-:*:*:online:win2003:x64:*'
        >>> c = CPE2_3_FS(fs)
        >>> c[14]
        Traceback (most recent call last):
        KeyError: 'index not exists. Possible values: 0-10'
        """

        keys = CPE2_3_FS.wfn_ordered_part_dict.keys()
        if i not in keys:
            max_index = len(keys) - 1
            msg = "index not exists. Possible values: 0-%s" % max_index
            raise KeyError(msg)

        part_key = CPE2_3_FS.wfn_ordered_part_dict[i]
        value = CPE2_3_FS._get_str_value_dict(self._cpe_dict[part_key])

        return CPE2_3_FS._get_str_value_dict(value)

    def __eq__(self, cpe):
        """
        Return True if "cpe" is equal to self object.

        - TEST: equals
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:es-es:-:-:-:-'
        >>> c = CPE2_3_FS(fs)
        >>> c == c
        True

        - TEST: not equals
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:es-es:-:-:-:-'
        >>> c = CPE2_3_FS(fs)
        >>> uri2 = 'cpe:2.3:a:ubuntu:*:12.04:desktop:*:es-es:-:-:-:-'
        >>> c2 = CPE2_3_FS(uri2)
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
        eqSw_edition = self.getSw_edition() == cpe.getSw_edition()
        eqTarget_sw = self.getTarget_sw() == cpe.getTarget_sw()
        eqTarget_hw = self.getTarget_hw() == cpe.getTarget_hw()
        eqOther = self.getOther() == cpe.getOther()

        return (eqPart and eqVendor and eqProduct and eqVersion and
                eqUpdate and eqEdition and eqLanguage and eqSw_edition and
                eqTarget_sw and eqTarget_hw and eqOther)

    def _validate(self):
        """
        Checks CPE name with formatted string style is valid.
        """

        # #####################
        #  CHECK CPE NAME PARTS
        # #####################

        # Compilation of regular expression associated with parts of CPE name
        typesys = "(?P<%s>(h|o|a|%s))" % (CPE2_3.KEY_PART,
                                          CPE2_3_FS._LOGICAL)

        aux_pattern = "(?P<%s>[^\:]+)"
        vendor = aux_pattern % (CPE2_3.KEY_VENDOR)
        product = aux_pattern % (CPE2_3.KEY_PRODUCT)
        version = aux_pattern % (CPE2_3.KEY_VERSION)
        update = aux_pattern % (CPE2_3.KEY_UPDATE)
        edition = aux_pattern % (CPE2_3.KEY_EDITION)
        language = aux_pattern % (CPE2_3.KEY_LANGUAGE)
        sw_edition = aux_pattern % (CPE2_3.KEY_SW_EDITION)
        target_sw = aux_pattern % (CPE2_3.KEY_TARGET_SW)
        target_hw = aux_pattern % (CPE2_3.KEY_TARGET_HW)
        other = aux_pattern % (CPE2_3.KEY_OTHER)

        parts_pattern = "^cpe:2.3:%s" % typesys

        aux_parts_pattern = "\:%s"
        parts_pattern += aux_parts_pattern % vendor
        parts_pattern += aux_parts_pattern % product
        parts_pattern += aux_parts_pattern % version
        parts_pattern += aux_parts_pattern % update
        parts_pattern += aux_parts_pattern % edition
        parts_pattern += aux_parts_pattern % language
        parts_pattern += aux_parts_pattern % sw_edition
        parts_pattern += aux_parts_pattern % target_sw
        parts_pattern += aux_parts_pattern % target_hw
        parts_pattern += aux_parts_pattern % other
        parts_pattern += "$"

        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE name
        parts_match = parts_rxc.match(self.str)

        # Validation of CPE name parts
        if (parts_match is None):
            msg = "Malformed CPE name: validation of parts failed"
            raise ValueError(msg)

        for pk in CPE2_3.wfn_part_keys:
            value = parts_match.group(pk)

            # Logical value
            if (value == CPE2_3_FS.VALUE_ANY_VALUE):
                value = CPE2_3_FS._VALUE_INT_ANY
            elif (value == CPE2_3_FS.VALUE_NOT_APPLICABLE):
                value = CPE2_3_FS._VALUE_INT_NA
            else:
                # String value
                if pk == CPE2_3.KEY_LANGUAGE:
                    if not CPE2_3_FS._is_valid_fs_language(value):
                        msg = "Malformed CPE name: value '%s' is invalid" % value
                        raise ValueError(msg)
                else:
                    if not CPE2_3_FS._is_valid_fs_value(value):
                        msg = "Malformed CPE name: value '%s' is invalid " % value
                        raise ValueError(msg)

            self._cpe_dict[pk] = value

        return self._cpe_dict

    def get_fs_string(self):
        """
        Return the formatted string of CPE name.
        """

        fs = "cpe:2.3:"
        for i, k in enumerate(CPE2_3_FS.wfn_ordered_part_dict):
            if k in self._cpe_dict.keys():
                v = self._cpe_dict[k]
                fs += "%s:" % CPE2_3_FS._get_str_value_dict(v)

        fs = fs[0:len(fs) - 1]

    def isHardware(self):
        """
        Returns True if CPE name corresponds to hardware elem.

        - TEST: is HW
        >>> fs = 'cpe:2.3:h:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isHardware() == True
        True

        - TEST: is not HW
        >>> fs = 'cpe:2.3:o:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isHardware() == False
        True

        - TEST: is not HW
        >>> fs = 'cpe:2.3:a:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isHardware() == False
        True
        """

        # Value of part of CPE name
        part_value = self.getPart()

        isHW = part_value == CPE2_3.VALUE_PART_HW
        isAny = part_value == CPE2_3_FS.VALUE_ANY_VALUE

        return (isHW or isAny)

    def isOperatingSystem(self):
        """
        Returns True if CPE name corresponds to operating system elem.

        - TEST: is not OS
        >>> fs = 'cpe:2.3:h:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isOperatingSystem() == False
        True

        - TEST: is OS
        >>> fs = 'cpe:2.3:o:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isOperatingSystem() == True
        True

        - TEST: is not OS
        >>> fs = 'cpe:2.3:a:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isOperatingSystem() == False
        True
        """

        # Value of part of CPE name
        part_value = self.getPart()

        isOS = part_value == CPE2_3.VALUE_PART_OS
        isAny = part_value == CPE2_3_FS.VALUE_ANY_VALUE

        return (isOS or isAny)

    def isApplication(self):
        """
        Returns True if CPE name corresponds to application elem.

        - TEST: is not application
        >>> fs = 'cpe:2.3:h:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isApplication() == False
        True

        - TEST: is not application
        >>> fs = 'cpe:2.3:o:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isApplication() == False
        True

        - TEST: is application
        >>> fs = 'cpe:2.3:a:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.isApplication() == True
        True
        """

        # Value of part of CPE name
        part_value = self.getPart()

        isApp = part_value == CPE2_3.VALUE_PART_APP
        isAny = part_value == CPE2_3_FS.VALUE_ANY_VALUE

        return (isApp or isAny)

    def getPart(self):
        """
        Returns the part type of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getPart()
        'a'

        - TEST: is operating system
        >>> fs = 'cpe:2.3:o:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getPart()
        'o'

        - TEST: is hardware
        >>> fs = 'cpe:2.3:h:*:*:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getPart()
        'h'
        """

        return self.__getitem__(0)

    def getVendor(self):
        """
        Returns the vendor name of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:windows:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getVendor()
        'microsoft'
        """

        return self.__getitem__(1)

    def getProduct(self):
        """
        Returns the product name of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:windows:*:*:*:*:*:*:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getProduct()
        'windows'
        """

        return self.__getitem__(2)

    def getVersion(self):
        """
        Returns the version of product of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:*:*:*:*:*:-:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getVersion()
        '8.0'
        """

        return self.__getitem__(3)

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE name.

        - TEST: is operating system
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:*:-:-:-:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getUpdate()
        'sp2'
        """

        return self.__getitem__(4)

    def getEdition(self):
        """
        Returns the edition of product of CPE name.

        - TEST: is operating system
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:pro?:*:-:-:-:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getEdition()
        'pro?'
        """

        return self.__getitem__(5)

    def getLanguage(self):
        """
        Returns the internationalization information of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:es-es:-:-:-:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getLanguage()
        'es-es'
        """

        return self.__getitem__(6)

    def getSw_edition(self):
        """
        Returns the software edition of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:*:home:-:-:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getSw_edition()
        'home'
        """

        return self.__getitem__(7)

    def getTarget_sw(self):
        """
        Returns the software computing environment of CPE name
        within which the product operates.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:*:*:-:*:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getTarget_sw()
        '-'
        """

        return self.__getitem__(8)

    def getTarget_hw(self):
        """
        Returns the arquitecture of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:*:-:-:x64:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getTarget_hw()
        'x64'
        """

        return self.__getitem__(9)

    def getOther(self):
        """
        Returns the other information part of CPE name.

        - TEST: is application
        >>> fs = 'cpe:2.3:a:microsoft:*:8.0:sp2:*:*:-:-:-:*'
        >>> c = CPE2_3_FS(fs)
        >>> c.getOther()
        '*'
        """

        return self.__getitem__(10)


if __name__ == "__main__":

    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
