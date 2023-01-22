from instrumentation.base import NAME
from tests import awg, scope


def test_base():
    assert NAME == "instrumentation"


def test_awg():
    assert awg is not None


def test_scope():
    assert scope is not None
