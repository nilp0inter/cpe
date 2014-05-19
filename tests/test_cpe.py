from cpe.cpe import CPE
from cpe.cpe1_1 import CPE1_1
from cpe.cpe2_2 import CPE2_2
from cpe.cpe2_3_wfn import CPE2_3_WFN
from cpe.cpe2_3_uri import CPE2_3_URI
from cpe.cpe2_3_fs import CPE2_3_FS

import unittest


class CreateCPEs(unittest.TestCase):
    """
    Check the __new__ function creates CPE names.
    """

    def setUp(self):
        # CPE version 1.1
        self.str11 = 'cpe:///mozilla:firefox:2.0::osx:es-es'
        self.str11_2e = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
        self.str11_or = 'cpe://microsoft:windows:xp!vista'

        # CPE version 2.2
        self.str22 = 'cpe:/a:mozilla:firefox:2.0:%up:osx:es-es'
        self.str22_percent = 'cpe:/a:adobe:acrobat:7.0:%up:'

        # CPE version 2.3 WFN
        self.str23_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", edition="osx", language="es\-es"]'

        # CPE version 2.3 formatted string
        self.str23_fs = 'cpe:2.3:a:mozilla:firefox:2.0.0.6:*:osx:es-es:*:*:*:*'

        # CPE version 2.3 URI
        self.str23_uri = 'cpe:/a:mozilla:firefox:2.0.0.6::osx:es-es'
        self.str23_uri_pack = 'cpe:/a:hp:insight_diagnostics:7.4.0.1570::~~online~win2003~x64~'

    def test_cpe_without_version(self):
        """
        __new__ should create CPE names with well-formed string without
        setting the version.
        """

        self.c11 = CPE(self.str11)
        self.assertIsInstance(self.c11, CPE1_1)

        self.c22 = CPE(self.str22)
        self.assertIsInstance(self.c22, CPE2_2)

        self.c23_wfn = CPE(self.str23_wfn)
        self.assertIsInstance(self.c23_wfn, CPE2_3_WFN)

        self.c23_fs = CPE(self.str23_fs)
        self.assertIsInstance(self.c23_fs, CPE2_3_FS)

        self.c23_uri = CPE(self.str23_uri)
        self.assertIsInstance(self.c23_uri, CPE2_3_URI)

    def test_cpe_with_version(self):
        """
        __new__ should create CPE names with well-formed string and version
        of CPE set.
        """

        c11_2e = CPE(self.str11_2e, CPE.VERSION_1_1)
        self.assertIsInstance(c11_2e, CPE1_1)
        c11_or = CPE(self.str11_or, CPE.VERSION_1_1)
        self.assertIsInstance(c11_or, CPE1_1)

        c22_percent = CPE(self.str22_percent, CPE.VERSION_2_2)
        self.assertIsInstance(c22_percent, CPE2_2)

        c23_wfn_uri_pack = CPE(self.str23_uri_pack, CPE.VERSION_2_3)
        self.assertIsInstance(c23_wfn_uri_pack, CPE2_3_URI)


class CreateBadCPEs(unittest.TestCase):
    """
    Check the __new__ function fails to create bad CPE names.
    """

    def setUp(self):
        # CPE version 1.1: bad character '%'
        self.str11_char = 'cpe:///mozilla:firefox:2.0:%up:osx:es-es'

        # CPE version 2.2: bad character '#'
        self.str22_char = 'cpe:/a:mozilla:firefox:2.0:#up:osx:es-es'

        # CPE version 2.2: bad character '!' (operation OR of version 1.1 not allowed
        self.str22_or = 'cpe://microsoft:windows:xp!vista'

        # CPE version 2.3 WFN: invalid attribute 'invented'
        self.str23_wfn_att = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", invented="fail"]'

        # CPE version 2.3 WFN: invalid value 'OTHER'
        self.str23_wfn_val = 'wfn:[part="o", vendor="microsoft", product="windows", version=OTHER]'

        # CPE version 2.3 formatted string: ';' without escape
        self.str23_fs_escape = 'cpe:2.3:a:mozilla:firefox:2.0:up;down:-:es-es:*:*:*:*'

        # CPE version 2.3 URI: character '%' without percent-encoded
        self.str23_uri_nopce = 'cpe:/a:mozilla:firefox:2.0:%up:osx:es-es'

        # CPE version 2.3 URI: bad packed edition (too many separators)
        self.str23_uri_pack = 'cpe:/a:hp:insight_diagnostics:7.4.0.1570::~~online~win2003~x64~~~'

    def test_bad_cpe_names_without_version(self):
        """
        __new__ should fails when you try to create CPE names with
        bad-formed string without setting version.
        """

        with self.assertRaises(NotImplementedError):
            CPE(self.str11_char)
            CPE(self.str22_char)
            CPE(self.str22_or)
            CPE(self.str23_wfn_att)
            CPE(self.str23_wfn_val)
            CPE(self.str23_fs_escape)
            CPE(self.str23_uri_nopce)
            CPE(self.str23_uri_pack)

    def test_bad_cpe_names_with_version(self):
        """
        __new__ should fails when you try to create CPE names with
        bad-formed string and version set.
        """

        with self.assertRaises(NotImplementedError):
            CPE(self.str11_char, CPE1_1)
            CPE(self.str22_char, CPE2_2)
            CPE(self.str22_or, CPE2_2)
            CPE(self.str23_wfn_att, CPE2_3_WFN)
            CPE(self.str23_wfn_val, CPE2_3_WFN)
            CPE(self.str23_fs_escape, CPE2_3_FS)
            CPE(self.str23_uri_nopce, CPE2_3_URI)
            CPE(self.str23_uri_pack, CPE2_3_URI)


