from time import sleep
from instrumentation.JDS6600.awg import Freq, WaveForm

import pytest

from tests import awg, scope
from instrumentation.siglent.channel import (
    Attenuation,
    Coupling,
    Offset,
    Skew,
    Unit,
    Value,
)

channel = scope.channel(1)
channels = scope.channels([3, 4])


def test_channel_attenuation():
    channel.attenuation(Attenuation._50)
    assert channel.attenuation() == Attenuation._50

    channel.attenuation(Attenuation._1)
    assert channel.attenuation() == Attenuation._1

    assert channels.attenuation() == [Attenuation._1, Attenuation._1]


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

    scope.channels([1, 2, 3, 4]).bandwith_limit(False)
    assert scope.channels([1, 2, 3, 4]).bandwith_limit() == [
        False,
        False,
        False,
        False,
    ]


def test_channel_coupling():
    channel.coupling(Coupling.A1M)
    assert channel.coupling() == Coupling.A1M

    # NOTE: Cannot use 50 ohm coupling on my model
    channel.coupling(Coupling.D1M)
    assert channel.coupling() == Coupling.D1M
    assert channels.coupling() == [Coupling.D1M, Coupling.D1M]


def test_channel_offset():
    channel.offset(Offset.V(-3.0))
    result = channel.offset()
    assert result.value == float(-3.0)
    assert result.unit == "V"

    channel.offset(Offset.mV(500.0))
    result = channel.offset()
    assert result.value == float(0.5)
    assert result.unit == "V"

    channel.offset(Offset.mV(0.0))
    result = channel.offset()
    assert result.value == float(0.0)
    assert result.unit == "V"


def test_channel_skew():
    channel.skew(Skew.nS(-3.0))
    result = channel.skew()
    assert result.value == float("-3.0E-09")
    assert result.unit == "S"

    channel.skew(Skew.nS(0))
    result = channel.skew()
    assert result.value == float(0.0)
    assert result.unit == "S"


def test_channel_trace():
    channel.trace(True)
    assert channel.trace()

    channel.trace(False)
    assert channel.trace() is False


def test_channel_unit():
    channel.unit(Unit.A)
    assert channel.unit() == Unit.A

    channel.unit(Unit.V)
    assert channel.unit() == Unit.V


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
