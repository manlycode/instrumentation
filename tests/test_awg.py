from time import sleep

from tests import awg
from instrumentation.JDS6600.awg import WaveForm

channel = awg.channel(1)
channels = awg.channels([1, 2])


def test_channel_waveForm():
    channel.waveForm(WaveForm.SINE)
    assert channel.waveForm() == ":r21=0."

    channel.waveForm(WaveForm.SQUARE)
    assert channel.waveForm() == ":r21=1."


def test_channels_waveForm():
    channels.waveForm(WaveForm.SINE)
    assert channels.waveForm() == [":r21=0.", ":r22=0."]

    channels.waveForm(WaveForm.SQUARE)
    assert channels.waveForm() == [":r21=1.", ":r22=1."]