class SanityCheck(unittest.TestCase):
    """
    Check the conversion between different style of CPE names.
    """

    def setUp(self):
        # CPE version 1.1
        self.str11 = 'cpe:///mozilla:firefox:2.0::osx:es-es'
        self.c11 = CPE(self.str11, CPE.VERSION_1_1)

        # CPE version 2.2
        self.str22 = 'cpe:/a:mozilla:firefox:2.0::osx:es-es'
        self.c22 = CPE(self.str22, CPE.VERSION_2_2)

        # CPE version 2.3 WFN
        self.str23_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", edition="osx", language="es\-es"]'
        self.c23_wfn = CPE(self.str23_wfn)

        # CPE version 2.3 formatted string
        self.str23_fs = 'cpe:2.3:a:mozilla:firefox:2.0:*:osx:es-es:*:*:*:*'
        self.c23_fs = CPE(self.str23_fs)
        self.str23_fs_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", update=ANY, edition="osx", language="es\-es", sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]'

        # CPE version 2.3 URI
        self.str23_uri = 'cpe:/a:mozilla:firefox:2.0::osx:es-es'
        self.c23_uri = CPE(self.str23_uri)
        self.str23_uri_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", update=ANY, edition="osx", language="es\-es"]'

    def test_as_wfn(self):
        """
        as_wfn should give the same WFN string with equals CPE names
        defined with different versions of CPE.
        """

        self.assertTrue(self.c11.as_wfn() == self.str23_wfn)
        self.assertTrue(self.c22.as_wfn() == self.str23_wfn)
        self.assertTrue(self.c23_wfn.as_wfn() == self.str23_wfn)
        self.assertTrue(self.c23_fs.as_wfn() == self.str23_fs_wfn)
        self.assertTrue(self.c23_uri.as_wfn() == self.str23_uri_wfn)

    def test_as_uri(self):
        """
        as_uri should give the same WFN string with equals CPE names
        defined with different versions of CPE.
        """

        self.assertTrue(self.c11.as_uri_2_3() == self.str23_uri)
        self.assertTrue(self.c22.as_uri_2_3() == self.str23_uri)
        self.assertTrue(self.c23_wfn.as_uri_2_3() == self.str23_uri)
        self.assertTrue(self.c23_fs.as_uri_2_3() == self.str23_uri)
        self.assertTrue(self.c23_uri.as_uri_2_3() == self.str23_uri)

    def test_as_fs(self):
        """
        as_fs should give the same WFN string with equals CPE names
        defined with different versions of CPE.
        """

        self.assertTrue(self.c11.as_fs() == self.str23_fs)
        self.assertTrue(self.c22.as_fs() == self.str23_fs)
        self.assertTrue(self.c23_wfn.as_fs() == self.str23_fs)
        self.assertTrue(self.c23_fs.as_fs() == self.str23_fs)
        self.assertTrue(self.c23_uri.as_fs() == self.str23_fs)


