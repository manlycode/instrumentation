# -*- coding: utf-8 -*-

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Reference(Commandable):
    """
    The REFERENCE system controls the reference waveforms.
    (Pg. 154)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] REFCL
        - [ ] REFDS
        - [ ] REFLA
        - [ ] REFPO
        - [ ] REFSA
        - [ ] REFSC
        - [ ] REFSR

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
