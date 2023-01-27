from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Save(Commandable):
    """
    Save oscilloscope setups and waveform data.
    (Pg. 165)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] *SAV
        - [ ] PNSU
        - [ ] STPN

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
