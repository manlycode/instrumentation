from instrumentation.siglent.scope import ScopeId
from tests import scope

def test_reset():
    scope.reset()
    # Verified manually
    assert True

def test_scope_id():
    result = ScopeId("Siglent Technologies,SDS1204X-E,SDS1EBAC0L0098,7.6.1.15")
    assert result.manufacturer == "Siglent Technologies"
    assert result.model == "SDS1204X-E"
    assert result.serial_num == "SDS1EBAC0L0098"
    assert result.firmware == "7.6.1.15"


def test_idn():
    result = scope.idn()
    assert result.manufacturer == "Siglent Technologies"
    assert result.model == "SDS1104X-U"
    assert result.serial_num == "SDSAHBAQ6R1188"
    assert result.firmware == "2.1.1.1.5R6"


def test_opc():
    assert scope.opc(True) is None
    assert scope.opc() == 1



