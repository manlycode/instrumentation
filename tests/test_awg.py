import pytest

from tests import awg
from instrumentation.JDS6600.awg import WaveForm, Freq

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


def test_channel_frequency():
    channel.frequency(Freq.kHz(0.5786))
    assert channel.frequency() == ":r23=5786,1."

    channel.frequency(Freq.MHz(0.00025786))
    assert channel.frequency() == ":r23=25786,2."

    channel.frequency(Freq.mHz(257.86))
    assert channel.frequency() == ":r23=25786,3."

    channel.frequency(Freq.uHz(257.86))
    assert channel.frequency() == ":r23=25786,4."


def test_channels_phase():
    # You can't call that on channel 1
    with pytest.raises(RuntimeError):
        channel.phase(10.0)

    assert awg.channel(2).phase(10.0) == ":ok"
    assert awg.channel(2).phase() == ":r31=100."


def test_channels_amplitude():
    channel.amplitude(0.03)
    assert channel.amplitude() == ":r25=30."
