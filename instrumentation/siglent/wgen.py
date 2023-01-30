# -*- coding: utf-8 -*-

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class WGen(Commandable):
    """
    When the built-in waveform generator is licensed (Option AWG), you can use
    it to output sine, square, ramp, pulse, DC, noise, exponential rise,
    exponential fall, cardiac, Gaussian pulse and arbitrary waveforms. The
    WGEN commands are used to select the waveform function and parameters.
    (Pg. 275)

    Args:
        Commandable (_type_): _description_

    TODO:
         - [ ] ARWV
         - [ ] PROD?
         - [ ] STL?
         - [ ] WGEN
         - [ ] WVPR?

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
