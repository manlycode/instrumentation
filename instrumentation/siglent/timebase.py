from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Timebase(Commandable):
    """
    The TIMEBASE subsystem commands control the horizontal (X-axis) functions.

    The time per division, delay, and reference can be controlled for the main
    and window (zoomed) time bases.
    (Pg. 183)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] TDIV
        - [ ] TRDL
        - [ ] HMAG
        - [ ] HPOS

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
