#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is an implementation of name matching
algorithm in accordance with version 2.3 of CPE (Common Platform
Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
"""

from .cpe2_3 import CPE2_3
from .cpe2_3_wfn import CPE2_3_WFN
from .comp.cpecomp import CPEComponent
from .comp.cpecomp2_3_wfn import CPEComponent2_3_WFN
from .cpeset import CPESet


class CPESet2_3(CPESet):
    """
    Represents a set of CPEs.

    This class allows:

    - create set of CPE elements.
    - match a CPE element against a set of CPE elements.
    """

    ###############
    #  CONSTANTS  #
    ###############

    # Possible set relations between a source WFN and a target WFN:
    # - The source is a SUPERSET of the target
    # - The source is a SUBSET of the target
    # - The source and target are EQUAL
    # - The source and target are mutually exclusive or DISJOINT
    # - The target has wild cards and the result is undefined
    LOGICAL_VALUE_SUPERSET = 1
    LOGICAL_VALUE_SUBSET = 2
    LOGICAL_VALUE_EQUAL = 3
    LOGICAL_VALUE_DISJOINT = 4
    LOGICAL_VALUE_UNDEFINED = 5

    # Version of CPE set
    VERSION = "2.3"

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _compare(cls, source, target):
        """
        Compares two values associated with a attribute of two WFNs,
        which may be logical values (ANY or NA) or string values.

        :param string source: First attribute value
        :param string target: Second attribute value
        :returns: The attribute comparison relation.
        :rtype: int

        This function is a support function for compare_WFNs.
        """

        if (CPESet2_3._is_string(source)):
            source = source.lower()
        if (CPESet2_3._is_string(target)):
            target = target.lower()

        # In this specification, unquoted wildcard characters in the target
        # yield an undefined result

        if (CPESet2_3._is_string(target) and
           CPESet2_3._contains_wildcards(target)):
            return CPESet2_3.LOGICAL_VALUE_UNDEFINED

        # If source and target attribute values are equal,
        # then the result is EQUAL
        if (source == target):
            return CPESet2_3.LOGICAL_VALUE_EQUAL

        # If source attribute value is ANY, then the result is SUPERSET
        if (source == CPEComponent2_3_WFN.VALUE_ANY):
            return CPESet2_3.LOGICAL_VALUE_SUPERSET

        # If target attribute value is ANY, then the result is SUBSET
        if (target == CPEComponent2_3_WFN.VALUE_ANY):
            return CPESet2_3.LOGICAL_VALUE_SUBSET

        # If either source or target attribute value is NA
        # then the result is DISJOINT
        isSourceNA = source == CPEComponent2_3_WFN.VALUE_NA
        isTargetNA = target == CPEComponent2_3_WFN.VALUE_NA

        if (isSourceNA or isTargetNA):
            return CPESet2_3.LOGICAL_VALUE_DISJOINT

        # If we get to this point, we are comparing two strings
        return CPESet2_3._compare_strings(source, target)

    @classmethod
    def _compare_strings(cls, source, target):
        """
        Compares a source string to a target string,
        and addresses the condition in which the source string
        includes unquoted special characters.

        It performs a simple regular expression match,
        with the assumption that (as required) unquoted special characters
        appear only at the beginning and/or the end of the source string.

        It also properly differentiates between unquoted and quoted
        special characters.

        :param string source: First string value
        :param string target: Second string value
        :returns: The comparison relation among input strings.
        :rtype: int
        """

        start = 0
        end = len(source)
        begins = 0
        ends = 0

        # Reading of initial wildcard in source
        if source.startswith(CPEComponent2_3_WFN.WILDCARD_MULTI):
            # Source starts with "*"
            start = 1
            begins = -1
        else:
            while ((start < len(source)) and
                   source.startswith(CPEComponent2_3_WFN.WILDCARD_ONE,
                                     start, start)):
                # Source starts with one or more "?"
                start += 1
                begins += 1

        # Reading of final wildcard in source
        if (source.endswith(CPEComponent2_3_WFN.WILDCARD_MULTI) and
           CPESet2_3._is_even_wildcards(source, end - 1)):

            # Source ends in "*"
            end -= 1
            ends = -1
        else:
            while ((end > 0) and
                   source.endswith(CPEComponent2_3_WFN.WILDCARD_ONE, end - 1, end) and
                   CPESet2_3._is_even_wildcards(source, end - 1)):

                # Source ends in "?"
                end -= 1
                ends += 1

        source = source[start: end]
        index = -1
        leftover = len(target)

        while (leftover > 0):
            index = target.find(source, index + 1)
            if (index == -1):
                break
            escapes = target.count("\\", 0, index)
            if ((index > 0) and (begins != -1) and
               (begins < (index - escapes))):

                break

            escapes = target.count("\\", index + 1, len(target))
            leftover = len(target) - index - escapes - len(source)
            if ((leftover > 0) and ((ends != -1) and (leftover > ends))):
                continue

            return CPESet2_3.LOGICAL_VALUE_SUPERSET

        return CPESet2_3.LOGICAL_VALUE_DISJOINT

    @classmethod
    def _contains_wildcards(cls, s):
        """
        Return True if the string contains any unquoted special characters
        (question-mark or asterisk), otherwise False.

        Ex: _contains_wildcards("foo") => FALSE
        Ex: _contains_wildcards("foo\?") => FALSE
        Ex: _contains_wildcards("foo?") => TRUE
        Ex: _contains_wildcards("\*bar") => FALSE
        Ex: _contains_wildcards("*bar") => TRUE

        :param string s: string to check
        :returns: True if string contains any unquoted special characters,
            False otherwise.
        :rtype: boolean

        This function is a support function for _compare().
        """

        idx = s.find("*")
        if idx != -1:
            if idx == 0:
                return True
            else:
                if s[idx - 1] != "\\":
                    return True

        idx = s.find("?")
        if idx != -1:
            if idx == 0:
                return True
            else:
                if s[idx - 1] != "\\":
                    return True
        return False

    @classmethod
    def _is_even_wildcards(cls, str, idx):
        """
        Returns True if an even number of escape (backslash) characters
        precede the character at index idx in string str.

        :param string str: string to check
        :returns: True if an even number of escape characters precede
            the character at index idx in string str, False otherwise.
        :rtype: boolean
        """

        result = 0
        while ((idx > 0) and (str[idx - 1] == "\\")):
            idx -= 1
            result += 1

        isEvenNumber = (result % 2) == 0
        return isEvenNumber

    @classmethod
    def _is_string(cls, arg):
        """
        Return True if arg is a string value,
        and False if arg is a logical value (ANY or NA).

        :param string arg: string to check
        :returns: True if value is a string, False if it is a logical value.
        :rtype: boolean

        This function is a support function for _compare().
        """

        isAny = arg == CPEComponent2_3_WFN.VALUE_ANY
        isNa = arg == CPEComponent2_3_WFN.VALUE_NA

        return not (isAny or isNa)

    @classmethod
    def compare_wfns(cls, source, target):
        """
        Compares two WFNs and returns a generator of pairwise attribute-value
        comparison results. It provides full access to the individual
        comparison results to enable use-case specific implementations
        of novel name-comparison algorithms.

        Compare each attribute of the Source WFN to the Target WFN:

        :param CPE2_3_WFN source: first WFN CPE Name
        :param CPE2_3_WFN target: seconds WFN CPE Name
        :returns: generator of pairwise attribute comparison results
        :rtype: generator
        """

        # Compare results using the get() function in WFN
        for att in CPEComponent.CPE_COMP_KEYS_EXTENDED:
            value_src = source.get_attribute_values(att)[0]
            if value_src.find('"') > -1:
                # Not a logical value: del double quotes
                value_src = value_src[1:-1]

            value_tar = target.get_attribute_values(att)[0]
            if value_tar.find('"') > -1:
                # Not a logical value: del double quotes
                value_tar = value_tar[1:-1]

            yield (att, CPESet2_3._compare(value_src, value_tar))

    @classmethod
    def cpe_disjoint(cls, source, target):
        """
        Compares two WFNs and returns True if the set-theoretic relation
        between the names is DISJOINT.

        :param CPE2_3_WFN source: first WFN CPE Name
        :param CPE2_3_WFN target: seconds WFN CPE Name
        :returns: True if the set relation between source and target
            is DISJOINT, otherwise False.
        :rtype: boolean
        """

        # If any pairwise comparison returned DISJOINT  then
        # the overall name relationship is DISJOINT
        for att, result in CPESet2_3.compare_wfns(source, target):
            isDisjoint = result == CPESet2_3.LOGICAL_VALUE_DISJOINT
            if isDisjoint:
                return True
        return False

    @classmethod
    def cpe_equal(cls, source, target):
        """
        Compares two WFNs and returns True if the set-theoretic relation
        between the names is EQUAL.

        :param CPE2_3_WFN source: first WFN CPE Name
        :param CPE2_3_WFN target: seconds WFN CPE Name
        :returns: True if the set relation between source and target
            is EQUAL, otherwise False.
        :rtype: boolean
        """

        # If any pairwise comparison returned EQUAL then
        # the overall name relationship is EQUAL
        for att, result in CPESet2_3.compare_wfns(source, target):
            isEqual = result == CPESet2_3.LOGICAL_VALUE_EQUAL
            if not isEqual:
                return False
        return True

    @classmethod
    def cpe_subset(cls, source, target):
        """
        Compares two WFNs and returns True if the set-theoretic relation
        between the names is (non-proper) SUBSET.

        :param CPE2_3_WFN source: first WFN CPE Name
        :param CPE2_3_WFN target: seconds WFN CPE Name
        :returns: True if the set relation between source and target
            is SUBSET, otherwise False.
        :rtype: boolean
        """

        # If any pairwise comparison returned something other than SUBSET
        # or EQUAL, then SUBSET is False.
        for att, result in CPESet2_3.compare_wfns(source, target):
            isSubset = result == CPESet2_3.LOGICAL_VALUE_SUBSET
            isEqual = result == CPESet2_3.LOGICAL_VALUE_EQUAL
            if (not isSubset) and (not isEqual):
                return False
        return True

    @classmethod
    def cpe_superset(cls, source, target):
        """
        Compares two WFNs and returns True if the set-theoretic relation
        between the names is (non-proper) SUPERSET.

        :param CPE2_3_WFN source: first WFN CPE Name
        :param CPE2_3_WFN target: seconds WFN CPE Name
        :returns: True if the set relation between source and target
            is SUPERSET, otherwise False.
        :rtype: boolean
        """

        # If any pairwise comparison returned something other than SUPERSET
        # or EQUAL, then SUPERSET is False.
        for att, result in CPESet2_3.compare_wfns(source, target):
            isSuperset = result == CPESet2_3.LOGICAL_VALUE_SUPERSET
            isEqual = result == CPESet2_3.LOGICAL_VALUE_EQUAL
            if (not isSuperset) and (not isEqual):
                return False

        return True

    ####################
    #  OBJECT METHODS  #
    ####################

    def append(self, cpe):
        """
        Adds a CPE element to the set if not already.
        Only WFN CPE Names are valid, so this function converts the input CPE
        object of version 2.3 to WFN style.

        :param CPE cpe: CPE Name to store in set
        :returns: None
        :exception: ValueError - invalid version of CPE Name
        """

        if cpe.VERSION != CPE2_3.VERSION:
            errmsg = "CPE Name version {0} not valid, version 2.3 expected".format(
                cpe.version)
            raise ValueError(errmsg)

        for k in self.K:
            if cpe._str == k._str:
                return None

        if isinstance(cpe, CPE2_3_WFN):
            self.K.append(cpe)
        else:
            # Convert the CPE Name to WFN
            wfn = CPE2_3_WFN(cpe.as_wfn())
            self.K.append(wfn)

    def name_match(self, wfn):
        """
        Accepts a set of CPE Names K and a candidate CPE Name X. It returns
        'True' if X matches any member of K, and 'False' otherwise.

        :param CPESet self: A set of m known CPE Names K = {K1, K2, …, Km}.
        :param CPE cpe: A candidate CPE Name X.
        :returns: True if X matches K, otherwise False.
        :rtype: boolean
        """

        for N in self.K:
            if CPESet2_3.cpe_superset(wfn, N):
                return True
        return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpeset2_3.txt")
