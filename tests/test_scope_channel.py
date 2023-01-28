from time import sleep
from instrumentation.JDS6600.awg import Freq, WaveForm

import pytest

from tests import awg, scope
from instrumentation.siglent.channel import (
    Attenuation,
    BWLimit,
    Coupling,
    Value,
)

channel = scope.channel(1)
channels = scope.channels([3, 4])


def test_channel_attenuation():
    channel.attenuation(Attenuation._50)
    assert channel.attenuation() == Attenuation._50

    channel.attenuation(Attenuation._1)
    assert channel.attenuation() == Attenuation._1


def test_channel_bandwith_limit():
    scope.reset()
    sleep(2)

    assert scope.channel(1).bandwith_limit() is False
    assert scope.channel(2).bandwith_limit() is False
    assert scope.channel(3).bandwith_limit() is False
    assert scope.channel(4).bandwith_limit() is False

    scope.channel(1).bandwith_limit(True)
    scope.channel(2).bandwith_limit(True)
    scope.channel(3).bandwith_limit(True)
    scope.channel(4).bandwith_limit(True)

    assert scope.channel(1).bandwith_limit()
    assert scope.channel(2).bandwith_limit()
    assert scope.channel(3).bandwith_limit()
    assert scope.channel(4).bandwith_limit()

    scope.channel(1).bandwith_limit(False)
    scope.channel(2).bandwith_limit(False)
    scope.channel(3).bandwith_limit(False)
    scope.channel(4).bandwith_limit(False)

    assert scope.channel(1).bandwith_limit() is False
    assert scope.channel(2).bandwith_limit() is False
    assert scope.channel(3).bandwith_limit() is False
    assert scope.channel(4).bandwith_limit() is False


def xtest_channel_coupling():
    channel.coupling(Coupling.AC)
    assert channel.coupling() == "AC"

    channel.coupling(Coupling.DC)
    assert channel.coupling() == "DC"


def xtest_channels_coupling():
    channels.coupling(Coupling.AC)
    assert channels.coupling() == ["AC", "AC"]

    channels.coupling(Coupling.DC)
    assert channels.coupling() == ["DC", "DC"]


def xtest_channel_invert():
    channel.invert(True)
    assert channel.invert() == "ON"

    channel.invert(False)
    assert channel.invert() == "OFF"


def xtest_channels_invert():
    channels.invert(True)
    assert channels.invert() == ["ON", "ON"]

    channels.invert(False)
    assert channels.invert() == ["OFF", "OFF"]


def xtest_channel_label():
    pytest.skip(reason="This doesn't seem to work")
    channel.label(True)
    assert channel.label() == "OFF"

    channel.label(True)
    assert channel.label() == "ON"


def xtest_channels_label():
    pytest.skip(reason="This doesn't seem to work")
    channels.label(True)
    assert channels.label() == ["ON", "ON"]

    channels.label(False)
    assert channels.label() == ["OFF", "OFF"]


def xtest_channel_labelText():
    channel.labelText("A")
    assert channel.labelText() == "A"

    channel.labelText("B")
    assert channel.labelText() == "B"


def xtest_channels_labelText():
    channels.labelText("A")
    assert channels.labelText() == ["A", "A"]

    channels.labelText("B")
    assert channels.labelText() == ["B", "B"]


def xtest_channel_visible():
    channel.visible(True)
    assert channel.visible() == "ON"

    channel.visible(False)
    assert channel.visible() == "OFF"


def xtest_channels_visible():
    channels.visible(True)
    assert channels.visible() == ["ON", "ON"]

    channels.visible(False)
    assert channels.visible() == ["OFF", "OFF"]


def xtest_channel_parameter_value():
    awg.channel(1).waveForm(WaveForm.SINE)
    awg.channel(1).frequency(Freq.Hz(100))
    awg.channel(1).offset(0.0)
    awg.channel(1).amplitude(1.0)

    scope.channel(1).switch(True)
    scope.auto_setup()

    sleep(2)
    print(channel.parameter_value(Value.PKPK))
    print(channel.parameter_value(Value.AMPL))
    print(channel.parameter_value(Value.FREQ))
