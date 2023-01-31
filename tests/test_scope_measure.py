# -*- coding: utf-8 -*-

from time import sleep
from instrumentation.siglent.channel import Coupling
from instrumentation.siglent.measure import MDType
import pytest
from instrumentation.JDS6600.awg import Freq, WaveForm
from tests import scope, awg


def setup_awg():
    awg_chan = awg.channel(1)
    awg_chan.waveForm(WaveForm.SINE)
    awg_chan.frequency(Freq.Hz(100))
    awg_chan.offset(0.0)
    awg_chan.amplitude(1.0)


def setup_dual_awg():
    awg_chans = awg.channels([1, 2])
    awg_chans.waveForm(WaveForm.SINE)
    awg_chans.frequency(Freq.Hz(100))
    awg_chans.offset(0.0)
    awg_chans.amplitude(1.0)


def test_measure_cymometer():
    pytest.skip()
    setup_awg()
    scope.reset()
    scope.auto_setup()
    sleep(5)
    result = scope.measure.cymometer()
    assert result.unit == "Hz"
    assert result.value > 99.0
    assert result.value < 101.0


def test_measure_delay():
    setup_dual_awg()
    awg.enable_channels(True, True)
    awg.channel(2).phase(180)
    scope.channels([1, 2]).coupling(Coupling.A1M)
    scope.auto_setup()
    sleep(2)
    response = scope.measure.measure_delay(MDType.PHA, 1, 2)
    assert response.value > 179.0
    assert response.value < 181.0

    response = scope.measure.measure_delay(MDType.FFF, 1, 2)
