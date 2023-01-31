from time import sleep

import pyvisa

from instrumentation.JDS6600.awg import Freq

from ..JDS6600 import AWG, WaveForm
from ..siglent import Coupling, Scope

rm = pyvisa.ResourceManager()


def build_awg() -> AWG:
    res = rm.open_resource(AWG.RESOURCE_ID)
    res.baud_rate = AWG.BAUD_RATE  # type: ignore
    return AWG(res)  # type: ignore


def build_scope() -> Scope:
    res = rm.open_resource(Scope.RESOURCE_ID)
    return Scope(res)  # type: ignore


def runScript():

    scope_resource = rm.open_resource(Scope.RESOURCE_ID)
    scope = Scope(scope_resource)

    awg_res = rm.open_resource(AWG.RESOURCE_ID)
    awg_res.baud_rate = AWG.BAUD_RATE

    awg = AWG(awg_res)

    # Setup Scope
    scope.reset()
    sleep(5)
    scope_channels = scope.channels([1, 2])

    scope_channels.switch(True)
    scope_channels.coupling(Coupling.AC)

    # Setup Waves
    awg.channel(1).frequency(Freq.Hz(10))
    awg.channel(1).waveForm(WaveForm.SINE)
    awg.channel(1).offset(0.0)
    awg.channel(1).amplitude(1.0)
