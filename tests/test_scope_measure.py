from tests import scope


def test_measure():
    scope.measure.enable(True)
    assert scope.measure.enable() == "ON"

    scope.measure.enable(False)
    assert scope.measure.enable() == "OFF"
