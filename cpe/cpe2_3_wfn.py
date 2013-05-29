#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpe2_3_wfn.py
Author: Alejandro Galindo
Date: 16-05-2013
Description: Module for the treatment of identifiers in accordance with
             Well-Formed Name (WFN) of version 2.3 of CPE
             (Common Platform Enumeration) specification.
"""


from cpe2_3 import CPE2_3
from cpe2_3_fs import CPE2_3_FS
from cpe2_3_uri import CPE2_3_URI

import re


class CPE2_3_WFN(CPE2_3):
    r"""
    Implementation of WFN of version 2.3 of CPE specification.

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

    - TEST: bad WFN
    >>> wfn = 'baduri'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: WFN prefix not found

    - TEST: an empty CPE.
    >>> wfn = 'wfn:[]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an empty CPE with bad part name
    >>> wfn = 'wfn:[bad="hw"]'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: attribute name 'bad' not valid

    - TEST: an operating system CPE
    >>> wfn = 'wfn:[part="o", vendor="acme", product="producto", version="1\.0", update="update2", edition="pro", language="en-us"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an application CPE
    >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.444\.0\.1570", sw_edition="online", target_sw="windows_2003", target_hw="x64", language=ANY, other=NA]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an application CPE
    >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: an CPE with special characters
    >>> wfn = 'wfn:[part="h", vendor="hp", product="insight\diagnostics", version="8.0~"]'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: product value is invalid

    - TEST: An unquoted question mark MAY be used at the beginning
    and/or the end of an attribute-value string
    >>> wfn = 'wfn:[part="a", vendor="hp", product="?insight_diagnostics?", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: A contiguous sequence of unquoted question marks MAY appear
     at the beginning and/or the end of an attribute-value string
    >>> wfn = 'wfn:[part="a", vendor="???hp???", product="?insight_diagnostics?", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: Unquoted question marks and asterisks MAY appear
    in the same attribute-value string
    >>> wfn = 'wfn:[part="a", vendor="???hp*", product="?insight_diagnostics?", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn) # doctest: +ELLIPSIS
    <__main__.CPE2_3_WFN object at 0x...>

    - TEST: An unquoted question mark SHALL NOT be used
    in any other place in an attribute-value string
    >>> wfn = 'wfn:[part="a", vendor="h??p", product="?insight_diagnostics?", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
    >>> CPE2_3_WFN(wfn)
    Traceback (most recent call last):
    ValueError: Malformed CPE name: vendor value is invalid
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Logical values in integer format
    _VALUE_INT_NULL = 0
    _VALUE_INT_ANY = 1
    _VALUE_INT_NA = 2

    # Logical values in string format
    VALUE_NULL = ""
    VALUE_ANY_VALUE = "ANY"
    VALUE_NOT_APPLICABLE = "NA"

    # Constant associated with wildcard to indicate a sequence of characters
    WILDCARD_MULTI = "*"
    # Constant associated with wildcard to indicate a character
    WILDCARD_ONE = "?"

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

    ###############
    #  VARIABLES  #
    ###############

    _int_to_string_logical_dict = {
        _VALUE_INT_NULL: VALUE_ANY_VALUE,
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
    def _is_valid_wfn_value(cls, str_value):
        """
        Return True if the input value of WFN attribute distinct of
        "language" is valid, and otherwise False.

        - TEST: invalid value
        >>> val = 'insight_?diagnostics'
        >>> CPE2_3_WFN._is_valid_wfn_value(val)
        False

        - TEST: valid valua
        >>> val = '8\.*'
        >>> CPE2_3_WFN._is_valid_wfn_value(val)
        True

        - TEST: valid value
        >>> val = '?es?'
        >>> CPE2_3_WFN._is_valid_wfn_value(val)
        True

        - TEST: special values
        >>> val = '\?\*'
        >>> CPE2_3_WFN._is_valid_wfn_value(val)
        True
        """

        # Checks value not equal than a dash
        if str_value == ("-") or str_value == ("\-"):
            return False

        # Compilation of regular expression associated with value of CPE part
        quest = "\%s" % CPE2_3_FS.WILDCARD_ONE
        asterisk = "\%s" % CPE2_3_FS.WILDCARD_MULTI
        unreserved = "\w"
        special = "%s|%s" % (quest, asterisk)
        spec_chrs = "%s+|%s" % (quest, asterisk)
        punc = "\!|\"|\;|\#|\$|\%|\&|\'|\(|\)|\+|\,|\.|\/|\:|\<|\=|\>|\@|\[|\]|\^|\`|\{|\||\}|\~|\-"
        quoted = r"\\(\\" + "|%s|%s)" % (special, punc)
        avstring = "%s|%s" % (unreserved, quoted)
        value_string_pattern = "^(%s+|%s*(%s)+|%s(%s)+)(%s)?$" % (quest,
                                                                  quest, avstring,
                                                                  asterisk, avstring,
                                                                  spec_chrs)

        part_value_rxc = re.compile(value_string_pattern)
        return part_value_rxc.match(str_value) is not None

    @classmethod
    def _is_valid_wfn_language(cls, str_value):
        """
        Return True if the input value of WFN attribute "language" is valid,
        and otherwise False.

        - TEST
        >>> val = 'es-ES'
        >>> CPE2_3_WFN._is_valid_wfn_language(val)
        True

        - TEST
        >>> val = 'es-noesES'
        >>> CPE2_3_WFN._is_valid_wfn_language(val)
        False

        - TEST
        >>> val = 'esES'
        >>> CPE2_3_WFN._is_valid_wfn_language(val)
        False
        """

        # Compilation of regular expression associated with value of CPE part
        region = "([%s]{2}|[%s]{3})" % (CPE2_3._ALPHA, CPE2_3._DIGIT)
        language = "[%s]{2,3}" % CPE2_3._ALPHA
        LANGTAG = "%s(\-%s)?" % (language, region)

        value_lang_pattern = "^%s$" % LANGTAG

        lang_value_rxc = re.compile(value_lang_pattern)

        return lang_value_rxc.match(str_value) is not None

    @classmethod
    def _get_str_value_dict(cls, v):
        """
        Returns the textual logical value associated with the value v.
        If v is not a logical value it returns v.
        """

        result = v

        if v in CPE2_3_WFN._int_to_string_logical_dict:
            result = CPE2_3_WFN._int_to_string_logical_dict[v]

        return result

    @classmethod
    def _get_int_value_dict(cls, v):
        """
        Returns the internal logical value associated with the value v.
        If v is not a logical value it returns v.
        """

        result = v

        if v in CPE2_3_WFN._string_to_int_logical_dict:
            result = CPE2_3_WFN._string_to_int_logical_dict[v]

        return result

    @classmethod
    def _trim(cls, s):
        """
        Remove trailing colons from the URI back to the first non-colon.

        - TEST: trailing colons necessary
        >>> s = '1:2::::'
        >>> CPE2_3_WFN._trim(s)
        '1:2'

        - TEST: trailing colons not necessary
        >>> s = '1:2:3:4:5:6'
        >>> CPE2_3_WFN._trim(s)
        '1:2:3:4:5:6'
        """
        reverse = s[::-1]
        idx = 0
        for i in range(0, len(reverse)):
            if reverse[i] == ":":
                idx += 1
            else:
                break

        # Return the substring after all trailing colons,
        # reversed back to its original character order.
        new_s = reverse[idx: len(reverse)]
        return new_s[::-1]

    @classmethod
    def _is_alphanum(cls, c):
        """
        Returns True if c is an uppercase letter, a lowercase letter,
        a digit, or the underscore, otherwise False.

        - TEST: alpha
        >>> c = 'A'
        >>> CPE2_3_WFN._is_alphanum(c)
        True

        - TEST: num
        >>> c = '2'
        >>> CPE2_3_WFN._is_alphanum(c)
        True

        - TEST: char is _
        >>> c = '_'
        >>> CPE2_3_WFN._is_alphanum(c)
        True

        - TEST: char not valid
        >>> c = 'Ç'
        >>> CPE2_3_WFN._is_alphanum(c)
        False
        """

        alphanum_pattern = "\w"
        alphanum_rxc = re.compile(alphanum_pattern)

        return (alphanum_rxc.match(c) is not None)

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
            return CPE2_3_WFN.VALUE_ANY_VALUE

        if (s == '-'):
            return CPE2_3_WFN.VALUE_NOT_APPLICABLE

        # Start the scanning loop.
        # Normalize: convert all uppercase letters to lowercase first.
        s = s.lower()
        result = ""
        idx = 0
        embedded = False

        while (idx < len(s)):
            # Get the idx'th character of s
            c = s[idx]

            # Deal with dot, hyphen and tilde: decode with quoting
            if ((c == '.') or (c == '-') or (c == '~')):
                result = "%s\\%s" % (result, c)
                idx += 1
                embedded = True  # a non-%01 encountered
                continue

            if (c != '%'):
                result = "%s%s" % (result, c)
                idx += 1
                embedded = True  # a non-%01 encountered
                continue

            # we get here if we have a substring starting w/ '%'.
            form = s[idx: idx + 3]  # get the three-char sequence

            if form == CPE2_3_WFN.PCE_QUESTION:
                # If %01 legal at beginning or end
                # embedded is false, so must be preceded by %01
                # embedded is true, so must be followed by %01
                if (((idx == 0) or (idx == (len(s)-3))) or ((not embedded) and (s[idx - 3, idx - 1] == CPE2_3_WFN.PCE_ASTERISK)) or (embedded and (len(s) >= idx + 6) and (s[idx + 3, idx + 5] == CPE2_3_WFN.PCE_ASTERISK))):

                    # A percent-encoded question mark is found
                    # at the beginning or the end of the string,
                    # or embedded in sequence as required.
                    # Decode to unquoted form.
                    result = "%s%s" % (result, CPE2_3_WFN.WILDCARD_ONE)
                    idx += 3
                    continue
                else:
                    msg = "error"
                    raise ValueError(msg)
            elif form == CPE2_3_WFN.PCE_ASTERISK:
                if ((idx == 0) or (idx == (len(s) - 3))):
                    # Percent-encoded asterisk is at the beginning
                    # or the end of the string, as required.
                    # Decode to unquoted form.
                    result = "%s%s" % (result, CPE2_3_WFN.WILDCARD_MULTI)
                else:
                    msg = "error"
                    raise ValueError(msg)
            elif form in CPE2_3_WFN.DECODE_DICT.keys():
                value = CPE2_3_WFN.DECODE_DICT[form]
                result = "%s%s" % (result, value)
            else:
                msg = "Percent-encoded character '%s' not valid" % s
                raise ValueError(msg)

            idx += 3
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
        >>> s = 'change\\~too?and*'
        >>> CPE2_3_WFN._transform_for_uri(s)
        'change%7etoo%01and%02'
        """

        result = ""
        idx = 0
        while (idx < len(s)):
            thischar = s[idx]  # get the idx'th character of s

            # alphanumerics (incl. underscore) pass untouched
            if (CPE2_3_WFN._is_alphanum(thischar)):
                result += thischar
                idx += 1
                continue

            # escape character
            if (thischar == "\\"):
                idx += 1
                nxtchar = s[idx]
                result += CPE2_3_WFN._pct_encode(nxtchar)
                idx += 1
                continue

            # Bind the unquoted '?' special character to "%01"
            if (thischar == CPE2_3_WFN.WILDCARD_ONE):
                result += CPE2_3_WFN.PCE_QUESTION

            # Bind the unquoted '*' special character to "%02"
            if (thischar == CPE2_3_WFN.WILDCARD_MULTI):
                result += CPE2_3_WFN.PCE_ASTERISK

            idx += 1

        return result

    @classmethod
    def _bind_value_for_uri(cls, s):
        """
        Takes a string s and converts it to the proper string for
        inclusion in a CPE v2.2-conformant URI. The logical value ANY
        binds to the blank in the 2.2-conformant URI.

        - TEST
        >>> s = "ANY"
        >>> CPE2_3_WFN._bind_value_for_uri(s)
        ''

        - TEST
        >>> s = "NA"
        >>> CPE2_3_WFN._bind_value_for_uri(s)
        '-'

        - TEST
        >>> s = "hola"
        >>> CPE2_3_WFN._bind_value_for_uri(s)
        'hola'
        """

        if s == CPE2_3_WFN.VALUE_ANY_VALUE:
            return ""

        # The value NA binds to a single hyphen
        if s == CPE2_3_WFN.VALUE_NOT_APPLICABLE:
            return "-"

        # s is a string value
        return CPE2_3_WFN._transform_for_uri(s)

    @classmethod
    def _process_quoted_chars(cls, s):
        r"""
        Inspect each character in string s. Certain nonalpha
        characters pass thru without escaping into the result,
        but most retain escaping.

        - TEST:
        >>> s = "ho\\la"
        >>> CPE2_3_WFN._process_quoted_chars(s)
        'ho\\la'

        - TEST:
        >>> s = "\."
        >>> CPE2_3_WFN._process_quoted_chars(s)
        '.'
        """

        result = ""
        idx = 0
        while (idx < len(s)):

            c = s[idx]  # get the idx'th character of s
            if c != "\\":
                # unquoted characters pass thru unharmed
                result = "%s%s" % (result, c)
            else:
                # Escaped characters are examined
                nextchr = s[idx + 1]

                if (nextchr == ".") or (nextchr == "-") or (nextchr == "_"):
                    # the period, hyphen and underscore pass unharmed
                    result = "%s%s" % (result, nextchr)
                    idx += 1
                else:
                    # all others retain escaping
                    result = "%s\\%s" % (result, nextchr)
                    idx += 2
                    continue
            idx += 1

        return result

    @classmethod
    def _bind_value_for_fs(cls, v):
        """
        Convert the value v to its proper string representation for
        insertion into the formatted string.
        """

        if (v == CPE2_3_WFN.VALUE_ANY_VALUE or v == CPE2_3_WFN.VALUE_NULL):
            return "*"
        elif v == CPE2_3_WFN.VALUE_NOT_APPLICABLE:
            return "-"
        else:
            return CPE2_3_WFN._process_quoted_chars(v)

    @classmethod
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

    @classmethod
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
            c = s[idx]  # get the idx'th character of s
            if (CPE2_3_WFN._is_alphanum(c) or c == "_"):
                # Alphanumeric characters pass untouched
                result = "%s%s" % (result, c)
                idx += 1
                embedded = True
                continue

            if c == "\\":
                # Anything quoted in the bound string stays quoted
                # in the unbound string.
                result = "%s%s" % (result, s[idx: idx + 2])
                idx += 2
                embedded = True
                continue

            if (c == CPE2_3_WFN.WILDCARD_MULTI):
                # An unquoted asterisk must appear at the beginning or
                # end of the string.
                if (idx == 0) or (idx == (len(s) - 1)):
                    result = "%s%s" % (result, c)
                    idx += 1
                    embedded = True
                    continue
                else:
                    msg = "Character '%s' not valid" % c
                    raise ValueError(msg)

            if (c == CPE2_3_WFN.WILDCARD_ONE):
                # An unquoted question mark must appear at the beginning or
                # end of the string, or in a leading or trailing sequence:
                # - ? legal at beginning or end
                # - embedded is false, so must be preceded by ?
                # - embedded is true, so must be followed by ?
                if (((idx == 0) or (idx == (len(s) - 1))) or ((not embedded) and (s[idx - 1] == CPE2_3_WFN.WILDCARD_ONE)) or (embedded and (s[idx + 1] == CPE2_3_WFN.WILDCARD_ONE))):
                    result = "%s%s" % (result, c)
                    idx += 1
                    embedded = False
                    continue
                else:
                    msg = "Character '%s' not valid" % c
                    raise ValueError(msg)

            # all other characters must be quoted
            result = r"%s\%s" % (result, c)
            idx += 1
            embedded = True

        return result

    @classmethod
    def unbind_uri(cls, cpe_uri):
        r"""
        Unbinds a URI binding uri to a WFN. Returns an object WFN
        associated to binding style URI of input version 2.2 CPE object.

        Input is URI binding.
        Output is WFN.

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
        >>> cpe2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\\.0\\.6001", update="beta", edition=ANY, language=ANY]'

        - TEST: two percent-encoded characters are unbound with added quoting.
          Although the percent-encoded characters are the same as the special
          characters, the added quoting blocks their interpretation in the WFN.
        >>> uri = 'cpe:/a:microsoft:internet_explorer:8.%2a:sp%3f'
        >>> cpe2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\\.\\*", update="sp\\?", edition=ANY, language=ANY]'

        - TEST: two percent-encoded special characters are unbound without
          quoting
        >>> uri = 'cpe:/a:microsoft:internet_explorer:8.%02:sp%01'
        >>> cpe2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\\.*", update="sp?", edition=ANY, language=ANY]'

        - TEST: legacy edition attribute as well as the four extended attributes
          are unpacked from the edition component of the URI
        >>> uri = 'cpe:/a:hp:insight_diagnostics:7.4.01.1570::~~online~win2003~x64~'
        >>> cpe2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\\.4\\.01\\.1570", update=ANY, edition=ANY, language=ANY, sw_edition="online", target_sw="win2003", target_hw="x64", other=ANY]'

        - TEST: the lone hyphen in the update component is unbound to the
          logical value NA, and all the other blanks embedded in the packed
          edition component unbind to ANY, with only the target_sw attribute
          actually specified.
        >>> uri = 'cpe:/a:hp:openview_network_manager:7.51:-:%7b%7b%7blinux%7b'
        >>> cpe2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="hp", product="openview_network_manager", version="7\\.51", update=NA, edition="\\{\\{\\{linux\\{", language=ANY]'

        - TEST: both the tildes (unencoded as well as percent-encoded) are
          handled: both are quoted in the WFN. The original v2.2 URI syntax
          allows tildes to appear without encoding, but the preferred URI syntax
          is for tildes to be encoded like any other printable non-alphanumeric
          character.
        >>> uri = 'cpe:/a:foo%7ebar:big%7emoney_2010'
        >>> cpe2 = CPE2_3_URI(uri)
        >>> wfn = CPE2_3_WFN.unbind_uri(cpe2)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="foo\\~bar", product="big\\~money_2010", version=ANY, update=ANY, edition=ANY, language=ANY]'
        """

        # Initialize the empty WFN
        wfn = CPE2_3_WFN()

        for i in range(0, 7):
            # Get the i'th component of uri
            v = cpe_uri[i]
            comp_key = CPE2_3.wfn_ordered_part_dict[i]

            if v is None:
                # Attribute without value
                wfn.set_value(comp_key, CPE2_3_WFN.VALUE_ANY_VALUE)
            else:
                # Attribute with value
                # Special handling for edition component
                if comp_key == CPE2_3.KEY_EDITION:
                    # Unpack edition if needed
                    if (v == "" or v == "-" or v[0] != "~"):
                        #unbind the parsed string
                        wfn.set_value(comp_key, CPE2_3_WFN._decode(v))
                    else:
                        # We have five values packed together here
                        wfn._unpack(v)
                else:
                    #unbind the parsed string
                    wfn.set_value(comp_key, CPE2_3_WFN._decode(v))

        return wfn

    @classmethod
    def unbind_fs(cls, cpe_fs):
        r"""
        Unbinds a formatted string fs to a WFN.

        Input is formatted string.
        Output is WFN.

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
        >>> uri = 'cpe:2.3:a:microsoft:internet_explorer:8.0.6003:beta:*:*:*:*:*:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\\.0\\.6003", update="beta", edition=ANY, language=ANY, sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]'

        - TEST: the embedded special characters are unbound untouched in the WFN
        >>> uri = 'cpe:2.3:a:microsoft:internet_explorer:8.*:sp?:*:*:*:*:*:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\\.*", update="sp?", edition=ANY, language=ANY, sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]'

        - TEST: the lone hyphen in the update field unbinds to the logical value
          NA, and the lone asterisks unbind to the logical value ANY
        >>> uri = 'cpe:2.3:a:hp:insight_diagnostics:7.4.0.1570:-:*:*:online:win2003:x64:*'
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\\.4\\.0\\.1570", update=NA, edition=ANY, language=ANY, sw_edition="online", target_sw="win2003", target_hw="x64", other=ANY]'

        - TEST: the quoted special characters retain their quoting in the WFN
        >>> uri = r"cpe:2.3:a:foo\\bar:big\$money:2010:*:*:*:special:ipod_touch:80gb:*"
        >>> fs = CPE2_3_FS(uri)
        >>> wfn = CPE2_3_WFN.unbind_fs(fs)
        >>> wfn.get_wfn_string()
        'wfn:[part="a", vendor="foo\\\\bar", product="big\\$money", version="2010", update=ANY, edition=ANY, language=ANY, sw_edition="special", target_sw="ipod_touch", target_hw="80gb", other=ANY]'
        """

        # Initialize the empty WFN
        wfn = CPE2_3_WFN()

        # The cpe scheme is the 0th component, the cpe version is the
        # 1st. So we start parsing at the 2nd component.
        for a in range(0, 11):
            v = cpe_fs[a]  # get the a'th field string
            v = CPE2_3_WFN._unbind_value_fs(v)  # unbind the string

            # set the value of the corresponding attribute
            att_key = CPE2_3.wfn_ordered_part_dict[a]
            wfn.set_value(att_key, v)

        return wfn

    @classmethod
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

    @classmethod
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

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, cpe_str="wfn:[]"):
        """
        Checks that input CPE name string is valid according to binding
        style Well-Formed Name (WFN) and, if so, stores the component
        in a dictionary.
        """

        CPE2_3.__init__(self, cpe_str)
        CPE2_3_WFN.style = CPE2_3.STYLE_WFN
        self._validate()

    def __len__(self):
        """
        Returns the number of parts of CPE name.

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
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", sw_edition="online", target_sw="windows_2003", target_hw="x64", language=ANY, other=NA]'
        >>> c = CPE2_3_WFN(wfn)
        >>> len(c)
        9
        """

        count = 0
        for k, v in self._cpe_dict.iteritems():
            if v != CPE2_3_WFN._VALUE_INT_NULL:
                count += 1

        return count

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE name as a string.

        - TEST: existing item
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c[0] == 'a'
        True

        - TEST: existing item
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="8\.*", sw_edition="?", target_sw=ANY, target_hw="x32"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c[6] == "x32"
        True

        - TEST: not existing valid item
        >>> wfn = 'wfn:[part="h", vendor="hp", product=ANY, version=NA, target_hw="x32"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c[4]
        'x32'

        - TEST: not valid item
        >>> wfn = 'wfn:[part="h", vendor="hp", product=ANY, version=NA, target_hw="x32"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c[10]
        Traceback (most recent call last):
        KeyError: 'index not exists. Possible values: 0-4'
        """

        total_elems = self.__len__()
        if i >= total_elems:
            max_index = total_elems - 1
            msg = "Index not exists. Possible values: 0-%s" % max_index
            raise KeyError(msg)

        keys = CPE2_3.wfn_ordered_part_dict.keys()
        count = 0

        for idx in range(0, len(keys)):
            part_key = CPE2_3.wfn_ordered_part_dict[idx]
            value = CPE2_3_WFN._get_str_value_dict(self._cpe_dict[part_key])

            if value != CPE2_3_WFN.VALUE_NULL:
                if count == i:
                    # Found elem
                    break
                else:
                    # Count not null element
                    count += 1

        return value

    def __eq__(self, cpe):
        """
        Return True if "cpe" is equal to self object.

        - TEST: equals
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", language="es-es"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c == c
        True

        - TEST: not equals
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", language="es-es"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> wfn2 = 'wfn:[part="a", vendor="microsoft"]'
        >>> c2 = CPE2_3_WFN(wfn2)
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
        Checks CPE name with WFN style is valid.
        """

        # #####################
        #  CHECK CPE NAME PARTS
        # #####################

        # Check prefix and initial bracket of WFN
        if self.str[0:5] != "wfn:[":
            msg = "Malformed CPE name: WFN prefix not found"
            raise ValueError(msg)

        # Check final backet
        if self.str[-1:] != "]":
            msg = "Malformed CPE name: final bracket of WFN not found"
            raise ValueError(msg)

        content = self.str[5:-1]

        if content != "":
            # Split WFN in components
            list_component = content.split(", ")

            for e in list_component:
                # Whitespace not valid in component names and values
                if e.find(" ") != -1:
                    msg = "Malformed CPE name: WFN with too many whitespaces"
                    raise ValueError(msg)

                # Split pair attribute-value
                pair = e.split("=")
                att_name = pair[0]
                att_value = pair[1]

                # Check valid attribute name
                if att_name not in CPE2_3_WFN.wfn_part_keys:
                    msg = "Malformed CPE name: attribute name '%s' not valid" % att_name
                    raise ValueError(msg)

                # Check valid attribute value
                # "e" is used instead of "att_value" to retain the difference between
                # double quotes and logical values
                if not (att_value.startswith('"') and att_value.endswith('"')):
                    # Logical value
                    if (att_value == CPE2_3_WFN.VALUE_ANY_VALUE.lower()):
                        att_value = CPE2_3_WFN._VALUE_INT_ANY
                    elif (att_value == CPE2_3_WFN.VALUE_NOT_APPLICABLE.lower()):
                        att_value = CPE2_3_WFN._VALUE_INT_NA
                    else:
                        msg = "Malformed CPE name: logical value %s is invalid" % att_value
                        raise ValueError(msg)

                elif att_value.startswith('"') and att_value.endswith('"'):
                    # String value

                    # Del double quotes
                    att_value = att_value[1:-1]

                    if att_name == CPE2_3.KEY_PART:
                        # Check part (system type) value
                        part_pattern = "^(h|o|a)$"
                        part_rxc = re.compile(part_pattern)
                        part_match = part_rxc.match(att_value)

                        if part_match is None:
                            msg = "Malformed CPE name: part value '%s' is invalid" % att_value
                            raise ValueError(msg)

                    # Check language value
                    if att_name == CPE2_3.KEY_LANGUAGE:
                        if not CPE2_3_WFN._is_valid_wfn_language(att_value):
                            msg = "Malformed CPE name: language value is invalid"
                            raise ValueError(msg)
                    else:
                        if not CPE2_3_WFN._is_valid_wfn_value(att_value):
                            msg = "Malformed CPE name: %s value is invalid " % att_name
                            raise ValueError(msg)
                else:
                    # Bad value
                    msg = "Malformed CPE name: %s value is invalid" % att_name
                    raise ValueError(msg)

                if att_name in self._cpe_dict:
                    # Duplicate attribute
                    msg = "Malformed CPE name: %s attribute repeated" % att_name
                    raise ValueError(msg)

                self._cpe_dict[att_name] = att_value

        # Sets attributes unfilled
        for i, name in CPE2_3.wfn_ordered_part_dict.iteritems():
            if name not in self._cpe_dict:
                self._cpe_dict[name] = CPE2_3_WFN._VALUE_INT_NULL

        return self._cpe_dict

    def _pack(self):
        """
        “Pack” the values of the five arguments into the single edition
        component. If all the values are blank, just return a blank.

        - TEST: full input
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", update=ANY, edition=ANY, sw_edition="online", target_sw="win2003", target_hw="x64", other=ANY, language=ANY]'
        >>> cpe = CPE2_3_WFN(wfn)
        >>> cpe._pack()
        '~~online~win2003~x64~'

        - TEST: an only value
        >>> wfn = 'wfn:[part="a", vendor="hp", product="openview_network_manager", version="7\.51", update=NA, edition=ANY, sw_edition=ANY, target_sw="linux", target_HW=ANY, other=ANY, language=ANY]'
        >>> cpe = CPE2_3_WFN(wfn)
        >>> cpe._pack()
        '~~~linux~~'

        - TEST: without edition
        >>> wfn = 'wfn:[part="a", vendor="hp", product="openview_network_manager"]'
        >>> cpe = CPE2_3_WFN(wfn)
        >>> cpe._pack()
        ''
        """

        ed = CPE2_3_WFN._bind_value_for_uri(self.getEdition())
        sw_ed = CPE2_3_WFN._bind_value_for_uri(self.getSw_edition())
        t_sw = CPE2_3_WFN._bind_value_for_uri(self.getTarget_sw())
        t_hw = CPE2_3_WFN._bind_value_for_uri(self.getTarget_hw())
        oth = CPE2_3_WFN._bind_value_for_uri(self.getOther())

        if (sw_ed == "") and (t_sw == "") and (t_hw == "") and (oth == ""):
            # All the extended attributes are blank,
            # so don't do any packing, just return ed

            return ed

        # Otherwise, pack the five values into a single string
        # prefixed and internally delimited with the tilde
        return "~%s~%s~%s~%s~%s" % (ed, sw_ed, t_sw, t_hw, oth)

    def _unpack(self, s):
        """
        Unpack its elements and set the attributes in wfn accordingly.
        Parse out the five elements.
        ~ edition ~ software edition ~ target sw ~ target hw ~ other
        """

        components = s.split("~")

        ed = components[1]
        sw_ed = components[2]
        t_sw = components[3]
        t_hw = components[4]
        oth = components[5]

        self.set_value(CPE2_3.KEY_EDITION, CPE2_3_WFN._decode(ed))
        self.set_value(CPE2_3.KEY_SW_EDITION, CPE2_3_WFN._decode(sw_ed))
        self.set_value(CPE2_3.KEY_TARGET_SW, CPE2_3_WFN._decode(t_sw))
        self.set_value(CPE2_3.KEY_TARGET_HW, CPE2_3_WFN._decode(t_hw))
        self.set_value(CPE2_3.KEY_OTHER, CPE2_3_WFN._decode(oth))

    def get_value(self, att):
        """
        Takes two arguments, a WFN (self) and an attribute att,
        and returns the value of att.
        If the attribute att is unspecified in self, returns the
        default value ANY.
        """

        if att in self._cpe_dict.keys():
            value = CPE2_3_WFN._get_str_value_dict(self._cpe_dict[att])
            return value
        else:
            # Attribute not valid
            msg = "WFN attribute '%s' not valid" % att
            raise ValueError(msg)

    def set_value(self, att, value):
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
            if att == CPE2_3_WFN.KEY_LANGUAGE:
                if not CPE2_3_WFN._is_valid_wfn_language(value):
                    msg = "Value '%s' of attribute '%s' not valid" % (value, att)
                    raise ValueError(msg)
            else:
                if not CPE2_3_WFN._is_valid_wfn_value(value):
                    msg = "Value '%s' of attribute '%s' not valid" % (value, att)
                    raise ValueError(msg)

        # Correct value
        if att in self._cpe_dict.keys():
            if value is None:
                # Del attribute
                value = CPE2_3_WFN.VALUE_NULL

            # Replace value
            self._cpe_dict[att] = CPE2_3_WFN._get_int_value_dict(value)
        else:
            msg = "Attribute '%s' not valid" % att
            raise ValueError(msg)

        return self.get_wfn_string()

    def get_wfn_string(self):
        """
        Returns the WFN of CPE name in string.
        """

        wfn = "wfn:["
        for i, k in CPE2_3.wfn_ordered_part_dict.iteritems():
            if k in self._cpe_dict.keys():
                v = self._cpe_dict[k]
                if v != CPE2_3_WFN._VALUE_INT_NULL:
                    wfn += k
                    wfn += "="
                    if v in CPE2_3_WFN._int_to_string_logical_dict:
                        wfn += '%s, ' % CPE2_3_WFN._get_str_value_dict(v)
                    else:
                        wfn += '"%s", ' % v

        wfn = wfn[0:len(wfn)-2]
        wfn += "]"

        return wfn

    def bind_to_uri(self):
        """
        Converts the binding style WFN to URI 2.2 version
        and returns version 2.2 CPE object

        - TEST: Microsoft Internet Explorer 8.0.6001 Beta (any edition)
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.0\.6001", update="beta", edition=ANY]'
        >>> w1 = CPE2_3_WFN(wfn)
        >>> w1.bind_to_uri()
        'cpe:/a:microsoft:internet_explorer:8.0.6001:beta'

        - TEST: Microsoft Internet Explorer 8.* SP?
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.*", update="sp?"]'
        >>> w2 = CPE2_3_WFN(wfn)
        >>> w2.bind_to_uri()
        'cpe:/a:microsoft:internet_explorer:8.%02:sp%01'

        - TEST: HP Insight Diagnostics 7.4.0.1570 Online Edition for Windows 2003 x64
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight_diagnostics", version="7\.4\.0\.1570", update=NA, sw_edition="online", target_sw="win2003", target_hw="x64"]'
        >>> w3 = CPE2_3_WFN(wfn)
        >>> w3.bind_to_uri()
        'cpe:/a:hp:insight_diagnostics:7.4.0.1570:-:~~online~win2003~x64~'

        - TEST: HP OpenView Network Manager 7.51 (any update) for Linux
        >>> wfn = 'wfn:[part="a", vendor="hp", product="openview_network_manager", version="7\.51", target_sw="linux"]'
        >>> w4 = CPE2_3_WFN(wfn)
        >>> w4.bind_to_uri()
        'cpe:/a:hp:openview_network_manager:7.51::~~~linux~~'

        - TEST: Foo\Bar Big$Money Manager 2010 Special Edition for iPod Touch 80GB
        >>> wfn = 'wfn:[part="a", vendor="foobar", product="big\$money_manager_2010", sw_edition="special", target_sw="ipod_touch", target_hw="80gb"]'
        >>> w5 = CPE2_3_WFN(wfn)
        >>> w5.bind_to_uri()
        'cpe:/a:foobar:big%24money_manager_2010:::~~special~ipod_touch~80gb~'
        """

        uri = "cpe:/"

        for a in CPE2_3.uri_part_keys:
            if a == CPE2_3.KEY_EDITION:
                # Call the pack() helper function to compute the proper
                # binding for the edition element

                v = self._pack()
            else:
                # Get the value for a in self, then bind to a string
                # for inclusion in the URI.

                v = CPE2_3_WFN._bind_value_for_uri(self.get_value(a))

            # Append v to the URI then add a colon.
            uri += "%s:" % v

        # Return the URI string, with trailing colons trimmed
        return CPE2_3_WFN._trim(uri)

    def bind_to_fs(self):
        """
        Bind WFN (self) to formatted string.

        Converts the binding style WFN to formatted string
        and returns a formatted string object.

        - TEST: Microsoft Internet Explorer 8.0.6001 Beta (any edition). The
          unspecified attributes bind to “*” in the formatted string binding.
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.0\.6001", update="beta", edition=ANY]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        'cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*'

        - TEST: Microsoft Internet Explorer 8.* SP? (any edition). The
          unspecified attributes default to ANY and are thus bound to “*”. Also
          note how the unquoted special characters in the WFN are carried over
          into the formatted string.
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="8\.*", update="sp?", edition=ANY]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        'cpe:2.3:a:microsoft:internet_explorer:8.*:sp?:*:*:*:*:*:*'

        - TEST: HP Insight 7.4.0.1570 Online Edition for Windows 2003 x64. The
          NA binds to the lone hyphen, the unspecified edition, language and
          other all bind to the asterisk, and the extended attributes appear in
          their own fields.
        >>> wfn = 'wfn:[part="a", vendor="hp", product="insight", version="7\.7\.0\.1570", update=NA, sw_edition="online", target_sw="win2003", target_hw="x64"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        'cpe:2.3:a:hp:insight:7.7.0.1570:-:*:*:online:win2003:x64:*'

        - TEST: HP OpenView Network Manager 7.51 (any update) for Linux. The
          unspecified attributes update, edition, language, sw_edition,
          target_hw, and other each bind to an asterisk in the
          formatted string.
        >>> wfn = 'wfn:[part="a", vendor="hp", product="openview_network_manager", version="7\.51", target_sw="linux"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        'cpe:2.3:a:hp:openview_network_manager:7.51:*:*:*:*:linux:*:*'

        - TEST: Foo\Bar Big$Money 2010 Special Edition for iPod Touch 80GB. The
          \\ and \$ carry over into the binding, and all the other
          unspecified attributes bind to the asterisk.
        >>> wfn = 'wfn:[part="a", vendor="foobar", product="big\$money_2010", sw_edition="special", target_sw="ipod_touch", target_hw="80gb"]'
        >>> w = CPE2_3_WFN(wfn)
        >>> w.bind_to_fs()
        'cpe:2.3:a:foobar:big\\\\$money_2010:*:*:*:*:special:ipod_touch:80gb:*'
        """

        # Initialize the output with the CPE v2.3 string prefix.
        fs = "cpe:2.3:"

        for k, att in CPE2_3.wfn_ordered_part_dict.iteritems():
            if att in CPE2_3_WFN.wfn_part_keys:
                value = CPE2_3_WFN._bind_value_for_fs(self.get_value(att))
                fs = "%s%s" % (fs, value)

                # Add a colon except at the very end
                if (att != CPE2_3_WFN.KEY_OTHER):
                    fs = "%s:" % fs

        return fs

    def isHardware(self):
        """
        Returns True if CPE name corresponds to hardware elem.

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

        # Value of part of CPE name
        part_value = self.getPart()

        isHW = part_value == CPE2_3.VALUE_PART_HW
        isEmpty = part_value == CPE2_3_WFN.VALUE_NULL
        isAny = part_value == CPE2_3_WFN.VALUE_ANY_VALUE

        return (isHW or isEmpty or isAny)

    def isOperatingSystem(self):
        """
        Returns True if CPE name corresponds to operating system elem.

        - TEST: is not OS
        >>> wfn = 'wfn:[part="h"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isOperatingSystem() == False
        True

        - TEST: is OS
        >>> wfn = 'wfn:[part="o"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isOperatingSystem() == True
        True

        - TEST: is not OS
        >>> wfn = 'wfn:[part="a"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isOperatingSystem() == False
        True
        """

        # Value of part type of CPE name
        part_value = self.getPart()

        isOS = part_value == CPE2_3.VALUE_PART_OS
        isEmpty = part_value == CPE2_3_WFN.VALUE_NULL
        isAny = part_value == CPE2_3_WFN.VALUE_ANY_VALUE

        return (isOS or isEmpty or isAny)

    def isApplication(self):
        """
        Returns True if CPE name corresponds to application elem.

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
        >>> wfn = 'wfn:[]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.isApplication()
        True
        """

        # Value of part type of CPE name
        part_value = self.getPart()

        isApp = part_value == CPE2_3.VALUE_PART_APP
        isEmpty = part_value == CPE2_3_WFN.VALUE_NULL
        isAny = part_value == CPE2_3_WFN.VALUE_ANY_VALUE

        return (isApp or isEmpty or isAny)

    def getPart(self):
        """
        Returns the part type of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getPart()
        'a'

        - TEST: is operating system
        >>> wfn = 'wfn:[part="o"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getPart()
        'o'

        - TEST: is hardware
        >>> wfn = 'wfn:[]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getPart()
        ''
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_PART])

    def getVendor(self):
        """
        Returns the vendor name of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getVendor()
        'microsoft'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_VENDOR])

    def getProduct(self):
        """
        Returns the product name of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product="windows"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getProduct()
        'windows'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_PRODUCT])

    def getVersion(self):
        """
        Returns the version of product of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getVersion()
        '8\\\\.0'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_VERSION])

    def getUpdate(self):
        """
        Returns the update or service pack information of CPE name.

        - TEST: is operating system
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getUpdate()
        'sp2'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_UPDATE])

    def getEdition(self):
        """
        Returns the edition of product of CPE name.

        - TEST: is operating system
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", edition="pro"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getEdition()
        'pro'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_EDITION])

    def getLanguage(self):
        """
        Returns the internationalization information of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", language="es-es"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getLanguage()
        'es-es'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_LANGUAGE])

    def getSw_edition(self):
        """
        Returns the software edition of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", sw_edition="home"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getSw_edition()
        'home'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_SW_EDITION])

    def getTarget_sw(self):
        """
        Returns the software computing environment of CPE name
        within which the product operates.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", target_sw=NA]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getTarget_sw()
        'NA'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_TARGET_SW])

    def getTarget_hw(self):
        """
        Returns the arquitecture of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", target_hw="x64"]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getTarget_hw()
        'x64'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_TARGET_HW])

    def getOther(self):
        """
        Returns the other information part of CPE name.

        - TEST: is application
        >>> wfn = 'wfn:[part="a", vendor="microsoft", product=ANY, version="8\.0", update="sp2", other=NA]'
        >>> c = CPE2_3_WFN(wfn)
        >>> c.getOther()
        'NA'
        """

        return CPE2_3_WFN._get_str_value_dict(self._cpe_dict[CPE2_3.KEY_OTHER])


if __name__ == "__main__":

    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
