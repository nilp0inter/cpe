from __future__ import print_function

import pytest

from cpe.cpe import CPE
from cpe.cpe2_2 import CPE2_2
from cpe.comp.cpecomp import CPEComponent
from cpe.comp.cpecomp2_2 import CPEComponent2_2


#
# Test for _get_attribute_values(self)
#
def test_get_attribute_values_1():
    c = CPE2_2('cpe:/a:mozilla:firefox:2.0.0.6::osx:zh-tw')
    assert c.get_attribute_values(CPEComponent.ATT_VENDOR) == ['mozilla']
    assert c.get_attribute_values(CPEComponent.ATT_LANGUAGE) == ['zh-tw']


#
# Test for __getitem__(self, i)
#
def test_getitem_1():
    """good index"""
    c = CPE2_2('cpe:/a:mozilla:firefox:2.0.0.6::osx:zh-tw')
    assert isinstance(c[1], CPEComponent2_2)
    assert str(c[1]) == "mozilla"


def test_getitem_2():
    """bad index"""
    c = CPE2_2('cpe:/a:mozilla:firefox:2.0.0.6::osx:zh-tw')
    with pytest.raises(IndexError):
        c[8]


def test_getitem_3():
    """bad index"""
    c = CPE2_2('cpe:/')
    with pytest.raises(IndexError):
        c[0]


#
# Test for __new__(cls, cpe_str, *args, **kwargs)
#
@pytest.mark.parametrize('s', [
    # An empty hardware part, and no OS or application part.
    'cpe:/',

    # An operation system. The CPE Name below designates all
    # Professional editions of Microsoft Windows XP, regardless of
    # service pack level.
    'cpe:/o:microsoft:windows_xp:::pro',

    # An application
    'cpe:/a:acme:product:1.0:update2:-:en-us',

    # An application
    'cpe:/a:acme:product:1.0:update2::en-us',

    # An application
    'cpe:/a:acme:product:1.0:update2:pro:en-us',

    # An application. The vendor Best Software may not have a qualified
    # DNS name, so a CPE Name for their application ABC123 would be as
    # follows:
    'cpe:/a:best_software:abc123',

    # For applications that do not have a vendor or organization
    # associated with them, this component  should use a developer's
    # name. Note that multi-word names should use underscores instead of
    # spaces.
    'cpe:/a:jon_smith:tool_name:1.2.3',

    # An application. Multi-word product names and designations should
    # be spelled out in full, replacing spaces with underscores.  The
    # example below shows how this would look for the Zone Labs
    # ZoneAlarm Internet Security Suite version 7.0.
    'cpe:/a:zonelabs:zonealarm_internet_security_suite:7.0',

    # The following example denotes Adobe Reader version 8.1
    'cpe:/a:adobe:reader:8.1',

    # The following example denotes Red Hat Enterprise Linux 4.0 Update
    # 4.
    'cpe:/o:redhat:enterprise_linux:4:update4',

    # CPE Name of Red Hat operating system with initial release of
    # Enterprise Linux 4
    'cpe:/o:redhat:enterprise_linux:4:ga',

    # An operating system
    'cpe:/o:microsoft:windows_2000::sp4:pro',

    # An application
    'cpe:/a:mozilla:firefox:2.0.0.6::osx:zh-tw',

    # This example name below represents a typical CPE Name that refers
    # to the Microsoft Windows 2000 operating system, all editions and
    # update levels.
    'cpe:/o:microsoft:windows_2000',

    # This example CPE Name below identifies Microsoft?s Windows XP
    # operating system, Professional Edition, update level "Service Pack
    # 2".
    'cpe:/o:microsoft:windows_xp::sp2:pro',

    # This example name below refers to Red Hat Enterprise Linux 3
    # Advanced Server.
    'cpe:/o:redhat:enterprise_linux:3::as',

    # This example specifies an application, specifically the Apache
    # Foundation HTTP server version 2.0.52.
    'cpe:/a:apache:httpd:2.0.52',

    # This example name below refers to a particular web browser,
    # regardless of any hardware or particular OS on which it is
    # running.
    'cpe:/a:microsoft:ie:6.0',

    # This example name below refers to a Cisco model 3825 integrated
    # services router.
    'cpe:/h:cisco:router:3825',

    # The example name below identifies a particular laptop computer
    # hardware platform. The vendor is Dell Computer, the product line
    # name is "Inspiron", and the version (or model in this example)
    # number is 8500.
    'cpe:/h:dell:inspiron:8500',

    # The CPE Name below shows an example for a virtual hardware
    # platform.
    'cpe:/h:emc:vmware_esx:2.5',

    # The CPE name below shows a valid CPE that contains a '/' in the product
    'cpe:/a:intel:proset\/wireless_wifi'
])
def test_new_legal_cpe(s):
    """legal cpe"""
    CPE2_2(s)  # Must instantiate just fine


@pytest.mark.parametrize('s', [
    # bad URI syntax
    'baduri',

    # URI with whitespaces
    'cpe:/con espacios',
])
def test_new_ilegal_cpe(s):
    """ilegal cpe"""
    with pytest.raises(ValueError):
        CPE2_2(s)


#
# Test for __len__(self)
#
@pytest.mark.parametrize('s,l', [
    # A CPE name without components
    ("cpe:/", 0),

    # A CPE name with some full components
    ("cpe:/a:i4s:javas", 3),

    # A CPE name with some empty components
    ("cpe:/a:i4s:::javas", 5),

    # A CPE name with all components
    ("cpe:/a:acme:product:1.0:update2:-:en-us", 7),
])
def test_len(s, l):
    assert len(CPE2_2(s)) == l


#
# Test for __str__(self)
#
def test_str():
    """not negate components"""
    current = str(CPE2_2('cpe:/a:acme:product:1.0:update2:-:en-us'))
    expected = "CPE v2.2: cpe:/a:acme:product:1.0:update2:-:en-us"
    assert current == expected
