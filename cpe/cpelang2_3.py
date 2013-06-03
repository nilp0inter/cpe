#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cpelang2_3.py
Author: Alejandro Galindo
Date: 27-05-2013
Description: Implementation of CPE Applicability Language matching algorithm
             in accordance with version 2.3 of specification CPE
             (Common Platform Enumeration).

             This class allows:
             - match a CPE element against an expression in the CPE Language,
             that is, a XML document format for binding descriptive prose and
             diagnostic test to a CPE Name (CPE Description Format).
"""


from cpe2_3 import CPE2_3
from cpeset2_3 import CPESet2_3
from cpe2_3_wfn import CPE2_3_WFN
from cpe2_3_uri import CPE2_3_URI
from cpe2_3_fs import CPE2_3_FS

from xml.dom import minidom


class CPELanguage2_3(object):
    """
    Represents an expression in the CPE Language.
    """

    ###################
    #  CLASS METHODS  #
    ###################

    @classmethod
    def _fact_ref_eval(cls, cpeset, wfn):
        """
        Input argument wfn is WFN.
        Input argument cpeset is a list of CPE bound names.

        Returns True if wfn is a non-proper superset (True superset
        or equal to) any of the names in cpeset, otherwise False.
        """

        for n in cpeset:
            # Need to convert each n from bound form to WFN
            if (CPESet2_3.cpe_superset(wfn, CPELanguage2_3._unbind(n.cpe_str))):
                return True

        return False

    @classmethod
    def _check_fact_ref_eval(cls, cpel_dom):

        CHECK_SYSTEM = "check-system"
        CHECK_LOCATION = "check-location"
        CHECK_ID = "check-id"

        checksystemID = cpel_dom.getAttribute(CHECK_SYSTEM)
        if (checksystemID == "http://oval.mitre.org/XMLSchema/ovaldefinitions-5"):
            # Perform an OVAL check.
            # First attribute is the URI of an OVAL definitions file.
            # Second attribute is an OVAL definition ID.
            return CPELanguage2_3.ovalcheck(cpel_dom.getAttribute(CHECK_LOCATION),
                                            cpel_dom.getAttribute(CHECK_ID))

        if (checksystemID == "http://scap.nist.gov/schema/ocil/2"):
            # Perform an OCIL check.
            # First attribute is the URI of an OCIL questionnaire file.
            # Second attribute is OCIL questionnaire ID.
            return CPELanguage2_3.ocilcheck(cpel_dom.getAttribute(CHECK_LOCATION),
                                            cpel_dom.getAttribute(CHECK_ID))

        # Can add additional check systems here, with each returning a
        # True, False, or Error value
        return False

    @classmethod
    def _unbind(cls, boundname):
        """
        Unbinds a bound form to a WFN.

        Input is a CPE name as string
        Output WFN object associated with boundname.
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
                return CPE2_3_WFN.unbind_uri(uri)
        else:
            return CPE2_3_WFN.unbind_fs(fs)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __init__(self, expression, isFile=False):
        """
        Create an object that contains the input expression in
        the CPE Language (a set of CPE Names) and
        the DOM tree asociated with expression.

        Input:
            - expression: XML content in string or a path to XML file
            - isFile: indicates whether expression is a XML file or
                      XML content string
        """

        if isFile:
            self.expression = ""
            self.path = expression

            # Parse an XML file by name (filepath)
            self.document = minidom.parse(self.expression)
        else:
            self.expression = expression
            self.path = ""

            # Parse an XML stored in a string
            self.document = minidom.parseString(self.expression)

    def __unicode__(self):
        """
        Print CPE name as string.
        """

        return self.expression

    def language_match(self, cpeset, cpel_dom=None):
        r"""
        Accepts a set of known CPE Names and an expression in the CPE language,
        and delivers the answer 'true' if the expression matches with the set.
        Otherwise, it returns 'false'.

        Inputs:
            - self: An expression in the CPE Applicability Language,
                    represented as the XML infoset for the platform element.
            - cpeset: CPE set object to match with self expression.
            - cpel_dom: An expression in the CPE Applicability Language,
                        represented as DOM tree.
        Output:
            - True if self expression can be satisfied by language matching
              against cpeset, False otherwise.

        - TEST: not matching (there are undefined values)
        >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform id="123"><cpe:title>Sun Solaris 5.8 or 5.9 with BEA Weblogic 8.1 installed</cpe:title><cpe:logical-test operator="AND" negate="FALSE"><cpe:logical-test operator="OR" negate="FALSE"><cpe:fact-ref name="cpe:2.3:o:sun:solaris:5.8:*:*:*:*:*:*:*" /><cpe:fact-ref name="cpe:2.3:o:sun:solaris:5.9:*:*:*:*:*:*:*" /></cpe:logical-test><cpe:fact-ref name="cpe:2.3:a:bea:weblogic:8.1:*:*:*:*:*:*:*" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

        >>> c1 = CPE2_3_FS('cpe:2.3:o:sun:solaris:5.9:*:*:*:*:*:*:*')
        >>> c2 = CPE2_3_FS('cpe:2.3:a:bea:weblogic:8.*:*:*:*:*:*:*:*')

        >>> s = CPESet2_3()
        >>> s.append(CPE2_3_WFN.unbind_fs(c1))
        >>> s.append(CPE2_3_WFN.unbind_fs(c2))

        >>> l = CPELanguage2_3(document)
        >>> l.language_match(s)
        False

        - TEST: matching
        >>> document = '''<?xml version="1.0" encoding="UTF-8"?><cpe:platform-specification xmlns:cpe="http://cpe.mitre.org/language/2.0"><cpe:platform id="123"><cpe:title>Sun Solaris 5.8</cpe:title><cpe:logical-test operator="AND" negate="FALSE"><cpe:fact-ref name="cpe:2.3:a:bea:weblogic:8.*:*:*:*:*:*:*:*" /></cpe:logical-test></cpe:platform></cpe:platform-specification>'''

        >>> c1 = CPE2_3_FS('cpe:2.3:o:sun:solaris:5.9:*:*:*:*:*:*:*')
        >>> c2 = CPE2_3_FS('cpe:2.3:a:bea:weblogic:8.1:*:*:*:*:*:*:*')

        >>> s = CPESet2_3()
        >>> s.append(CPE2_3_WFN.unbind_fs(c1))
        >>> s.append(CPE2_3_WFN.unbind_fs(c2))

        >>> l = CPELanguage2_3(document)
        >>> l.language_match(s)
        True
        """

        # Root element
        ROOT_TAG = '#document'

        # A container for child platform definitions
        PLATSPEC_TAG = 'cpe:platform-specification'

        # Information about a platform definition
        PLATFORM_TAG = 'cpe:platform'
        LOGITEST_TAG = 'cpe:logical-test'
        CPE_TAG = 'cpe:fact-ref'
        CHECK_CPE_TAG = 'check-fact-ref'

        # Constant associated with an error in language matching
        ERROR = 2

        if cpel_dom is None:
            cpel_dom = self.document

        # Identify the root element
        if cpel_dom.nodeName == ROOT_TAG or cpel_dom.nodeName == PLATSPEC_TAG:
            for node in cpel_dom.childNodes:
                if node.nodeName == PLATSPEC_TAG:
                    return self.language_match(cpeset, node)
                if node.nodeName == PLATFORM_TAG:
                    return self.language_match(cpeset, node)

        # Identify a platform element
        elif cpel_dom.nodeName == PLATFORM_TAG:
            # Parse through E's elements and ignore all but logical-test
            for node in cpel_dom.childNodes:
                if node.nodeName == LOGITEST_TAG:
                    # Call the function again, but with logical-test
                    # as the root element
                    return self.language_match(cpeset, node)

        # Identify a CPE element
        elif cpel_dom.nodeName == CPE_TAG:
            # fact-ref's name attribute is a bound name,
            # so we unbind it to a WFN before passing it
            cpename = cpel_dom.getAttribute('name')
            wfn = CPELanguage2_3._unbind(cpename)
            return CPELanguage2_3._fact_ref_eval(cpeset, wfn)

        # Identify a check of CPE names (OVAL, OCIL...)
        elif cpel_dom.nodeName == CHECK_CPE_TAG:
            return CPELanguage2_3._check_fact_ref_Eval(cpel_dom)

        # Identify a logical operator element
        elif cpel_dom.nodeName == LOGITEST_TAG:
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

            operator = cpel_dom.getAttribute('operator').upper()

            if operator == 'AND':
                if count == len:
                    answer = True
            elif operator == 'OR':
                if count > 0:
                    answer = True

            operator_not = cpel_dom.getAttribute('negate')
            if operator_not:
                if (operator_not.upper() == 'TRUE') and (answer != ERROR):
                    answer = not answer

            return answer
        else:
            return False

    def ovalcheck(location, oval_id):
        pass

    def ocilcheck(location, ocil_id):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
