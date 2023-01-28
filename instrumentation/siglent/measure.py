from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Measure(Commandable):
    """
    The commands in the MEASURE subsystem are used to make parametric
    measurements on displayed waveforms.

    To make a measurement, the portion of the waveform required for that
    measurement must be displayed on the oscilloscope screen.
    (Pg. 113)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] CYMT?
        - [ ] MEAD
        - [ ] PACU
        - [ ] PAVA?
        - [ ] PASTAT
        - [ ] MEACL
        - [ ] MEGS
        - [ ] MEGA
        - [ ] MEGB


    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
