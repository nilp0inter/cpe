#! /usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

'''
File: cpe2_3_wfn.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Module for the treatment of identifiers in accordance with
             binding style Well-Formed Name (WFN) of version 2.3 of
             specification CPE (Common Platform Enumeration).
'''


from cpe2_3 import CPE2_3

import re
import itertools


class CPE2_3_WFN(CPE2_3):
    """
    Implementation of CPE 2.3 specification.

    - TEST: bad WFN
    >>> wfn = 'baduri'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 131, in __init__
        self._validate_uri()
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 202, in _validate_uri
        raise TypeError(msg)
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: WFN with whitespaces
    >>> wfn = 'cpe con espacios'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 131, in __init__
        self._validate_uri()
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 170, in _validate_uri
        raise TypeError(msg)
    TypeError: Malformed CPE, it must not have whitespaces

    - TEST: an empty CPE.
    >>> wfn = 'wfn:[]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an empty CPE with bad part name
    >>> wfn = 'wfn:[bad="hw"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 131, in __init__
        1: CPE2_3.KEY_VENDOR,
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 202, in _validate_uri
        CPE2_3.KEY_VERSION,
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: an operating system CPE
    >>> wfn = 'wfn:[part="o", vendor="acme", product="producto", version="1.0",
    >>> update="update2", edition="pro", language="en-us"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an application CPE
    >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics",
    >>> version="7\.4\.0\.1570", sw_edition="online", target_sw="windows_2003",
    >>> target_hw="x64", language=ANY, other=NA]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an application CPE
    >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics",
    >>> version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an CPE with special characters
    >>> wfn = 'wfn:[part="h", vendor="hp", product="insight\diagnostics",
    >>> version="8.0~"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe2_3_wfn.py", line 158, in __init__
        self._validate_uri()
      File "cpe2_3_wfn.py", line 278, in _validate_uri
        raise TypeError(msg)
    TypeError: Malformed CPE, vendor value is invalid
    """

    ALPHA = "a-zA-Z"
    DIGIT = "\d"

    VALUE_NULL = 0
    VALUE_ANY = 1
    VALUE_NA = 2

    PCE_DICT = {
        '!': "%21",
        '"': "%22",
        '#': "%23",
        '$': "%24",
        '%': "%25",
        '&': "%26",
        '\'': "%27",
        '(': "%28",
        ')': "%29",
        '*': "%2a",
        '+': "%2b",
        ',': "%2c",
        '/': "%2f",
        ':': "%3a",
        ';': "%3b",
        '<': "%3c",
        '=': "%3d",
        '>': "%3e",
        '?': "%3f",
        '@': "%40",
        '[': "%5b",
        '\\': "%5c",
        ']': "%5d",
        '^': "%5e",
        '`': "%60",
        '{': "%7b",
        '|': "%7c",
        '}': "%7d",
        '~': "%7e"
    }

    wfn_part_keys = set(itertools.chain(CPE2_3.uri_part_keys,
                                        CPE2_3.extend_part_keys))

    wfn_order_parts_dict = set(itertools.chain(CPE2_3.uri_order_parts_dict,
                                               CPE2_3.extend_order_parts_dict))

    def __init__(self, cpe_str="wfn:[]"):
        """
        Checks that input CPE name string is valid according to binding
        style Well-Formed Name (WFN) and, if so, stores the component
        in a dictionary.

        if cpe_str is empty returns an empty WFN
        (a WFN containing no attribute-value pairs).
        """

        CPE2_3.__init__(self)

        # Store CPE identifier:
        #     CPE names are case-insensitive.
        #     To reduce potential for confusion,
        #     all CPE Names should be written in lowercase
        self.str = cpe_str.lower()

        self._validate_wfn()

    @classmethod
    def _is_valid_wfn_value(cls, str_value):
        """
        TODO
        """

        # Compilation of regular expression associated with value of CPE part
        punc_no_dash = "[\!|;|\#|\$|%|&|'|\(|\)|\+|\.|/"
        punc_no_dash += ":|\<|=|\>|@|\[|\|\^|`|\{|\||\}|~]"
        punc_w_dash = "%s|\-" % punc_no_dash

        special = "[\?\*]"
        quoted1 = "\\(\\|%s|%s)" % (special, punc_no_dash)
        quoted2 = "\\(\\|%s|%s)" % (special, punc_w_dash)
        unreserved = "[%s%s_]" % (CPE2_3_WFN.ALPHA, CPE2_3_WFN.DIGIT)

        body1 = "(%s|%s)" % (unreserved, quoted1)
        body2 = "(%s|%s)" % (unreserved, quoted2)
        body = "((%s%s*)|%s{2})" % (body1, body2, body2)

        spec_chrs = "(\?+|\*)"

        avstring = "(%s|(%s%s*))%s?" % (body, spec_chrs, body2, spec_chrs)

        value_string_pattern = "^%s$" % avstring

        part_value_rxc = re.compile(value_string_pattern)

        return part_value_rxc.match(str_value) is not None

    @classmethod
    def _is_valid_wfn_language(cls, str_value):
        """
        TODO
        """

        # Compilation of regular expression associated with value of CPE part
        region = "([%s]{2}|[%s]{3})" % (CPE2_3_WFN.ALPHA, CPE2_3_WFN.DIGIT)
        language = "[%s]{2,3}" % CPE2_3_WFN.ALPHA
        LANGTAG = "%s(\-%s)?" % (language, region)

        value_lang_pattern = "^%s?$" % LANGTAG

        lang_value_rxc = re.compile(value_lang_pattern)

        return lang_value_rxc.match(str_value) is not None

    def _validate_wfn(self):
        """
        Checks CPE name with WFN style is valid.

        A CPE Name is a percent-encoded WFN with each name
        starting with the prefix 'wfn:'.

        Each platform can be broken down into many distinct parts.
        A CPE Name specifies a single part and is used to identify
        any platform that matches the description of that part.
        The distinct parts are:

        - Hardware part: the physical platform supporting the IT system.
        - Operating system part: the operating system controls and manages the
          IT hardware.
        - Application part: software systems, services, servers, and packages
          installed on the system.

        CPE name syntax: wfn:[a1=v1, a2=v2, …, an=vn]

        Only the following attributes SHALL be permitted in a WFN
        attribute-value pair:
        a. part
        b. vendor
        c. product
        d. version
        e. update
        f. edition
        g. language
        h. sw_edition
        i. target_sw
        j. target_hw
        k. other
        """

        # CPE ID must not have whitespaces
        if (self.str.find(" ") != -1):
            msg = "Malformed CPE, it must not have whitespaces"
            raise ValueError(msg)

        # #####################
        #  CHECK CPE ID PARTS
        # #####################

        # Compilation of regular expression associated with parts of CPE ID
        typesys = "%s=?P<%s>\"(h|o|a)\"" % (CPE2_3.KEY_PART, CPE2_3.KEY_PART)

        aux_pattern = "%s=?P<%s>[^,]+"
        vendor = aux_pattern % (CPE2_3.KEY_VENDOR, CPE2_3.KEY_VENDOR)
        product = aux_pattern % (CPE2_3.KEY_PRODUCT, CPE2_3.KEY_PRODUCT)
        version = aux_pattern % (CPE2_3.KEY_VERSION, CPE2_3.KEY_VERSION)
        update = aux_pattern % (CPE2_3.KEY_UPDATE, CPE2_3.KEY_UPDATE)
        edition = aux_pattern % (CPE2_3.KEY_EDITION, CPE2_3.KEY_EDITION)
        language = aux_pattern % (CPE2_3.KEY_LANGUAGE, CPE2_3.KEY_LANGUAGE)
        sw_edition = aux_pattern % (CPE2_3.KEY_SW_EDITION, CPE2_3.KEY_SW_EDITION)
        target_sw = aux_pattern % (CPE2_3.KEY_TARGET_SW, CPE2_3.KEY_TARGET_SW)
        target_hw = aux_pattern % (CPE2_3.KEY_TARGET_HW, CPE2_3.KEY_TARGET_HW)
        other = aux_pattern % (CPE2_3.KEY_OTHER, CPE2_3.KEY_OTHER)

        parts_pattern = "^wfn:\["
        parts_pattern += "(%s)?" % typesys

        aux_parts_pattern = "(, (%s)?)?"
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
        parts_pattern += "\]$"

        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE ID
        parts_match = parts_rxc.match(self.str)

        # Validation of CPE ID parts
        if (parts_match is None):
            msg = "Input identifier is not a valid CPE ID: "
            msg += "Error to split CPE ID parts"
            raise TypeError(msg)

        for pk in CPE2_3.part_keys:
            value = parts_match.group(pk)

            if (value is None):
                # Attribute not specified
                value = CPE2_3_WFN. VALUE_NULL
            else:
                if value.count('"') == 0:
                    # Logical value
                    if (value == "ANY"):
                        value = CPE2_3_WFN.VALUE_ANY
                    elif (value == "NA"):
                        value = CPE2_3_WFN.VALUE_NA
                    else:
                        msg = "Malformed CPE, logical value in %s is invalid" % pk
                        raise ValueError(msg)

                elif value.count('"') == 2:
                    # String value
                    if pk == CPE2_3.KEY_LANGUAGE:
                        if not CPE2_3_WFN._is_valid_wfn_language(value):
                            msg = "Malformed CPE, language value is invalid"
                            raise TypeError(msg)
                    else:
                        if not CPE2_3_WFN._is_valid_wfn_value(value):
                            msg = "Malformed CPE, %s value is invalid " % pk
                            raise ValueError(msg)
                else:
                    # Bad value
                    msg = "Malformed CPE, %s value is invalid" % value
                    raise ValueError(msg)

            self.cpe_dict[pk] = value

        return self.cpe_dict

    def __len__(self):
        """
        Returns the number of parts of CPE ID.

        - TEST: a CPE name without components
        >>> wfn = "wfn:[]"
        >>> c = CPE2_3_WFN(wfn)
        >>> len(c)
        0

        - TEST: a CPE name with some elements
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> len(c)
        3

        - TEST: a CPE name with all elements
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics",
        >>> version="7\.4\.0\.1570", sw_edition="online", target_sw="windows_2003",
        >>> target_hw="x64", language=ANY, other=NA]'
        >>> c = CPE2_3_WFN(wfn)
        >>> len(c)
        7
        """

        count = 0
        for k, v in enumerate(self.cpe_dict):
            if v != CPE2_3_WFN.VALUE_NULL:
                count += 1

        return count

    def get(self, att):
        """
        Takes two arguments, a WFN (self) and an attribute att,
        and returns the value of att.
        If the attribute att is unspecified in self, returns the
        default value ANY.
        """

        if att in self.cpe_dict.keys():
            value = self.cpe_dict[att]
            if value == CPE2_3_WFN.VALUE_NULL:
                # Attribute not specified in WFN
                return CPE2_3_WFN.VALUE_ANY
            else:
                return value
        else:
            # Attribute not valid
            msg = "WFN Attribute not valid"
            raise TypeError(msg)

    def set(self, att, value):
        """
        Takes three arguments, a WFN (self), an attribute (att), and a value
        (vaue). If the attribute att is unspecified in self,
        adds the attribute-value pair att=value to self.
        If the attribute att is specified in self, replaces its value with value.
        If value is None, deletes att from self if att is specified in self,
        otherwise has no effect. The function always returns the new value of
        self.
        """

        # Check valid value
        if value is not None:
            if att == CPE2_3_WFN. KEY_LANGUAGE:
                if not CPE2_3_WFN._is_valid_wfn_language(value):
                    msg = "Language value not valid"
                    raise ValueError(msg)
            else:
                if not CPE2_3_WFN. _is_valid_wfn_value(value):
                    msg = "WFN value not valid"
                    raise ValueError(msg)

        # Correct value
        if att in self.cpe_dict.keys():
            if value is None:
                # Del attribute
                self.cpe_dict[att] = CPE2_3_WFN.VALUE_NULL
            else:
                # Replace value
                self.cpe_dict[att] = value
        else:
            msg = "Attribute not valid"
            raise ValueError(msg)

        return self.get_wfn_string()

    def get_wfn_string(self):
        """
        TODO
        """

        wfn = "wfn:["
        for k, v in enumerate(CPE2_3_WFN.wfn_order_parts_dict):
            if k in self.cpe_dict.keys():
                wfn += self.cpe_dict[k]
                wfn += "="

                if v == CPE2_3_WFN.VALUE_ANY:
                    wfn += "ANY"
                elif v == CPE2_3_WFN.VALUE_NA:
                    wfn += "NA"
                else:
                    wfn += '"v", '

        wfn = wfn[0:len(wfn)-2]
        wfn += "]"

    def _trim(cls, s):
        """
        Remove trailing colons from the URI back to the first non-colon.
        """
        reverse = s[::-1]
        idx = 0
        for i in range(0, len(reverse)):
            if reverse[i, i] == ":":
                idx = idx + 1
            else:
                break

        # Return the substring after all trailing colons,
        # reversed back to its original character order.
        new_s = reverse[idx, len(reverse) - 1]
        return new_s[::-1]

    @classmethod
    def _is_alphanum(cls, c):
        """
        Returns True if c is an uppercase letter, a lowercase letter,
        a digit, or the underscore, otherwise False.
        """

        alphanum_pattern = "[%s%s-]" % (CPE2_3_WFN.ALPHA, CPE2_3_WFN.DIGIT)
        alphanum_rxc = re.compile(alphanum_pattern)

        return alphanum_rxc.match(c) is not None

    def _pct_encode(cls, c):
        """
        Return the appropriate percent-encoding of character c.
        Certain characters are returned without encoding.
        """

        CPE2_3_WFN.PCE_DICT['-'] = c  # bound without encoding
        CPE2_3_WFN.PCE_DICT['.'] = c  # bound without encoding

        return CPE2_3_WFN.PCE_DICT[c]

    def _transform_for_uri(cls, s):
        """
        Scans an input string s and applies the following transformations:
        - Pass alphanumeric characters thru untouched
        - Percent-encode quoted non-alphanumerics as needed
        - Unquoted special characters are mapped to their special forms.
        """

        result = ""
        idx = 0
        while (idx < len(s)):
            thischar = s[idx:idx]  # get the idx'th character of s

            # alphanumerics (incl. underscore) pass untouched
            if (CPE2_3_WFN._is_alphanum(thischar)):
                result += thischar
                idx = idx + 1
                continue

            # escape character
            if (thischar == "\\"):
                idx = idx + 1
                nxtchar = s[idx:idx]
                result += CPE2_3_WFN._pct_encode(nxtchar)
                idx = idx + 1
                continue

            # Bind the unquoted '?' special character to "%01"
            if (thischar == "?"):
                result += "%01"

            # Bind the unquoted '*' special character to "%02"
            if (thischar == "*"):
                result += "%02"

            idx = idx + 1

            return result

    @classmethod
    def _bind_value_for_uri(cls, s):
        """
        Takes a string s and converts it to the proper string for
        inclusion in a CPE v2.2-conformant URI. The logical value ANY
        binds to the blank in the 2.2-conformant URI.
        """

        if s == CPE2_3_WFN.VALUE_ANY:
            return ""

        # The value NA binds to a single hyphen
        if s == CPE2_3_WFN.VALUE_NA:
            return "-"

        # s is a string value
        return CPE2_3_WFN._transform_for_uri(s)

    @classmethod
    def _pack(cls, ed, sw_ed, t_sw, t_hw, oth):
        """
        “Pack” the values of the five arguments into the single edition
        component. If all the values are blank, just return a blank.
        """

        if (sw_ed == "") and (t_sw == "") and (t_hw == "") and (oth == ""):
            # All the extended attributes are blank,
            # so don't do any packing, just return ed

            return ed

        # Otherwise, pack the five values into a single string
        # prefixed and internally delimited with the tilde
        return "~%s~%s~%s~%s~%s" % (ed, sw_ed, t_sw, t_hw, oth)

    def bind_to_uri(self):
        """
        Converts the binding style WFN to URI 2.2 version
        and returns version 2.2 CPE object
        """

        uri = "cpe:/"

        for a in CPE2_3.uri_part_keys:
            if a == CPE2_3.KEY_EDITION:
                # Call the pack() helper function to compute the proper
                # binding for the edition element

                ed = CPE2_3._bind_value_for_uri(self.getEdition())
                sw_ed = CPE2_3._bind_value_for_uri(self.getSw_edition())
                t_sw = CPE2_3._bind_value_for_uri(self.getTarget_sw())
                t_hw = CPE2_3._bind_value_for_uri(self.getTarget_hw())
                oth = CPE2_3._bind_value_for_uri(self.getOther())

                v = CPE2_3._pack(ed, sw_ed, t_sw, t_hw, oth)
            else:
                # Get the value for a in self, then bind to a string
                # for inclusion in the URI.

                v = CPE2_3._bind_value_for_uri(self.get(a))

            # Append v to the URI then add a colon.
            uri += "%s:" % v

        # Return the URI string, with trailing colons trimmed
        return CPE2_3_WFN._trim(uri)

    def isHardware(self):
        """
        Returns True if CPE ID corresponds to hardware elem.

        - TEST: is HW
        >>> wfn = 'wfn:[part="h"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isHardware() == True
        True

        - TEST: is not HW
        >>> wfn = 'wfn:[part="o"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isHardware() == False
        True

        - TEST: is not HW
        >>> wfn = 'wfn:[part="a"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isHardware() == False
        True
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_3.KEY_PART]

        isHW = type_value == CPE2_3.KEY_PART_HW
        isEmpty = type_value == CPE2_3_WFN.VALUE_NULL
        isAny = type_value == CPE2_3_WFN.VALUE_ANY

        return (isHW or isEmpty or isAny)

    def isOperatingSystem(self):
        """
        Returns True if CPE ID corresponds to operating system elem.

        - TEST: is not OS
        >>> wfn = 'wfn:[part="h"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isOperatingSystem() == False
        True

        - TEST: is OS
        >>> wfn = 'wfn:[part=o"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isOperatingSystem() == True
        True

        - TEST: is not OS
        >>> wfn = 'wfn:[part="a"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isOperatingSystem() == False
        True
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_3.KEY_PART]

        isOS = type_value == CPE2_3.KEY_PART_OS
        isEmpty = type_value == CPE2_3_WFN.VALUE_NULL
        isAny = type_value == CPE2_3_WFN.VALUE_ANY

        return (isOS or isEmpty or isAny)

    def isApplication(self):
        """
        Returns True if CPE ID corresponds to application elem.

        - TEST: is not application
        >>> wfn = 'wfn:[part="h"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isApplication() == False
        True

        - TEST: is not application
        >>> wfn = 'wfn:[part="o"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isApplication() == False
        True

        - TEST: is application
        >>> wfn = 'wfn:[part="a"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isApplication() == True
        True
        """

        # Value of part type of CPE ID
        type_value = self.cpe_dict[CPE2_3.KEY_PART]

        isApp = type_value == CPE2_3.KEY_PART_APP
        isEmpty = type_value == CPE2_3_WFN.VALUE_NULL
        isAny = type_value == CPE2_3_WFN.VALUE_ANY

        return (isApp or isEmpty or isAny)

    def getType(self):
        """
        Returns the part type of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getType()
        'a'

        - TEST: is operating system
        >>> wfn = 'wfn:[part="o"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getType()
        'o'

        - TEST: is hardware
        >>> wfn = 'wfn:[part="h"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getType()
        'h'
        """

        return self.cpe_dict[CPE2_3.KEY_PART]

    def getVendor(self):
        """
        Returns the vendor name of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getVendor()
        'microsoft'
        """

        return self.cpe_dict[CPE2_3.KEY_VENDOR]

    def getProduct(self):
        """
        Returns the product name of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getProduct()
        'windows'
        """

        return self.cpe_dict[CPE2_3.KEY_PRODUCT]

    def getVersion(self):
        """
        Returns the version of product of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getVersion()
        '8\.0'
        """

        return self.cpe_dict[CPE2_3.KEY_VERSION]

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE ID.

        - TEST: is operating system
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getUpdate()
        'sp2'
        """

        return self.cpe_dict[CPE2_3.KEY_UPDATE]

    def getEdition(self):
        """
        Returns the edition of product of CPE ID.

        - TEST: is operating system
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", edition="pro"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getEdition()
        'pro'
        """

        return self.cpe_dict[CPE2_3.KEY_EDITION]

    def getLanguage(self):
        """
        Returns the internationalization information of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", language="es-es"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getLanguage()
        'es-es'
        """

        return self.cpe_dict[CPE2_3.KEY_LANGUAGE]

    def getSw_edition(self):
        """
        Returns the software edition of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", sw_edition="home"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getSw_edition()
        'home'
        """

        return self.cpe_dict[CPE2_3.KEY_SW_EDITION]

    def getTarget_sw(self):
        """
        Returns the software computing environment of CPE ID
        within which the product operates.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", target_sw=NA]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getTarget_sw()
        NA
        """

        return self.cpe_dict[CPE2_3.KEY_TARGET_SW]

    def getTarget_hw(self):
        """
        Returns the arquitecture of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", target_hw="x64"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getTarget_hw()
        'x64'
        """

        return self.cpe_dict[CPE2_3.KEY_TARGET_HW]

    def getOther(self):
        """
        Returns the other information part of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", other=NA'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getOther()
        NA
        """

        return self.cpe_dict[CPE2_3.KEY_OTHER]

    def __unicode__(self):
        """
        Print CPE URI as string.
        """

        return self.str

    def __eq__(self, cpe):
        """
        Return True if "cpe" is equal to self object.

        - TEST: equals
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", language="es-es"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c == c
        True

        - TEST: not equals
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY,
        >>> version="8\.0", update="sp2", language="es-es"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> uri2 = 'wfn:[part="a", vendor="microsoft"]'
        >>> c2 = CPE2_3(uri2)
        >>> c == c2
        False
        """

        eqPart = self.cpe_dict[CPE2_3.KEY_PART] == cpe.getType()
        eqVendor = self.cpe_dict[CPE2_3.KEY_VENDOR] == cpe.getVendor()
        eqProduct = self.cpe_dict[CPE2_3.KEY_PRODUCT] == cpe.getProduct()
        eqVersion = self.cpe_dict[CPE2_3.KEY_VERSION] == cpe.getVersion()
        eqUpdate = self.cpe_dict[CPE2_3.KEY_UPDATE] == cpe.getUpdate()
        eqEdition = self.cpe_dict[CPE2_3.KEY_EDITION] == cpe.getEdition()
        eqLanguage = self.cpe_dict[CPE2_3.KEY_LANGUAGE] == cpe.getLanguage()
        eqSw_edition = self.cpe_dict[CPE2_3.KEY_SW_EDITION] == cpe.getSw_edition()
        eqTarget_sw = self.cpe_dict[CPE2_3.KEY_TARGET_SW] == cpe.getTarget_sw()
        eqTarget_hw = self.cpe_dict[CPE2_3.KEY_TARGET_HW] == cpe.getTarget_hw()
        eqOther = self.cpe_dict[CPE2_3.KEY_OTHER] == cpe.getOther()

        return (eqPart and eqVendor and eqProduct and eqVersion and
                eqUpdate and eqEdition and eqLanguage and eqSw_edition and
                eqTarget_sw and eqTarget_hw and eqOther)


if __name__ == "__main__":
    ##wfn = 'cpe:/'
    ##wfn = 'cpe:/::::::'
    ##wfn = 'cpe:/o:microsoft:windows_xp:::pro'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:pro:en-us'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:pro:en-usss'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:pro:en-123'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:pro:e-us'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:pro:esss-us'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:~~~un~dos:es-ES'
    ##wfn = 'cpe:/a:acme:product:1.0:update2:~~~un~dos~:es-ES'
    ##wfn = 'cpe:/a:acme:product:1.%02:update2:~~~un~dos~:es-ES'
    #wfn = 'cpe:/a:acme:product:1.%250:update2:~~~un~dos~:es-ES'
    ##wfn = 'cpe:/a:acme:product:1.%80:update2:~~~un~dos~:es-ES'
    ##wfn = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'

    #ce = CPE2_3_WFN(wfn)
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
