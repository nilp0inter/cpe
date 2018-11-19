from __future__ import print_function
from cpe.cpe2_3_uri import CPE2_3_URI

import pytest


def test_regular_cpe():
    uri = 'cpe:/a:TauPan:cpe:1.2.1BETA1'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part="a", vendor="taupan", product="cpe", version="1\\.2\\.1beta1"]'
    assert c.as_uri_2_3() == uri.lower()


def test_percent_encoded():
    uri = 'cpe:/a:TauPan:cpe%7cextra:1.2.1BETA1'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part="a", vendor="taupan", product="cpe\\|extra", version="1\\.2\\.1beta1"]'
    assert c.as_uri_2_3() == uri.lower()


def test_just_part():
    uri = 'cpe:/a'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part="a"]'
    assert c.as_uri_2_3() == uri.lower()


def test_just_vendor():
    uri = 'cpe:/:taupan'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part=ANY, vendor="taupan"]'
    assert c.as_uri_2_3() == uri.lower()


def test_just_product():
    uri = 'cpe:/::cpe'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part=ANY, vendor=ANY, product="cpe"]'
    assert c.as_uri_2_3() == uri.lower()


def test_just_version():
    uri = 'cpe:/:::version'
    cpe = CPE2_3_URI(uri)
    assert cpe.as_wfn() == ('wfn:[part=ANY, vendor=ANY, product=ANY, '
                            'version="version"'
                            ']')
    assert cpe.as_uri_2_3() == uri.lower()


def test_just_update():
    uri = 'cpe:/::::update'
    cpe = CPE2_3_URI(uri)
    assert cpe.as_wfn() == ('wfn:[part=ANY, vendor=ANY, product=ANY, '
                            'version=ANY, '
                            'update="update"'
                            ']')
    assert cpe.as_uri_2_3() == uri.lower()


def test_just_legacy_edition_uri():
    uri = 'cpe:/:::::legacy_edition'
    cpe = CPE2_3_URI(uri)
    assert cpe.as_uri_2_3() == uri.lower()


@pytest.mark.xfail
def test_just_legacy_edition_wfn():
    uri = 'cpe:/:::::legacy_edition'
    cpe = CPE2_3_URI(uri)
    # not sure if this is correct, see
    # https://github.com/nilp0inter/cpe/issues/28#issuecomment-253195951
    assert cpe.as_wfn() == ('wfn:[part=ANY, vendor=ANY, product=ANY, '
                            'version=ANY, '
                            'update=ANY, '
                            'edition="legacy_edition"'
                            ']')


def test_full_packed_edition():
    uri = 'cpe:/:::::~edition~sw_edition~target_sw~target_hw~other'
    cpe = CPE2_3_URI(uri)
    assert cpe.as_wfn() == ('wfn:[part=ANY, vendor=ANY, product=ANY, '
                            'version=ANY, '
                            'update=ANY, '
                            'edition="edition", '
                            'sw_edition="sw_edition", '
                            'target_sw="target_sw", '
                            'target_hw="target_hw", '
                            'other="other"'
                            ']')
    assert cpe.as_uri_2_3() == uri.lower()


def test_legacy_edition_uri():
    uri = 'cpe:/a:TauPan:cpe:1.2.1BETA1::legacy_edition'
    c = CPE2_3_URI(uri)
    assert c.as_uri_2_3() == uri.lower()


@pytest.mark.xfail  # see above
def test_legacy_edition_wfn():
    uri = 'cpe:/a:TauPan:cpe:1.2.1BETA1::legacy_edition'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part="a", vendor="taupan", product="cpe", version="1\\.2\\.1beta1", update=ANY, edition="legacy_edition"]'


def test_legacy_edition_packed():
    uri = 'cpe:/a:TauPan:cpe:1.2.1BETA1::~legacy_edition~~~~'
    c = CPE2_3_URI(uri)
    assert c.as_wfn() == 'wfn:[part="a", vendor="taupan", product="cpe", version="1\\.2\\.1beta1", update=ANY, edition="legacy_edition", sw_edition=ANY, target_sw=ANY, target_hw=ANY, other=ANY]'
    assert c.as_uri_2_3() == 'cpe:/a:taupan:cpe:1.2.1beta1::legacy_edition'
