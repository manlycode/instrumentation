from tests import awg


def test_measure():
    awg.measure.enable(True)
    assert awg.measure.enable() == "ON"
