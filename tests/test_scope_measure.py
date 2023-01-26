from tests import scope
from instrumentation.siglent.measure import Source


def test_measure():
    scope.measure.enable(True)
    assert scope.measure.enable() == "ON"

    scope.measure.enable(False)
    assert scope.measure.enable() == "OFF"


def test_measure_simple_source():
    scope.measure.simple.source(Source.C1)
    assert scope.measure.simple.source() == "C1"

    scope.measure.simple.source(Source.C2)
    assert scope.measure.simple.source() == "C2"
