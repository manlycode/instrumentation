from time import sleep
from instrumentation.JDS6600.awg import Freq

import pyvisa

from ..JDS6600 import AWG, WaveForm
from ..siglent import BWLimit, Coupling, Scope


def runScript():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

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
    scope_channels.bwLimit(BWLimit.BWL_20M)
    scope_channels.coupling(Coupling.AC)

    # Setup Waves
    awg.channel(1).frequency(Freq.Hz(10))
    awg.channel(1).waveForm(WaveForm.SINE)
    awg.channel(1).amplitude(2.0)
