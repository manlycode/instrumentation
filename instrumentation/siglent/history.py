# -*- coding: utf-8 -*-

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class History(Commandable):
    """
    The HISTORY subsystem commands control the waveform recording function and
    the history waveform play function.
    (Pg. 88)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] FRAM
        - [ ] FTIM?
        - [ ] HSMD
        - [ ] HSLST

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
