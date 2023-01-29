from time import sleep
from instrumentation.JDS6600.awg import Freq, WaveForm
from tests import scope, awg


def setup_awg():
    awg_chan = awg.channel(1)
    awg_chan.waveForm(WaveForm.SINE)
    awg_chan.frequency(Freq.Hz(100))
    awg_chan.offset(0.0)
    awg_chan.amplitude(1.0)


def test_measure_cymometer():
    setup_awg()
    scope.reset()
    scope.auto_setup()
    sleep(5)
    result = scope.measure.cymometer()
    assert result.unit == "Hz"
    assert result.value > 99.0
    assert result.value < 101.0