class CompareCPEs(unittest.TestCase):
    """
    Check the conversion between different style of CPE names.
    """

    def setUp(self):
        # CPE version 1.1
        self.str11 = 'cpe:///mozilla:firefox:2.0::osx:es-es'
        self.c11 = CPE(self.str11, CPE.VERSION_1_1)

        self.str11_2e = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
        self.c11_2e = CPE(self.str11_2e, CPE.VERSION_1_1)

        self.str11_or = 'cpe://microsoft:windows:xp!vista'
        self.c11_or = CPE(self.str11_or, CPE.VERSION_1_1)

        # CPE version 2.2
        self.str22 = 'cpe:/a:mozilla:firefox:2.0::osx:es-es'
        self.c22 = CPE(self.str22, CPE.VERSION_2_2)

        # CPE version 2.3 WFN
        self.str23_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", edition="osx", language="es\-es"]'
        self.c23_wfn = CPE(self.str23_wfn)

        # CPE version 2.3 formatted string
        self.str23_fs = 'cpe:2.3:a:mozilla:firefox:2.0:*:osx:es-es:*:*:*:*'
        self.c23_fs = CPE(self.str23_fs)
        self.str23_fs_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", update=ANY, edition="osx", language="es\-es", sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]'

        # CPE version 2.3 URI
        self.str23_uri = 'cpe:/a:mozilla:firefox:2.0::osx:es-es'
        self.c23_uri = CPE(self.str23_uri)
        self.str23_uri_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", update=ANY, edition="osx", language="es\-es"]'

    def test_equals(self):
        """
        __eq__ should return True if the CPE names of distinct versions have
        the equivalent WFN string.
        """

        self.assertEquals(self.c11, self.c22)
        self.assertEquals(self.c22, self.c11)
        self.assertEquals(self.c11, self.c23_wfn)
        self.assertEquals(self.c11, self.c23_fs)
        self.assertEquals(self.c23_uri, self.c23_fs)

    def test_incompatible_versions(self):
        """
        __eq__ should raise an exception when CPE name of version 1.1 has
        more than a element.
        """

        self.assertRaises(self.c11_2e == self.c22)
        self.assertRaises(self.c11_or == self.c23_wfn)


class GetAttributeValues(unittest.TestCase):
    """
    Check the value returned by the functions associated with CPE name
    attributes.
    """

    def setUp(self):
        # CPE version 1.1
        self.str11 = 'cpe:///mozilla:firefox:2.0::osx:es-es'
        self.c11 = CPE(self.str11, CPE.VERSION_1_1)

        self.str11_2e = 'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0'
        self.c11_2e = CPE(self.str11_2e, CPE.VERSION_1_1)

        self.str11_or = 'cpe://microsoft:windows:xp!vista'
        self.c11_or = CPE(self.str11_or, CPE.VERSION_1_1)

        self.str11_hw = 'cpe:/hp:nvidia:pro'
        self.c11_hw = CPE(self.str11_hw, CPE.VERSION_1_1)

        # CPE version 2.2
        self.str22 = 'cpe:/a:mozilla:firefox:2.0::osx:es-es'
        self.c22 = CPE(self.str22, CPE.VERSION_2_2)

        # CPE version 2.3 WFN
        self.str23_wfn = r'wfn:[part="a", vendor="mozilla", product="firefox", version="2\.0", edition="osx", language="es\-es"]'
        self.c23_wfn = CPE(self.str23_wfn)

        self.str23_uri = 'cpe:/'
        self.c23_uri = CPE(self.str23_uri)

    def test_get_one_value_defined(self):
        """
        getXXX() fucntion, where XXX is the name of an attribute of CPE name,
        should return only value when its components has only one element.
        These functions always return a list.
        """

        # Version 1.1
        self.assertTrue(self.c11.get_edition() == ["osx"])

        # Version 2.2
        self.c22.get_vendor()
        self.assertTrue(self.c22.get_vendor() == ["mozilla"])

        # Version 2.3 (with double quotes)
        self.assertTrue(self.c23_wfn.get_language() == ['"es\\-es"'])

    def test_get_one_value_undefined(self):
        """
        getXXX() fucntion, where XXX is the name of an attribute of CPE name,
        should return a empty value when the attibute is not set.
        """

        # Version 2.3
        self.assertTrue(self.c23_uri.get_language() == [''])

    def test_check_system_type(self):
        """
        isXXX() fucntion, where XXX is the name of type of system of CPE name
        (hardware, operating system and software) should return True or False
        if the attribute "part" of CPE name corresponds to type of system of
        function.
        """

        # Version 1.1
        self.assertTrue(self.c11.is_application())
        self.assertTrue(self.c11_2e.is_application())
        self.assertTrue(self.c11_2e.is_operating_system())
        self.assertTrue(self.c11_hw.is_hardware())

        # Version 2.2
        self.assertTrue(self.c22.is_application())
        self.assertFalse(self.c22.is_operating_system())

    def test_get_many_values(self):
        """
        getXXX() fucntion, where XXX is the name of an attribute of CPE name,
        should return a list of values when its components has two or more
        element. These functions always return a list.
        """

        # Version 1.1
        self.assertTrue(self.c11_2e.get_product() == ["sunos", "weblogic", "server"])
        self.assertTrue(self.c11_or.get_version() == ["xp!vista"])

if __name__ == '__main__':
    unittest.main()
