# -*- coding: utf-8 -*-
from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Acquire(Commandable):
    """
    The ACQUIRE subsystem controls the way in which waveforms are acquired.
    These commands set the parameters for acquiring and storing data.
    (Pg. 24)

    Args:
        Commandable (_type_): _description_

    TODO:
        - ARM
        - STOP
        - ACQW
        - AVGA
        - MSIZ
        - SAST?
        - SARA?
        - SANU?
        - SXSA
        - XYDS

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
