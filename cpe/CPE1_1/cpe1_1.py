#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cpe1_1.py
Author: Alejandro Galindo
Date: 18-04-2013
Description: Module for the treatment of identifiers of IT platforms
             (hardware, operating systems or applications of system)
             in accordance with version 1.1 of specification CPE
             (Common Platform Enumeration).
'''


from cpe.cpebase import CPEBASE

import re


class CPE1_1(CPEBASE):
    """
    Implementation of CPE specification 1.1.

    - TEST: bad URI
    >>> uri = 'baduri'
    >>> CPE1_1(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE1_1/cpe1_1.py", line 56, in __init__
        OP_NOT = "~"
      File "cpe/CPE1_1/cpe1_1.py", line 102, in _validate_uri
        #  CPE ID PART
    TypeError: Input identifier is not a valid CPE ID: Error to split CPE ID parts

    - TEST: URI with whitespaces
    >>> uri = 'cpe con espacios'
    >>> CPE1_1(uri)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE1_1/cpe1_1.py", line 56, in __init__
        OP_NONE = "None"
      File "cpe/CPE1_1/cpe1_1.py", line 77, in _validate_uri
        Checks CPE name with URI style is valid.
    TypeError: Malformed CPE, it must not have whitespaces

    - TEST: two operators in a subcomponent
    >>> uri = 'cpe://microsoft:windows:~2000!2007'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "cpe/CPE1_1/cpe1_1.py", line 56, in __init__
        - TEST: an application part
      File "cpe/CPE1_1/cpe1_1.py", line 164, in _validate_uri
    TypeError: Malformed CPE, can't ~ and ! in the same component

    - TEST: an empty hardware part, and no OS or application part.
    >>> uri = 'cpe:/'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an application part
    >>> uri = 'cpe://microsoft:windows:2000'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an OS part with an application part
    >>> uri = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an hardware part with OS part
    >>> uri = 'cpe:/cisco::3825/cisco:ios:12.3:enterprise'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: an application part
    >>> uri = 'cpe:///microsoft:ie:6.0'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: OS part with operator OR (two subcomponents)
    >>> uri = 'cpe://microsoft:windows:xp!vista'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: OS part with operator NOT (a subcomponent)
    >>> uri = 'cpe://microsoft:windows:~xp'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    - TEST: OS part with two elements in application part
    >>> uri = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
    >>> CPE1_1(uri) # doctest: +ELLIPSIS
    <__main__.CPE1_1 object at 0x...>

    """

    # CPE version
    VERSION = '1.1'

    # Constants associated with dictionary keys that
    # store CPE name elements
    KEY_HW = "hardware"
    KEY_OS = "operating_system"
    KEY_APP = "application"

    KEY_COMP_OP = "operator"
    KEY_COMP_NAME = "name"

    OP_OR = "!"
    OP_NOT = "~"
    OP_NONE = "None"
    OP_ANY = "ANY"

    def __init__(self, cpe_uri):
        """
        Checks that a CPE name defined with URI style is valid and,
        if so, stores the components in a dictionary.
        """

        CPEBASE.__init__(self)

        # Store CPE name with URI style:
        #     CPE names are case-insensitive.
        #     To reduce potential for confusion,
        #     all CPE Names should be written in lowercase
        self.uri = cpe_uri.lower()

        self._validate_uri()

    def _validate_uri(self):
        """
        Checks CPE name with URI style is valid.

        Basic structure of CPE name:
        - Hardware part: the physical platform supporting the IT system.
        - Operating system part: the operating system controls and manages the
          IT hardware.
        - Application part: software systems, services, servers, and packages
          installed on the system.

        CPE name syntax:
        - cpe:/ {hardware-part} [ / {OS-part} [ / {application-part} ] ]
        """

        # CPE ID URI must not have whitespaces
        if (self.uri.find(" ") != -1):
            msg = "Malformed CPE, it must not have whitespaces"
            raise TypeError(msg)

        # Compilation of regular expression associated with name of components
        name_pattern = "[\d\w\.\-,\(\)@#]+"
        name_rxc = re.compile(name_pattern, re.IGNORECASE)

        # ###################
        #  CPE ID PART
        # ###################

        # Compilation of regular expression associated with parts of CPE ID
        hw = "?P<%s>[^/]+" % CPE1_1.KEY_HW
        os = "?P<%s>[^/]+" % CPE1_1.KEY_OS
        app = "?P<%s>[^/]+" % CPE1_1.KEY_APP

        parts_pattern = "^cpe:/(%s)?(/(%s)?(/(%s)?)?)?$" % (hw, os, app)
        parts_rxc = re.compile(parts_pattern, re.IGNORECASE)

        # Partitioning of CPE ID
        parts_match = parts_rxc.match(self.uri)

        # Validation of CPE ID parts
        if (parts_match is None):
            msg = "Input identifier is not a valid CPE ID: "
            msg += "Error to split CPE ID parts"
            raise TypeError(msg)

        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]
        for pk in parts_key:
            self.cpe_dict[pk] = []

            # Get part content
            part = parts_match.group(pk)

            if (part is not None):

                # Part content is not empty
                i = 0

                # ############################
                #  CPE ID PART ELEMENTS
                # ###########################

                # semicolon (;) is ueesed to separate the name elements
                # in a CPE Name part
                for part_elem in part.split(';'):
                    self.cpe_dict[pk].append([])
                    self.cpe_dict[pk][i] = []
                    j = 0

                    # #################################
                    #  CPE ID PART ELEMENT COMPONENTS
                    # #################################

                    # colon (:) is used to separate the components
                    # in a name element
                    for elem_comp in part_elem.split(":"):
                        self.cpe_dict[pk][i].append([])
                        self.cpe_dict[pk][i][j] = []

                        # Compilation of regular expression associated with
                        # components of CPE part
                        cpe_comp_pattern = "^(~?[^~!:;/%]+)(![^~!:;/%]+)*$"
                        cpe_comp_rxc = re.compile(cpe_comp_pattern,
                                                  re.IGNORECASE)

                        comp_match = cpe_comp_rxc.match(elem_comp)

                        if (comp_match is not None):
                            if (len(elem_comp) == 0):
                                # Any value is possible
                                component = {}
                                component[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_ANY
                                component[CPE1_1.KEY_COMP_NAME] = elem_comp

                            else:
                                # Component is not empty
                                not_found = elem_comp.find('~') != -1
                                or_found = elem_comp.find('!') != -1

                                if (not_found) and (or_found):
                                    # The OR and NOT operators may not be used
                                    # together
                                    msg = "Malformed CPE, can't ~ and ! "
                                    msg += "in the same component"

                                    raise TypeError(msg)

                                elif elem_comp.find('~') == 0:
                                    # Operator NOT with a name
                                    name = elem_comp[1:]

                                    component = {}
                                    component[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NOT
                                    component[CPE1_1.KEY_COMP_NAME] = name

                                    if (name_rxc.match(name) is None):
                                        msg = "Malformed CPE, names must have "
                                        msg += "only the following characters:"
                                        msg += " alfanumeric, '.', '_', '-', "
                                        msg += "',', '(', ')', '@', '#'"

                                        raise TypeError(msg)

                                    self.cpe_dict[pk][i][j].append(component)

                                elif elem_comp.find('!') != -1:
                                    # Operator OR with two or more names
                                    for name in elem_comp.split('!'):
                                        if (name_rxc.match(name) is None):
                                            msg = "Malformed CPE, names must have "
                                            msg += "only the following characters:"
                                            msg += " alfanumeric, '.', '_', '-', "
                                            msg += "',', '(', ')', '@', '#'"

                                            raise TypeError(msg)

                                        component = {}
                                        component[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_OR
                                        component[CPE1_1.KEY_COMP_NAME] = name

                                        self.cpe_dict[pk][i][j].append(component)
                                else:
                                    # Name without operator
                                    component = {}
                                    component[CPE1_1.KEY_COMP_OP] = CPE1_1.OP_NONE
                                    component[CPE1_1.KEY_COMP_NAME] = elem_comp

                                    self.cpe_dict[pk][i][j].append(component)
                        j += 1
                    i += 1

        return self.cpe_dict

    def __len__(self):
        """
        Returns the number of component names of CPE ID.
        "a!b" is a component, not two components.

        - TEST: a component with two components
        >>> uri = "cpe:///"
        >>> c = CPE1_1(uri)
        >>> len(c)
        0

        - TEST: components with a subcomponent
        >>> uri = "cpe:/cisco::3825/cisco:ios:12.3:enterprise"
        >>> c = CPE1_1(uri)
        >>> len(c)
        7

        - TEST: a component with two components
        >>> uri = "cpe:///adobe:acrobat:6.0:std!pro"
        >>> c = CPE1_1(uri)
        >>> len(c)
        4
        """

        count = 0
        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]

        for pk in parts_key:
            elements = self.cpe_dict[pk]
            for elem in elements:
                for component in elem:
                    count += 1

        return count

    def __getitem__(self, i):
        """
        Returns the i'th component name of CPE ID as a string.
        """

        NONAME = ""
        count = 0
        parts_key = [CPE1_1.KEY_HW, CPE1_1.KEY_OS, CPE1_1.KEY_APP]

        for pk in parts_key:
            elements = self.cpe_dict[pk]
            for elem in elements:
                for comp in elem:
                    if (count == i):
                        return comp
                    else:
                        count += 1
        return NONAME

    def _getPartCompNameList(self, part, index):
        '''
        Returns the i'th component name of elements of input part:

        INPUT:
            - part: Type of part of system (hardware, os, application)
            - index: position of component inside part

        OUTPUT:
            - list of subcomponents of i'th component
        '''

        NONAME = ""
        lc = []
        if (part not in self.cpe_dict.keys()):
            raise KeyError("Part key is not exist")

        elements = self.cpe_dict[part]
        for elem in elements:
            if len(elem) > index:
                comp = elem[index]
                for subcomp in comp:
                    key = CPE1_1.KEY_COMP_NAME
                    lc.append(subcomp[key])
        return lc

    def getHardwareVendorList(self):
        '''
        Returns the hardware vendor list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_HW, 0)

    def getHardwareFamilyList(self):
        '''
        Returns the hardware family name list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_HW, 1)

    def getHardwareModelList(self):
        '''
        Returns the hardware model list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_HW, 2)

    def getOsVendorList(self):
        '''
        Returns the operating system vendor list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_OS, 0)

    def getOsFamilyList(self):
        '''
        Returns the operating system family name list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_OS, 1)

    def getOsVersionList(self):
        '''
        Returns the operating system version list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_OS, 2)

    def getAppVendorList(self):
        '''
        Returns the application vendor list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_APP, 0)

    def getAppFamilyList(self):
        '''
        Returns the application family name list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_APP, 1)

    def getAppEditionList(self):
        '''
        Returns the application edition list.
        '''

        return self._getPartCompNameList(CPE1_1.KEY_APP, 2)

    def __unicode__(self):
        """
        Print CPE URI as string.
        """

        return self.uri


if __name__ == "__main__":
    #uri = 'cpe:/cisco::3825/cisco:ios:12.3:enterprise'
    #uri = 'cpe:///'
    #uri = 'cpe:////'
    #uri = 'cpe://microsoft:windows:2000::sp4'
    #uri = 'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52'
    #uri = 'cpe:/cisco::3825;cisco:2:44/cisco:ios:12.3:enterprise'
    #uri = 'cpe://microsoft:windows:xp!vista'
    #uri = 'cpe://microsoft:windows:~xp'
    #uri = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'

    #ce = CPE1_1(uri)
    #print("")
    #print(ce)
    #print("Elements: %s") % len(ce)
    #print("")
    #for i in range(len(ce)):
    #    print("Element %s: %s") % (i, ce[i])
    #print("")
    #print("HARDWARE vendor list: %s") % ce.getHardwareVendorList()
    #print("HARDWARE family name list: %s") % ce.getHardwareFamilyList()
    #print("HARDWARE model list: %s") % ce.getHardwareModelList()
    #print("")
    #print("OS vendor list: %s") % ce.getOsVendorList()
    #print("OS family name list: %s") % ce.getOsFamilyList()
    #print("OS version list: %s") % ce.getOsVersionList()
    #print("")
    #print("Application vendor list: %s") % ce.getAppVendorList()
    #print("Application family name list: %s") % ce.getAppFamilyList()
    #print("Application edition list: %s") % ce.getAppEditionList()
    #print("")

    import doctest
    doctest.testmod()
