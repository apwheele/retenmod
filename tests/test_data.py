"""
Tests for data loading
in the wheel file
"""


from retenmod import data_funcs


def test_meta():
    assert list(data_funcs.metadata.keys()) == ["metadata"]
    url = (
        "https://www.ojp.gov/sites/g/files/xyckuh241" "/files/media/document/193428.pdf"
    )
    assert data_funcs.metadata["metadata"][0]["source"] == url


def test_agency():
    sd = data_funcs.staff()
    assert sd.shape == (7, 3)
    ty = (sd[:, 0] != [1, 2, 3, 4, 5, 10, 15]).sum()
    assert ty == 0
