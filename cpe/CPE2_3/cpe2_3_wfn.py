#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe2_3_wfn.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Module for the treatment of identifiers in accordance with
             binding style Well-Formed Name (WFN) of version 2.3 of
             specification CPE (Common Platform Enumeration).
'''


from cpe2_3_base import CPE2_3_BASE

import re
import itertools


class CPE2_3_WFN(CPE2_3_BASE):
    """
    Implementation of CPE 2.3 specification.

    - TEST: bad WFN
    >>> wfn = 'baduri'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe2_3_wfn.py", line 131, in __init__
        self._validate_wfn()
      File "cpe2_3_wfn.py", line 202, in _validate_wfn
        raise TypeError(msg)
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

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
      File "cpe/CPE2_3/cpe2_3_wfn.py", line 202, in _validate_wfn
        CPE2_3.KEY_VERSION,
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: an operating system CPE
    >>> wfn = 'wfn:[part="o", vendor="acme", product="producto", version="1\.0", update="update2", edition="pro", language="en-us"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an application CPE
    >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", sw_edition="online", target_sw="windows_2003", target_hw="x64", language=ANY, other=NA]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an application CPE
    >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an CPE with special characters
    >>> wfn = 'wfn:[part="h", vendor="hp", product="insight\diagnostics", version="8.0~"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe2_3_wfn.py", line 158, in __init__
        self._validate_wfn()
      File "cpe2_3_wfn.py", line 278, in _validate_wfn
        raise TypeError(msg)
    TypeError: Malformed CPE, vendor value is invalid
    """

    ALPHA = "a-zA-Z"
    DIGIT = "\d"

    VALUE_ANY_VALUE = "ANY"
    VALUE_NOT_APPLICABLE = "NA"

    VALUE_INT_NULL = 0
    VALUE_INT_ANY = 1
    VALUE_INT_NA = 2

    PCE_ASTERISK = "%02"
    PCE_QUESTION = "%01"

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

    DECODE_DICT = {
        "%21": '\\!',
        "%22": '\\\"',
        "%23": '\\#',
        "%24": '\\$',
        "%25": '\\%',
        "%26": '\\&',
        "%27": '\\\'',
        "%28": '\\(',
        "%29": '\\)',
        "%2a": '\\*',
        "%2b": '\\+',
        "%2c": '\\,',
        "%2f": '\\/',
        "%3a": '\\:',
        "%3b": '\\;',
        "%3c": '\\<',
        "%3d": '\\=',
        "%3e": '\\>',
        "%3f": '\\?',
        "%40": '\\@',
        "%5b": '\\[',
        "%5c": '\\\\',
        "%5d": '\\]',
        "%5e": '\\^',
        "%60": '\\`',
        "%7b": '\\{',
        "%7c": '\\|',
        "%7d": '\\}',
        "%7e": '\\~'
    }

    wfn_part_keys = set(itertools.chain(CPE2_3_BASE.uri_part_keys,
                                        CPE2_3_BASE.extend_part_keys))

    wfn_order_parts_dict = set(itertools.chain(CPE2_3_BASE.uri_order_parts_dict,
                                               CPE2_3_BASE.extend_order_parts_dict))

    def __init__(self, cpe_str="wfn:[]"):
        """
        Checks that input CPE name string is valid according to binding
        style Well-Formed Name (WFN) and, if so, stores the component
        in a dictionary.

        if cpe_str is empty returns an empty WFN
        (a WFN containing no attribute-value pairs).
        """

        CPE2_3_BASE.__init__(self, cpe_str)

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
        punc_no_dash = "\!\;\#\$\%\&\'\(\)\+\,\./\:\<\=\>\@\[\]\^\`\{\|\}\~"
        punc_w_dash = "%s\-" % punc_no_dash

        special = "\?\*"
        quoted1 = "\\(\\|%s|%s)" % (special, punc_no_dash)
        #print "quoted1: %s" % quoted1
        quoted2 = "\\(\\|%s|%s)" % (special, punc_w_dash)
        #print "quoted2: %s" % quoted2
        unreserved = "[%s%s_]" % (CPE2_3_WFN.ALPHA, CPE2_3_WFN.DIGIT)

        body1 = "(%s|%s)" % (unreserved, quoted1)
        body2 = "(%s|%s)" % (unreserved, quoted2)
        body = "(%s%s*|%s{2})" % (body1, body2, body2)
        print body
        print

        spec_chrs = "\?+|\*"

        avstring = "(%s|(%s)%s*)(%s)?" % (body, spec_chrs, body2, spec_chrs)

        print avstring
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

        # #####################
        #  CHECK CPE ID PARTS
        # #####################

        # Compilation of regular expression associated with parts of CPE ID
        typesys = "%s=(?P<%s>\"(h|o|a)\")?" % (CPE2_3_BASE.KEY_PART, CPE2_3_BASE.KEY_PART)

        aux_pattern = "%s=(?P<%s>[^\,]+)?"
        vendor = aux_pattern % (CPE2_3_BASE.KEY_VENDOR, CPE2_3_BASE.KEY_VENDOR)
        product = aux_pattern % (CPE2_3_BASE.KEY_PRODUCT, CPE2_3_BASE.KEY_PRODUCT)
        version = aux_pattern % (CPE2_3_BASE.KEY_VERSION, CPE2_3_BASE.KEY_VERSION)
        update = aux_pattern % (CPE2_3_BASE.KEY_UPDATE, CPE2_3_BASE.KEY_UPDATE)
        edition = aux_pattern % (CPE2_3_BASE.KEY_EDITION, CPE2_3_BASE.KEY_EDITION)
        language = aux_pattern % (CPE2_3_BASE.KEY_LANGUAGE, CPE2_3_BASE.KEY_LANGUAGE)
        sw_edition = aux_pattern % (CPE2_3_BASE.KEY_SW_EDITION, CPE2_3_BASE.KEY_SW_EDITION)
        target_sw = aux_pattern % (CPE2_3_BASE.KEY_TARGET_SW, CPE2_3_BASE.KEY_TARGET_SW)
        target_hw = aux_pattern % (CPE2_3_BASE.KEY_TARGET_HW, CPE2_3_BASE.KEY_TARGET_HW)
        other = aux_pattern % (CPE2_3_BASE.KEY_OTHER, CPE2_3_BASE.KEY_OTHER)

        parts_pattern = "^wfn:\[%s" % typesys

        aux_parts_pattern = "(\, %s)?"
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
        print parts_pattern
        print self.str

        # Partitioning of CPE ID
        parts_match = parts_rxc.match(self.str)
        print parts_match

        # Validation of CPE ID parts
        if (parts_match is None):
            msg = "Input identifier is not a valid CPE ID: "
            msg += "Error to split CPE ID parts"
            raise TypeError(msg)

        for pk in CPE2_3_WFN.wfn_part_keys:
            value = parts_match.group(pk)

            if (value is None):
                # Attribute not specified
                value = CPE2_3_WFN. VALUE_INT_NULL
            else:
                if value.count('"') == 0:
                    # Logical value
                    if (value == CPE2_3_WFN.VALUE_ANY_VALUE):
                        value = CPE2_3_WFN.VALUE_INT_ANY
                    elif (value == CPE2_3_WFN.VALUE_NOT_APPLICABLE):
                        value = CPE2_3_WFN.VALUE_INT_NA
                    else:
                        msg = "Malformed CPE, logical value in %s is invalid" % pk
                        raise ValueError(msg)

                elif value.count('"') == 2:
                    # String value
                    if pk == CPE2_3_BASE.KEY_LANGUAGE:
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
            print "%s  %s" % (k, v)
            if v != CPE2_3_WFN.VALUE_INT_NULL:
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
            if value == CPE2_3_WFN.VALUE_INT_NULL:
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
                self.cpe_dict[att] = CPE2_3_WFN.VALUE_INT_NULL
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
        for i, k in enumerate(CPE2_3_WFN.wfn_order_parts_dict):
            if k in self.cpe_dict.keys():
                wfn += k
                wfn += "="
                v = self.cpe_dict[k]

                if v == CPE2_3_WFN.VALUE_INT_ANY:
                    wfn += CPE2_3_WFN.VALUE_ANY
                elif v == CPE2_3_WFN.VALUE_INT_NA:
                    wfn += CPE2_3_WFN.VALUE_NA
                else:
                    wfn += '"%s", ' % v

        wfn = wfn[0:len(wfn)-2]
        wfn += "]"

    @classmethod
    def _trim(cls, s):
        """
        Remove trailing colons from the URI back to the first non-colon.

        - TEST: trailing colons necessary
        >>> s = '1:2::::'
        >>> CPE2_3_WFN._trim(s)
        1:2

        - TEST: trailing colons not necessary
        >>> s = '1:2:3:4:5:6'
        >>> CPE2_3_WFN._trim(s)
        1:2:3:4:5:6
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

        - TEST: alpha
        >>> c = 'A'
        >>> CPE2_2_WFN._is_alphanum(c)
        True

        - TEST: num
        >>> c = 2
        >>> CPE2_2_WFN._is_alphanum(c)
        True

        - TEST: char is _
        >>> c = '_'
        >>> CPE2_2_WFN._is_alphanum(c)
        True

        - TEST: char not valid
        >>> c = 'Ç'
        >>> CPE2_2_WFN._is_alphanum(c)
        False
        """

        alphanum_pattern = "[%s%s-]" % (CPE2_3_WFN.ALPHA, CPE2_3_WFN.DIGIT)
        alphanum_rxc = re.compile(alphanum_pattern)

        return alphanum_rxc.match(c) is not None

    @classmethod
    def _pct_encode(cls, c):
        """
        Return the appropriate percent-encoding of character c.
        Certain characters are returned without encoding.
        """

        CPE2_3_WFN.PCE_DICT['-'] = c  # bound without encoding
        CPE2_3_WFN.PCE_DICT['.'] = c  # bound without encoding

        return CPE2_3_WFN.PCE_DICT[c]

    @classmethod
    def _decode(cls, s):
        """
        This function scans the string s and returns a copy
        with all percent-encoded characters decoded. This
        function is the inverse of pct_encode(s).
        Only legal percent-encoded forms are decoded.
        Others raise an error.
        Decode a blank to logical ANY, and hyphen to logical NA.
        """

        if (s == ''):
            return CPE2_3_WFN.VALUE_ANY

        if (s == '-'):
            return CPE2_3_WFN.VALUE_NA

        # Start the scanning loop.
        # Normalize: convert all uppercase letters to lowercase first.
        s = s.lower()
        result = ""
        idx = 0
        embedded = False

        while (idx < len(s)):
            # Get the idx'th character of s
            c = s[idx, idx]

            # Deal with dot, hyphen and tilde: decode with quoting
            if ((c == '.') or (c == '-') or (c == '~')):
                result = "%s\\%s" % (result, c)
                idx = idx + 1
                embedded = True  # a non-%01 encountered
                continue

            if (c != '%'):
                result = "%s%s" % (result, c)
                idx = idx + 1
                embedded = True  # a non-%01 encountered
                continue

            # we get here if we have a substring starting w/ '%'.
            form = s[idx, idx + 2]  # get the three-char sequence

            if form == CPE2_3_WFN.PCE_ASTERISK:
                # If %01 legal at beginning or end
                # embedded is false, so must be preceded by %01
                # embedded is true, so must be followed by %01
                if (((idx == 0) or (idx == (len(s)-3))) or ((not embedded) and (s[idx - 3, idx - 1] == CPE2_3_WFN.PCE_ASTERISK)) or (embedded and (len(s) >= idx + 6) and (s[idx + 3, idx + 5] == CPE2_3_WFN.PCE_ASTERISK))):

                    # A percent-encoded question mark is found
                    # at the beginning or the end of the string,
                    # or embedded in sequence as required.
                    # Decode to unquoted form.
                    result = "%s?" % result
                    idx = idx + 3
                    continue
                else:
                    msg = "error"
                    raise ValueError(msg)
            elif form == CPE2_3_WFN.PCE_QUESTION:
                if ((idx == 0) or (idx == (len(s) - 3))):
                    # Percent-encoded asterisk is at the beginning
                    # or the end of the string, as required.
                    # Decode to unquoted form.
                    result = "%s*" % result
                else:
                    msg = "error"
                    raise ValueError(msg)
            elif form in CPE2_3_WFN.DECODE_DICT.keys():
                value = CPE2_3_WFN.DECODE_DICT[form]
                result = "%s%s" % (result, value)
            else:
                msg = "Error"
                raise ValueError(msg)

            idx = idx + 3
            embedded = True  # a non-%01 encountered.

        return result

    @classmethod
    def _transform_for_uri(cls, s):
        """
        Scans an input string s and applies the following transformations:
        - Pass alphanumeric characters thru untouched
        - Percent-encode quoted non-alphanumerics as needed
        - Unquoted special characters are mapped to their special forms.

        -TEST: Change some special characters
        >>> s = 'change\\too?and*'
        >>> CPE2_3_WFN._transform_for_uri(s)
        change\too%01and%02
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
                result += CPE2_3_WFN.PCE_ASTERISK

            # Bind the unquoted '*' special character to "%02"
            if (thischar == "*"):
                result += CPE2_3_WFN.PCE_QUESTION

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
    def _pack(self):
        """
        “Pack” the values of the five arguments into the single edition
        component. If all the values are blank, just return a blank.

        - TEST: full input
        >>> wfn = 'wfn:[part="a",vendor="hp",product="insight_diagnostics", version="7\.4\.0\.1570",update=ANY,edition=ANY, sw_edition="online",target_sw="win2003",target_hw="x64", other=ANY,language=ANY]'
        >>> cpe = CPE2_3_WFN(wfn)
        >>> cpe._pack()
        ~~online~win2003~x64~

        - TEST: an only value
        >>> wfn = 'wfn:[part="a",vendor="hp",product="openview_network_manager", version="7\.51",update=NA,edition=ANY,sw_edition=ANY, target_sw="linux",target_HW=ANY,other=ANY,language=ANY]'
        >>> cpe = CPE2_3_WFN(wfn)
        >>> cpe._pack()
        ~~~linux~~

        - TEST: without edition
        >>> wfn = 'wfn:[part="a",vendor="hp",product="openview_network_manager"]'
        >>> cpe = CPE2_3_WFN(wfn)
        >>> cpe._pack()
        ~~~~~
        """

        ed = CPE2_3_BASE._bind_value_for_uri(self.getEdition())
        sw_ed = CPE2_3_BASE._bind_value_for_uri(self.getSw_edition())
        t_sw = CPE2_3_BASE._bind_value_for_uri(self.getTarget_sw())
        t_hw = CPE2_3_BASE._bind_value_for_uri(self.getTarget_hw())
        oth = CPE2_3_BASE._bind_value_for_uri(self.getOther())

        if (sw_ed == "") and (t_sw == "") and (t_hw == "") and (oth == ""):
            # All the extended attributes are blank,
            # so don't do any packing, just return ed

            return ed

        # Otherwise, pack the five values into a single string
        # prefixed and internally delimited with the tilde
        return "~%s~%s~%s~%s~%s" % (ed, sw_ed, t_sw, t_hw, oth)

    @classmethod
    def _unpack(self, s):
        """
        Unpack its elements and set the attributes in wfn accordingly.
        Parse out the five elements.
        """

        components = s.split("~")

        ed = components[0]
        sw_ed = components[1]
        t_sw = components[2]
        t_hw = components[3]
        oth = components[4]

        self.set(CPE2_3_BASE.KEY_EDITION, CPE2_3_WFN._decode(ed))
        self.set(CPE2_3_BASE.KEY_SW_EDITION, CPE2_3_WFN._decode(sw_ed))
        self.set(CPE2_3_BASE.KEY_TARGET_SW, CPE2_3_WFN._decode(t_sw))
        self.set(CPE2_3_BASE.KEY_TARGET_HW, CPE2_3_WFN._decode(t_hw))
        self.set(CPE2_3_BASE.KEY_OTHER, CPE2_3_WFN._decode(oth))

    def bind_to_uri(self):
        """
        Converts the binding style WFN to URI 2.2 version
        and returns version 2.2 CPE object

        - TEST: Microsoft Internet Explorer 8.0.6001 Beta (any edition)
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.0\.6001", update="beta", edition=ANY]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_uri()
        cpe:/a:microsoft:internet_explorer:8.0.6001:beta

        - TEST: Microsoft Internet Explorer 8.* SP?
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.*", update="sp?"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_uri()
        cpe:/a:microsoft:internet_explorer:8.%02:sp%01

        - TEST: HP Insight Diagnostics 7.4.0.1570 Online Edition for Windows 2003 x64
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", update=NA, sw_edition="online", target_sw="win2003", target_hw="x64"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_uri()
        cpe:/a:hp:insight_diagnostics:7.4.0.1570:-:~~online~win2003~x64~

        - TEST: HP OpenView Network Manager 7.51 (any update) for Linux
        >>> wfn = 'wfn:[part="a", vendor="hp", product="openview_network_manager", version="7\.51", target_sw="linux"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_uri()
        cpe:/a:hp:openview_network_manager:7.51::~~~linux~~

        - TEST: Foo\Bar Big$Money Manager 2010 Special Edition for iPod Touch 80GB
        >>> wfn = 'wfn:[part="a", vendor="foo\\bar", product="big\$money_manager_2010", sw_edition="special", target_sw="ipod_touch", target_hw="80gb"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_uri()
        cpe:/a:foo%5cbar:big%24money_manager_2010:::~~special~ipod_touch~80gb~
        """

        uri = "cpe:/"

        for a in CPE2_3_BASE.uri_part_keys:
            if a == CPE2_3_BASE.KEY_EDITION:
                # Call the pack() helper function to compute the proper
                # binding for the edition element

                v = CPE2_3_BASE._pack()
            else:
                # Get the value for a in self, then bind to a string
                # for inclusion in the URI.

                v = CPE2_3_BASE._bind_value_for_uri(self.get(a))

            # Append v to the URI then add a colon.
            uri += "%s:" % v

        # Return the URI string, with trailing colons trimmed
        return CPE2_3_WFN._trim(uri)

    @classmethod
    def unbind_uri(cls, cpe2_2):
        """
        Returns an object WFN associated to binding style URI of
        input version 2.2 CPE object.

        The procedure for unbinding a URI is straightforward:
            1. Loop over the seven attributes corresponding to the seven
            CPE v2.2 components, performing steps 2 through 7.

            2. For URI components 1-5 and 7, decode the string and set the
            corresponding WFN attribute value. Decoding entails: converting
            sole "" to ANY, sole "-" to NA, adding quoting to embedded periods
            and hyphens, and decoding percent-encoded forms.

            3. The edition component is "unpacked" if a leading tilde indicates
            it contains a packed collection of five attribute values.

        - TEST: legacy edition and language attributes are unbound to the
          logical value ANY.
        >>> uri = 'cpe:/a:microsoft:internet_explorer:8.0.6001:beta'
        >>> cpe2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        >>> wfn.get_wfn_string()
        wfn:[part="a",vendor="microsoft",product="internet_explorer", version="8\.0\.6001",update="beta",edition=ANY, language=ANY]

        - TEST: two percent-encoded characters are unbound with added quoting.
          Although the percent-encoded characters are the same as the special
          characters, the added quoting blocks their interpretation in the WFN.
        >>> uri = 'cpe:/a:microsoft:internet_explorer:8.%2a:sp%3f'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        >>> wfn.get_wfn_string()
        wfn:[part="a",vendor="microsoft",product="internet_explorer", version="8\.\*",update="sp\?",edition=ANY,language=ANY]

        - TEST: two percent-encoded special characters are unbound without
          quoting
        >>> uri = 'cpe:/a:microsoft:internet_explorer:8.%02:sp%01'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        >>> wfn.get_wfn_string()
        wfn:[part="a",vendor="microsoft",product="internet_explorer", version="8\.*",update="sp?",edition=ANY,language=ANY]

        - TEST: legacy edition attribute as well as the four extended attributes
          are unpacked from the edition component of the URI
        >>> uri = 'cpe:/a:hp:insight_diagnostics:7.4.0.1570::~~online~win2003~x64~'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        >>> wfn.get_wfn_string()
        wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", update=ANY, edition=ANY, sw_edition="online", target_sw="win2003", target_hw="x64", other=ANY,language=ANY]

        - TEST: the lone hyphen in the update component is unbound to the
          logical value NA, and all the other blanks embedded in the packed
          edition component unbind to ANY, with only the target_sw attribute
          actually specified.
        >>> uri = 'cpe:/a:hp:openview_network_manager:7.51:-:~~~linux~'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        >>> wfn.get_wfn_string()
        wfn:[part="a",vendor="hp",product="openview_network_manager", version="7\.51",update=NA,edition=ANY,sw_edition=ANY, target_sw="linux",target_HW=ANY,other=ANY,language=ANY]

        - TEST: An error is raised when this URI is unbound, because it contains
          an illegal percent-encoded form, "%07".
        >>> uri = 'cpe:/a:foo%5cbar:big%24money_2010%07:::~~special~ipod_touch~80gb~'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        error

        - TEST: both the tildes (unencoded as well as percent-encoded) are
          handled: both are quoted in the WFN. The original v2.2 URI syntax
          allows tildes to appear without encoding, but the preferred URI syntax
          is for tildes to be encoded like any other printable non-alphanumeric
          character.
        >>> uri = 'cpe:/a:foo~bar:big%7emoney_2010'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        wfn:[part="a",vendor="foo\~bar",product="big\~money_2010", version=ANY,update=ANY,edition=ANY,language=ANY]

        - TEST: An error is raised when this URI is unbound, because it contains
          a special character ("%02") embedded within a value string.
        >>> uri = 'cpe:/a:foo:bar:12.%02.1234'
        >>> CPE2_2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2_2)
        error
        """

        # Initialize the empty WFN
        wfn = CPE2_3_WFN()

        for i in range(0, 7):
            # Get the i'th component of uri
            v = cpe2_2[i]
            comp_key = CPE2_3_BASE.uri_order_parts_dict[i]

            # Special handling for edition component
            if comp_key == CPE2_3_BASE.KEY_EDITION:

                # Unpack edition if needed
                if (v != "" and v != "-" and v[0:0] == "~"):

                    # We have five values packed together here
                    CPE2_3_WFN._unpack(v, wfn)

            #unbind the parsed string
            wfn.set(comp_key, CPE2_3_WFN._decode(v))

        return wfn

    @classmethod
    def _process_quoted_chars(cls, s):
        """
        Inspect each character in string s. Certain nonalpha
        characters pass thru without escaping into the result,
        but most retain escaping.
        """

        result = ""
        idx = 0
        while (idx < len(s)):
            c = s[idx, idx]  # get the idx'th character of s
        if c != "\\":
            # unquoted characters pass thru unharmed
            result = "%s%s" % (result, c)
        else:
            # Escaped characters are examined
            nextchr = s[idx + 1, idx + 1]

            if (nextchr == ".") or (nextchr == "-") or (nextchr == "_"):
                # the period, hyphen and underscore pass unharmed
                result = "%s%s" % (result, nextchr)
                idx = idx + 1
            else:
                # all others retain escaping
                result = "%s\\%s" % (result, nextchr)
                idx = idx + 2
                continue
            idx = idx + 1

        return result

    @classmethod
    def _bind_value_for_fs(cls, v):
        """
        Convert the value v to its proper string representation for
        insertion into the formatted string.
        """
        if v == CPE2_3_WFN.VALUE_ANY:
            return "*"
        elif v == CPE2_3_WFN.VALUE_NA:
            return "-"
        else:
            return CPE2_3_WFN._process_quoted_chars(v)

    def bind_to_fs(self):
        """
        Bind WFN (self) to formatted string.

        Converts the binding style WFN to formatted string
        and returns a formatted string object.

        - TEST: Microsoft Internet Explorer 8.0.6001 Beta (any edition). The
          unspecified attributes bind to “*” in the formatted string binding.
        >>> wfn = 'wfn:[part="a",vendor="microsoft",product="internet_explorer", version="8\.0\.6001",update="beta",edition=ANY]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*

        - TEST: Microsoft Internet Explorer 8.* SP? (any edition). The
          unspecified attributes default to ANY and are thus bound to “*”. Also
          note how the unquoted special characters in the WFN are carried over
          into the formatted string.
        >>> wfn = 'wfn:[part="a",vendor="microsoft",product="internet_explorer", version="8\.*",update="sp?",edition=ANY]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        cpe:2.3:a:microsoft:internet_explorer:8.*:sp?:*:*:*:*:*:*

        - TEST: HP Insight 7.4.0.1570 Online Edition for Windows 2003 x64. The
          NA binds to the lone hyphen, the unspecified edition, language and
          other all bind to the asterisk, and the extended attributes appear in
          their own fields.
        >>> wfn = 'wfn:[part="a",vendor="hp",product="insight", version="7\.4\.0\.1570",update=NA, sw_edition="online",target_sw="win2003",target_hw="x64"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        cpe:2.3:a:hp:insight:7.4.0.1570:-:*:*:online:win2003:x64:*

        - TEST: HP OpenView Network Manager 7.51 (any update) for Linux. The
          unspecified attributes update, edition, language, sw_edition,
          target_hw, and other each bind to an asterisk in the
          formatted string.
        >>> wfn = 'wfn:[part="a",vendor="hp",product="openview_network_manager", version="7\.51",target_sw="linux"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        cpe:2.3:a:hp:openview_network_manager:7.51:*:*:*:*:linux:*:*

        - TEST: Foo\Bar Big$Money 2010 Special Edition for iPod Touch 80GB. The
          \\ and \$ carry over into the binding, and all the other
          unspecified attributes bind to the asterisk.
        >>> wfn = 'wfn:[part="a",vendor="foo\\bar",product="big\$money_2010", sw_edition="special",target_sw="ipod_touch",target_hw="80gb"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        cpe:2.3:a:foo\\bar:big\$money_2010:*:*:*:*:special:ipod_touch:80gb:*
        """

        # Initialize the output with the CPE v2.3 string prefix.
        fs = "cpe:2.3:"

        for a in CPE2_3_WFN._wfn_part_keys:
            v = CPE2_3_WFN._bind_value_for_fs(self.get(a))
            fs = "%s%s" % (fs, v)

            # Add a colon except at the very end
            if (a != CPE2_3_WFN.KEY_OTHER):
                fs = "%s:" % fs

        return fs

    def unbind_fs(cls, fs):
        """
        The algorithm parses the eleven fields of the formatted string, then
        unbinds each string result. If a field contains only an asterisk, it is
        unbound to the logical value ANY. If a field contains only a hyphen, it
        is unbound to the logical value NA. Quoting of non-alphanumeric
        characters is restored as needed, but the two special characters
        (asterisk and question mark) are permitted to appear without a preceding
        escape character. The unbinding procedure performs limited error
        checking.

        - TEST: the periods in the version string are quoted in the WFN, and all
          the asterisks are unbound to the logical value ANY
        >>> uri = 'cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.0\.6001", update="beta", edition=ANY, language=ANY, sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]

        - TEST: the embedded special characters are unbound untouched in the WFN
        >>> uri = 'cpe:2.3:a:microsoft:internet_explorer:8.*:sp?:*:*:*:*:*:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.*", update="sp?", edition=ANY, language=ANY, sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]

        - TEST: the lone hyphen in the update field unbinds to the logical value
          NA, and the lone asterisks unbind to the logical value ANY
        >>> uri = 'cpe:2.3:a:hp:insight_diagnostics:7.4.0.1570:-:*:*:online:win2003:x64:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", update=NA, edition=ANY, language=ANY, sw_edition="online", target_sw="win2003", target_hw="x64", other=ANY]

        - TEST: This raises an error during unbinding, due to the embedded
          unquoted asterisk in the version attribute.
        >>> uri = 'cpe:2.3:a:hp:insight_diagnostics:7.4.*.1570:*:*:*:*:*:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        error

        - TEST: the quoted special characters retain their quoting in the WFN
        >>> uri = 'cpe:2.3:a:foo\\bar:big\$money:2010:*:*:*:special:ipod_touch:80gb:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        wfn:[part="a", vendor="foo\\bar", product="big\$money", version="2010", update=ANY, edition=ANY, language=ANY, sw_edition="special", target_sw="ipod_touch", target_hw="80gb", other=ANY]
        """

        # Initialize the empty WFN
        wfn = CPE2_3_WFN()

        # NB: the cpe scheme is the 0th component, the cpe version is the
        # 1st. So we start parsing at the 2nd component.
        for a in range(2, 12):
            v = fs[a]  # get the a'th field string
            v = CPE2_3_WFN._unbind_value_fs(v)  # unbind the string

            # set the value of the corresponding attribute
            att_key = CPE2_3_WFN._wfn_order_part_keys[a]
            wfn.set(CPE2_3_WFN._wfn_parts_dict[att_key], v)

        return wfn

    def _unbind_value_fs(cls, s):
        """
        Takes a string value s and returns the appropriate logical value
        if s is the bound form of a logical value.
        If s is some general value string,
        add quoting of non-alphanumerics as needed.
        """

        if s == "*":
            return CPE2_3_WFN.VALUE_ANY_VALUE
        elif s == "-":
            return CPE2_3_WFN.VALUE_NOT_APPLICABLE
        else:
            # add quoting to any unquoted non-alphanumeric characters,
            # but leave the two special characters alone,
            # as they may appear quoted or unquoted.
            return CPE2_3_WFN._add_quoting(s)

    def _add_quoting(cls, s):
        """
        Inspect each character in string s. Copy quoted characters,
        with their escaping, into the result. Look for unquoted non
        alphanumerics and if not "*" or "?", add escaping.
        """

        result = ""
        idx = 0
        embedded = False
        while (idx < len(s)):
            c = s[idx, idx]  # get the idx'th character of s
            if (CPE2_3_WFN._is_alphanum(c) or c == "_"):
                # Alphanumeric characters pass untouched
                result = "%s%s" % (result, c)
                idx = idx + 1
                embedded = True
                continue

            if c == "\\":
                # Anything quoted in the bound string stays quoted
                # in the unbound string.
                result = "%s%s" % (result, s[idx, idx + 1])
                idx = idx + 2
                embedded = True
                continue

            if (c == "*"):
                # An unquoted asterisk must appear at the beginning or
                # end of the string.
                if (idx == 0) or (idx == (len(s)-1)):
                    result = "%s%s" % (result, c)
                    idx = idx + 1
                    embedded = True
                    continue
            else:
                msg = "error"
                raise ValueError(msg)

            if (c == "?"):
                # An unquoted question mark must appear at the beginning or
                # end of the string, or in a leading or trailing sequence:
                # - ? legal at beginning or end
                # - embedded is false, so must be preceded by ?
                # - embedded is true, so must be followed by ?
                if (((idx == 0) or (idx == (len(s) - 1))) or ((not embedded) and (s[idx - 1, idx - 1] == "?")) or (embedded and (s[idx + 1, idx + 1] == "?"))):
                    result = "%s%s" % (result, c)
                    idx = idx + 1
                    embedded = False
                    continue
                else:
                    msg = "error"
                    raise ValueError(msg)

            # all other characters must be quoted
            result = "%s\\%s" % (result, c)
            idx = idx + 1
            embedded = True

        return result

    def convert_uri_to_fs(cls, uri):
        """
        Returns the CPE2_3_FS object associated with
        the input CPE2_3_URI object.

        Given a URI uri which conforms to the CPE v2.2 specification,
        the procedure for converting it to a formatted string has two steps:

        1. Unbind uri to WFN
        2. Bind WFN to formatted string
        """

        wfn = CPE2_3_WFN.unbind_uri(uri)
        fs = wfn.bind_to_fs()

        return fs

    def convert_fs_to_uri(cls, fs):
        """
        Returns the CPE2_3_URI object associated with
        the input CPE2_3_FS object.

        Given a formatted string fs, the procedure for converting it
        to a URI has two steps:

        1. Unbind formatted string to WFN
        2. Bind WFN to uri (CPE v2.2)
        """

        wfn = CPE2_3_WFN.unbind_fs(fs)
        uri = wfn.bind_to_uri()

        return uri

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
        type_value = self.cpe_dict[CPE2_3_BASE.KEY_PART]

        isHW = type_value == CPE2_3_BASE.KEY_PART_HW
        isEmpty = type_value == CPE2_3_WFN.VALUE_INT_NULL
        isAny = type_value == CPE2_3_WFN.VALUE_INT_ANY

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
        type_value = self.cpe_dict[CPE2_3_BASE.KEY_PART]

        isOS = type_value == CPE2_3_BASE.KEY_PART_OS
        isEmpty = type_value == CPE2_3_WFN.VALUE_INT_NULL
        isAny = type_value == CPE2_3_WFN.VALUE_INT_ANY

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
        type_value = self.cpe_dict[CPE2_3_BASE.KEY_PART]

        isApp = type_value == CPE2_3_BASE.KEY_PART_APP
        isEmpty = type_value == CPE2_3_WFN.VALUE_INT_NULL
        isAny = type_value == CPE2_3_WFN.VALUE_INT_ANY

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

        return self.cpe_dict[CPE2_3_BASE.KEY_PART]

    def getVendor(self):
        """
        Returns the vendor name of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getVendor()
        'microsoft'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_VENDOR]

    def getProduct(self):
        """
        Returns the product name of CPE ID.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getProduct()
        'windows'
        """

        return self.cpe_dict[CPE2_3_BASE.KEY_PRODUCT]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_VERSION]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_UPDATE]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_EDITION]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_LANGUAGE]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_SW_EDITION]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_TARGET_SW]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_TARGET_HW]

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

        return self.cpe_dict[CPE2_3_BASE.KEY_OTHER]

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

        eqPart = self.cpe_dict[CPE2_3_BASE.KEY_PART] == cpe.getType()
        eqVendor = self.cpe_dict[CPE2_3_BASE.KEY_VENDOR] == cpe.getVendor()
        eqProduct = self.cpe_dict[CPE2_3_BASE.KEY_PRODUCT] == cpe.getProduct()
        eqVersion = self.cpe_dict[CPE2_3_BASE.KEY_VERSION] == cpe.getVersion()
        eqUpdate = self.cpe_dict[CPE2_3_BASE.KEY_UPDATE] == cpe.getUpdate()
        eqEdition = self.cpe_dict[CPE2_3_BASE.KEY_EDITION] == cpe.getEdition()
        eqLanguage = self.cpe_dict[CPE2_3_BASE.KEY_LANGUAGE] == cpe.getLanguage()
        eqSw_edition = self.cpe_dict[CPE2_3_BASE.KEY_SW_EDITION] == cpe.getSw_edition()
        eqTarget_sw = self.cpe_dict[CPE2_3_BASE.KEY_TARGET_SW] == cpe.getTarget_sw()
        eqTarget_hw = self.cpe_dict[CPE2_3_BASE.KEY_TARGET_HW] == cpe.getTarget_hw()
        eqOther = self.cpe_dict[CPE2_3_BASE.KEY_OTHER] == cpe.getOther()

        return (eqPart and eqVendor and eqProduct and eqVersion and
                eqUpdate and eqEdition and eqLanguage and eqSw_edition and
                eqTarget_sw and eqTarget_hw and eqOther)


if __name__ == "__main__":
    #wfn = 'wfn:[]'
    wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.0\.6001", update="beta", edition=ANY]'

    ce = CPE2_3_WFN(wfn)
    print("")
    print(ce)
    print("Elements: %s") % len(ce)
    print("")
    print("IS HARDWARE: %s") % ce.isHardware()
    print("IS OS: %s") % ce.isOperatingSystem()
    print("IS APPLICATION: %s") % ce.isApplication()
    print("")
    print("VENDOR: %s") % ce.getVendor()
    print("PRODUCT: %s") % ce.getProduct()
    print("VERSION: %s") % ce.getVersion()
    print("UPDATE: %s") % ce.getUpdate()
    print("EDITION: %s") % ce.getEdition()
    print("LANGUAGE: %s") % ce.getLanguage()
    print("")

#    import doctest
#    doctest.testmod()
