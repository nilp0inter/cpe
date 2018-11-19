from __future__ import print_function

import pytest

from cpe.cpe import CPE
from cpe.cpe1_1 import CPE1_1
from cpe.comp.cpecomp import CPEComponent
from cpe.comp.cpecomp1_1 import CPEComponent1_1


#
# Test for _get_attribute_values(self)
#
def test_get_attribute_values_1():
    """(version 1.1) not negate components"""
    c = CPE('cpe:///microsoft:ie:6.0')
    att = CPEComponent.ATT_VENDOR
    assert c.get_attribute_values(att) == ['microsoft']


def test_get_attribute_values_2():
    """CPE Name with multiple parts and elements"""
    c = CPE('cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0')
    att = CPEComponent.ATT_VENDOR
    assert c.get_attribute_values(att) == ['sun', 'bea', 'mysql']


#
# Test for __getitem__(self, i)
#
def test_getitem_1():
    """good index"""
    c = CPE1_1('cpe:///sun_microsystem:sun@os:5.9:#update')
    assert isinstance(c[1], CPEComponent1_1)
    assert str(c[1]) == "sun@os"


def test_getitem_2():
    """bad index"""
    c = CPE1_1('cpe:///sun_microsystem:sun@os:5.9:#update')
    with pytest.raises(IndexError):
        c[6]


def test_getitem_3():
    """bad index"""
    c = CPE1_1('cpe://')
    with pytest.raises(IndexError):
        c[0]


#
# Test for __new__(cls, cpe_str, *args, **kwargs)
#
@pytest.mark.parametrize('s', [
    # An empty hardware part, and no OS or application part.
    'cpe:/',

    # An application part
    'cpe://microsoft:windows:2000',

    # An OS part with an application part,
    'cpe://redhat:enterprise_linux:3:as/apache:httpd:2.0.52',

    # An hardware part with OS part
    'cpe:/cisco::3825/cisco:ios:12.3:enterprise',

    # An application part
    'cpe:///microsoft:ie:6.0',

    # OS part with operator OR (two subcomponents)
    'cpe://microsoft:windows:xp!vista',

    # OS part with operator NOT (a subcomponent)
    'cpe://microsoft:windows:~xp',

    # OS part with two elements in application part
    'cpe://sun:sunos:5.9/bea:weblogic:8.1;mysql:server:5.0',

    # CPE with special characters
    'cpe:///sun_microsystem:sun@os:5.9:#update',
])
def test_new_legal_cpe(s):
    """legal cpe"""
    CPE1_1(s)  # Must instantiate just fine


@pytest.mark.parametrize('s', [
    # Bad URI syntax
    'baduri',
    # URI with whitespaces
    'cpe:/con espacios',
    # Two operators in a subcomponent
    'cpe://microsoft:windows:~2000!2007',
])
def test_new_ilegal_cpe(s):
    """ilegal cpe"""
    with pytest.raises(ValueError):
        CPE1_1(s)

#
# Test for __len__(self)
#
@pytest.mark.parametrize('s,l', [
    # A CPE name with empty parts
    ("cpe:///", 0),

    # A CPE name with two parts (hw and os) and some elements empty and
    # with values
    ("cpe:/cisco::3825/cisco:ios:12.3:enterprise", 7),

    # A CPE name with a application part and a component with two
    # subcomponents
    ("cpe:///adobe:acrobat:6.0:std!pro", 4),
])
def test_len(s, l):
    assert len(CPE1_1(s)) == l


#
# Test for __str__(self)
#
def test_str_1():
    """not negate components"""
    current = str(CPE1_1('cpe:///microsoft:ie:6.0'))
    expected = "CPE v1.1: cpe:///microsoft:ie:6.0"
    assert current == expected

def test_str_2():
    """negate components"""
    current = str(CPE1_1('cpe://microsoft:windows:~xp'))
    expected = "CPE v1.1: cpe://microsoft:windows:~xp"
    assert current == expected

