from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class System(Commandable):
    """
    The SYSTEM subsystem commands control basic system functions of the
    oscilloscope.
    (Pg. 177)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] *CAL?
        - [ ] BUZZ
        - [ ] CONET
        - [ ] SCSV
        - [ ] EMOD

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
