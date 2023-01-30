# -*- coding: utf-8 -*-

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Digital(Commandable):
    """
    The DIGITAL subsystem commands control the viewing of digital channels.
    They also control threshold settings for groups of digital channels.
    (Pg. 72)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] DGCH
        - [ ] DGST
        - [ ] DGTH
        - [ ] DI:SW
        - [ ] TRA
        - [ ] TSM
        - [ ] CUS
    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
