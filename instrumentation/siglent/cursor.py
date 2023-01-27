from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Cursor(Commandable):
    """
    The CURSOR subsystem commands set and query the settings of X-axis markers
    (X1 and X2 cursors) and the Y-axis markers (Y1 and Y2 cursors). You can set
    and query the marker mode and source, the position of X and Y cursors, and
    query delta X and delta Y cursor values.

    (Pg. 51)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] CRMS
        - [ ] CRST
        - [ ] CRTY
        - [ ] CRVA?

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
