import pyvisa
from time import sleep

from ..siglent import (
    Scope,
    BWLimit,
)

from ..JDS6600 import (
    AWG,
)


def runScript():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    # scope = rm.open_resource("USB0::0xF4EC::0x1012::SDSAHBAQ6R1188::INSTR")
    scope = Scope(rm)

    sleep(0.1)
    awg = rm.open_resource("ASRL1::INSTR")
    awg.baud_rate = 115200
    awg = AWG(rm)

    # For communication with the device, the baud rate must be set to 115200,
    # 8 data bits, 1 stop bit and no parity bit are required.

    print(scope.query("*IDN?"))

    # Set the bandwith limit for all channels
    # scope.write(":CHAN1:BWLimit 20M")
    # scope.write(":CHAN2:BWLimit 20M")
    # scope.write(":CHAN3:BWLimit 20M")
    # scope.write(":CHAN4:BWLimit 20M")

    for i in [1, 2, 3, 4]:
        scope.write(f':CHAN{i}:BWLimit 20M')

    # for i in [1,2,3,4]:
        # print(scope.query(f':CHAN{i}:BWLimit?'))

    scope.channel(1).bwLimit(BWLimit.BWL_20M)
    print(scope.channel(1).bwLimit())

    channels = scope.channels([1, 2, 3, 4])
    print(channels.bwLimit())

    # awg.write(":w21=3.")
    # awg.write(":w23=25786,0.")

    # print(awg.channels([1, 2]).waveForm())
    # awg.channels([1, 2]).waveForm(WaveForm.HALF_WAVE)

    # awg.channels([1,2]).frequency(Freq.uHz(557.86))

    # print(Freq.kHz(0.5786))
    # print(Freq.MHz(0.00025786))
    # print(Freq.mHz(257.86))
    # print(Freq.uHz(257.86))

    print(scope.channel(1).labelText())
    scope.channel(1).label(True)
    scope.channel(1).labelText("Bart")

    print(scope.channel(1).labelText())
    scope.channel(1).label(False)
    scope.channel(1).bwLimit(BWLimit.BWL_20M)

    print(scope.channels([1, 2]).labelText())
