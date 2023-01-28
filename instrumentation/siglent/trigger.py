from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Trigger(Commandable):
    """
    The TRIGGER subsystem controls the trigger modes and parameters for each
    trigger type.

    (Pg. 191)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] SET50
        - [ ] TRCP
        - [ ] TRLV
        - [ ] TRLV2
        - [ ] TRMD
        - [ ] TRPA
        - [ ] TRSE
        - [ ] TRSL
        - [ ] TRWI

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
