from tests import scope
from instrumentation.siglent.scope import BWLimit


def test_channel_bwLimit():
    channel = scope.channel(1)

    channel.bwLimit(BWLimit.BWL_200M)
    assert channel.bwLimit() == "FULL"

    channel.bwLimit(BWLimit.BWL_20M)
    assert channel.bwLimit() == "20M"


def test_channels_bwLimit():
    channels = scope.channels([1, 2, 3, 4])

    channels.bwLimit(BWLimit.BWL_200M)
    assert channels.bwLimit() == ["FULL", "FULL", "FULL", "FULL"]

    channels.bwLimit(BWLimit.BWL_20M)
    assert channels.bwLimit() == ["20M", "20M", "20M", "20M"]
