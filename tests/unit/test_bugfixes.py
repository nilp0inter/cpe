from cpe import CPE
from cpe.cpe2_3_uri import CPE2_3_URI


def test_issue_8():
    """TEST multiple %01 wildcards."""
    current = CPE2_3_URI('cpe:/a:microsoft:internet_explorer:%01%018.%02:%02s%01%01%01').as_wfn()
    expected = 'wfn:[part="a", vendor="microsoft", product="internet_explorer", version="??8\\.*", update="*s???"]'
    assert current == expected


def test_issue_11():
    """TEST: correctly transform not applicable values for edition."""
    current = CPE('wfn:[part="a", vendor="TauPan", product="cpelib", version="1\\.0\\.5", update=NA, edition=NA]').as_uri_2_3()
    expected = 'cpe:/a:taupan:cpelib:1.0.5:-:-'
    assert current == expected
