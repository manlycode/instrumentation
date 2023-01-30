# -*- coding: utf-8 -*-

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Math(Commandable):
    """
    The MATH subsystem controls the math functions in the oscilloscope. As
    selected by the DEF command, these math functions are available:

    Operators: Add, Subtract, Multiply, Divide. Operators perform their
    function on two analog channel sources.

    Transforms: DIFF, Integrate, FFT, SQRT.
    (Pg. 95)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] DEF
        - [ ] INVS
        - [ ] MTVD
        - [ ] MTVP
        - [ ] FFTC
        - [ ] FFTF
        - [ ] FFTP
        - [ ] FFTS
        - [ ] FFTT?
        - [ ] FFTU
        - [ ] FFTW

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
