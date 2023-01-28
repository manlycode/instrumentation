from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class PassFail(Commandable):
    """
    The PASS/FAIL subsystem commands and queries control the mask test
    features.
    (Pg. 135)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] PACL
        - [ ] PFBF
        - [ ] PFCM
        - [ ] PFDD
        - [ ] PFDS
        - [ ] PFEN
        - [ ] PFFS
        - [ ] PFOP
        - [ ] PFSC
        - [ ] PFST
    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
