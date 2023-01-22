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


# def test_channel_impedance():
#     channel.impedance(Impedance.ONE_MEG)
#     assert channel.impedance() == "ONEMeg"

#     channel.impedance(Impedance.FIFTY)
#     assert channel.impedance() == "FIFTy"


# def test_channels_impedance():
#     channels.impedance(Impedance.ONE_MEG)
#     assert channels.impedance() == ["ONEMeg", "ONEMeg"]

#     channels.impedance(Impedance.FIFTY)
#     assert channels.impedance() == ["FIFTy", "FIFTy"]


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
