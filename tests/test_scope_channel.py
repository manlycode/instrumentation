import pytest

from tests import scope
from instrumentation.siglent.scope import BWLimit, Coupling, Impedance

channel = scope.channel(1)
channels = scope.channels([3, 4])


def test_channel_bwLimit():
    channel.bwLimit(BWLimit.BWL_200M)
    assert channel.bwLimit() == "FULL"

    channel.bwLimit(BWLimit.BWL_20M)
    assert channel.bwLimit() == "20M"


def test_channels_bwLimit():
    channels.bwLimit(BWLimit.BWL_200M)
    assert channels.bwLimit() == ["FULL", "FULL"]

    channels.bwLimit(BWLimit.BWL_20M)
    assert channels.bwLimit() == ["20M", "20M"]


def test_channel_coupling():
    channel.coupling(Coupling.AC)
    assert channel.coupling() == "AC"

    channel.coupling(Coupling.DC)
    assert channel.coupling() == "DC"


def test_channels_coupling():
    channels.coupling(Coupling.AC)
    assert channels.coupling() == ["AC", "AC"]

    channels.coupling(Coupling.DC)
    assert channels.coupling() == ["DC", "DC"]


def test_channel_impedance():
    pytest.skip(reason="This doesn't seem to work")

    channel.impedance(Impedance.ONE_MEG)
    assert channel.impedance() == "ONEMeg"

    channel.impedance(Impedance.FIFTY)
    assert channel.impedance() == "FIFTy"


def test_channels_impedance():
    pytest.skip(reason="This doesn't seem to work")

    channels.impedance(Impedance.ONE_MEG)
    assert channels.impedance() == ["ONEMeg", "ONEMeg"]

    channels.impedance(Impedance.FIFTY)
    assert channels.impedance() == ["FIFTy", "FIFTy"]


def test_channel_invert():
    channel.invert(True)
    assert channel.invert() == "ON"

    channel.invert(False)
    assert channel.invert() == "OFF"


def test_channels_invert():
    channels.invert(True)
    assert channels.invert() == ["ON", "ON"]

    channels.invert(False)
    assert channels.invert() == ["OFF", "OFF"]


def test_channel_label():
    pytest.skip(reason="This doesn't seem to work")
    channel.label(True)
    assert channel.label() == "OFF"

    channel.label(True)
    assert channel.label() == "ON"


def test_channels_label():
    pytest.skip(reason="This doesn't seem to work")
    channels.label(True)
    assert channels.label() == ["ON", "ON"]

    channels.label(False)
    assert channels.label() == ["OFF", "OFF"]


def test_channel_labelText():
    channel.labelText("A")
    assert channel.labelText() == "A"

    channel.labelText("B")
    assert channel.labelText() == "B"


def test_channels_labelText():
    channels.labelText("A")
    assert channels.labelText() == ["A", "A"]

    channels.labelText("B")
    assert channels.labelText() == ["B", "B"]


def test_channel_visible():
    channel.visible(True)
    assert channel.visible() == "ON"

    channel.visible(False)
    assert channel.visible() == "OFF"


def test_channels_visible():
    channels.visible(True)
    assert channels.visible() == ["ON", "ON"]

    channels.visible(False)
    assert channels.visible() == ["OFF", "OFF"]


def test_channel_OFFSet():
    pytest.fail()
    channel.offset()


def test_channels_OFFSet():
    pytest.fail()
    channels.offset()


def test_channel_PROBe():
    pytest.fail()
    channel.probe()


def test_channels_PROBe():
    pytest.fail()
    channels.probe()


def test_channel_SCALe():
    pytest.fail()
    channel.scale()


def test_channels_SCALe():
    pytest.fail()
    channels.scale()


def test_channel_SKEW():
    pytest.fail()
    channel.skew()


def test_channels_SKEW():
    pytest.fail()
    channels.skew()


def test_channel_SWITch():
    pytest.fail()
    channel.switch()


def test_channels_SWITch():
    pytest.fail()
    channels.switch()


def test_channel_UNIT():
    pytest.fail()
    channel.unit()


def test_channels_UNIT():
    pytest.fail()
    channels.unit()
