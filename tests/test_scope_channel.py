# -*- coding: utf-8 -*-

from time import sleep

from tests import scope
from instrumentation.siglent.channel import (
    Attenuation,
    Coupling,
    Voltage,
    Skew,
    Unit,
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
    channel.offset(Voltage.V(-3.0))
    result = channel.offset()
    assert result.value == float(-3.0)
    assert result.unit == "V"

    channel.offset(Voltage.mV(500.0))
    result = channel.offset()
    assert result.value == float(0.5)
    assert result.unit == "V"

    channel.offset(Voltage.mV(0.0))
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
    channel.trace(False)
    assert channel.trace() is False

    channel.trace(True)
    assert channel.trace()


def test_channel_unit():
    channel.unit(Unit.A)
    assert channel.unit() == Unit.A

    channel.unit(Unit.V)
    assert channel.unit() == Unit.V


def test_channel_volt_div():
    channel.trace(True)
    channel.volt_div(Voltage.mV(50))
    assert channel.volt_div() == Voltage.V(0.05)

    channel.volt_div(Voltage.V(1))
    assert channel.volt_div() == Voltage.V(1)


def test_channel_invert():
    channel.invert(True)
    assert channel.invert()

    channel.invert(False)
    assert channel.invert() is False
