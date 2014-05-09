#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of cpe package.

This module is an implementation of CPE language matching
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

from .cpeset2_3 import CPESet2_3
from .cpelang import CPELanguage
from .cpe2_3_wfn import CPE2_3_WFN
from .cpe2_3_uri import CPE2_3_URI
from .cpe2_3_fs import CPE2_3_FS


class CPELanguage2_3(CPELanguage):
    """
    Represents an expression in the CPE Language.

    This class allows match a CPE element against an expression
    in the CPE Language, that is, a XML document format for binding
    descriptive prose and diagnostic test to a CPE name
    (CPE Description Format).
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Version of CPE Language
    VERSION = "2.3"

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _fact_ref_eval(cls, cpeset, wfn):
        """
        Returns True if wfn is a non-proper superset (True superset
        or equal to) any of the names in cpeset, otherwise False.

        :param CPESet cpeset: list of CPE bound Names.
        :param CPE2_3_WFN wfn: WFN CPE Name.
        :returns: True if wfn is a non-proper superset any of the names in cpeset, otherwise False
        :rtype: boolean
        """

        for n in cpeset:
            # Need to convert each n from bound form to WFN
            if (CPESet2_3.cpe_superset(wfn, n)):
                return True

        return False

    @classmethod
    def _check_fact_ref_eval(cls, cpel_dom):
        """
        Returns the result (True, False, Error) of performing the specified
        check, unless the check isnt supported, in which case it returns
        False. Error is a catch-all for all results other than True and
        False.

        :param string cpel_dom: XML infoset for the check_fact_ref element.
        :returns: result of performing the specified check
        :rtype: boolean or error
        """

        CHECK_SYSTEM = "check-system"
        CHECK_LOCATION = "check-location"
        CHECK_ID = "check-id"

        checksystemID = cpel_dom.getAttribute(CHECK_SYSTEM)
        if (checksystemID == "http://oval.mitre.org/XMLSchema/ovaldefinitions-5"):
            # Perform an OVAL check.
            # First attribute is the URI of an OVAL definitions file.
            # Second attribute is an OVAL definition ID.
            return CPELanguage2_3._ovalcheck(cpel_dom.getAttribute(CHECK_LOCATION),
                                             cpel_dom.getAttribute(CHECK_ID))

        if (checksystemID == "http://scap.nist.gov/schema/ocil/2"):
            # Perform an OCIL check.
            # First attribute is the URI of an OCIL questionnaire file.
            # Second attribute is OCIL questionnaire ID.
            return CPELanguage2_3._ocilcheck(cpel_dom.getAttribute(CHECK_LOCATION),
                                             cpel_dom.getAttribute(CHECK_ID))

        # Can add additional check systems here, with each returning a
        # True, False, or Error value
        return False

    @classmethod
    def _ocilcheck(location, ocil_id):
        """
        Perform an OCIL check.

        :param string location: URI of an OCIL questionnaire file
        :param string ocil_id: OCIL questionnaire ID
        :rtype: boolean
        :exception: NotImplementedError - Method not implemented
        """

        errmsg = "Method not implemented"
        raise NotImplementedError(errmsg)

    @classmethod
    def _ovalcheck(location, oval_id):
        """
        Perform an OVAL check.

        :param string location: URI of an OVAL definitions file
        :param string oval_id: OVAL definition ID
        :rtype: boolean
        :exception: NotImplementedError - Method not implemented
        """

        errmsg = "Method not implemented"
        raise NotImplementedError(errmsg)

    @classmethod
    def _unbind(cls, boundname):
        """
        Unbinds a bound form to a WFN.

        :param string boundname: CPE name
        :returns: WFN object associated with boundname.
        :rtype: CPE2_3_WFN
        """

        try:
            fs = CPE2_3_FS(boundname)
        except:
            # CPE name is not formatted string
            try:
                uri = CPE2_3_URI(boundname)
            except:
                # CPE name is not URI but WFN
                return CPE2_3_WFN(boundname)
            else:
                return CPE2_3_WFN(uri.as_wfn())
        else:
            return CPE2_3_WFN(fs.as_wfn())

    ####################
    #  OBJECT METHODS  #
    ####################

    def language_match(self, cpeset, cpel_dom=None):
        """
        Accepts a set of known CPE Names and an expression in the CPE language,
        and delivers the answer True if the expression matches with the set.
        Otherwise, it returns False.

        :param CPELanguage self: An expression in the CPE Applicability
            Language, represented as the XML infoset for the platform element.
        :param CPESet cpeset: CPE set object to match with self expression.
        :param string cpel_dom: An expression in the CPE Applicability
            Language, represented as DOM tree.
        :returns: True if self expression can be satisfied by language matching
            against cpeset, False otherwise.
        :rtype: boolean
        """

        # Root element tag
        TAG_ROOT = '#document'
        # A container for child platform definitions
        TAG_PLATSPEC = 'cpe:platform-specification'

        # Information about a platform definition
        TAG_PLATFORM = 'cpe:platform'
        TAG_LOGITEST = 'cpe:logical-test'
        TAG_CPE = 'cpe:fact-ref'
        TAG_CHECK_CPE = 'check-fact-ref'

        # Tag attributes
        ATT_NAME = 'name'
        ATT_OP = 'operator'
        ATT_NEGATE = 'negate'

        # Attribute values
        ATT_OP_AND = 'AND'
        ATT_OP_OR = 'OR'
        ATT_NEGATE_TRUE = 'TRUE'

        # Constant associated with an error in language matching
        ERROR = 2

        if cpel_dom is None:
            cpel_dom = self.document

        # Identify the root element
        if cpel_dom.nodeName == TAG_ROOT or cpel_dom.nodeName == TAG_PLATSPEC:
            for node in cpel_dom.childNodes:
                if node.nodeName == TAG_PLATSPEC:
                    return self.language_match(cpeset, node)
                if node.nodeName == TAG_PLATFORM:
                    return self.language_match(cpeset, node)

        # Identify a platform element
        elif cpel_dom.nodeName == TAG_PLATFORM:
            # Parse through E's elements and ignore all but logical-test
            for node in cpel_dom.childNodes:
                if node.nodeName == TAG_LOGITEST:
                    # Call the function again, but with logical-test
                    # as the root element
                    return self.language_match(cpeset, node)

        # Identify a CPE element
        elif cpel_dom.nodeName == TAG_CPE:
            # fact-ref's name attribute is a bound name,
            # so we unbind it to a WFN before passing it
            cpename = cpel_dom.getAttribute(ATT_NAME)
            wfn = CPELanguage2_3._unbind(cpename)
            return CPELanguage2_3._fact_ref_eval(cpeset, wfn)

        # Identify a check of CPE names (OVAL, OCIL...)
        elif cpel_dom.nodeName == TAG_CHECK_CPE:
            return CPELanguage2_3._check_fact_ref_Eval(cpel_dom)

        # Identify a logical operator element
        elif cpel_dom.nodeName == TAG_LOGITEST:
            count = 0
            len = 0
            answer = False

            for node in cpel_dom.childNodes:
                if node.nodeName.find("#") == 0:
                    continue
                len = len + 1
                result = self.language_match(cpeset, node)
                if result:
                    count = count + 1
                elif result == ERROR:
                    answer = ERROR

            operator = cpel_dom.getAttribute(ATT_OP).upper()

            if operator == ATT_OP_AND:
                if count == len:
                    answer = True
            elif operator == ATT_OP_OR:
                if count > 0:
                    answer = True

            operator_not = cpel_dom.getAttribute(ATT_NEGATE)
            if operator_not:
                if ((operator_not.upper() == ATT_NEGATE_TRUE) and
                   (answer != ERROR)):
                    answer = not answer

            return answer
        else:
            return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpelang2_3.txt")
