from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class Display(Commandable):
    """
    The DISPLAY subsystem is used to control how waveforms, and the graticules
    are displayed on the screen.
    (Pg. 82)

    Args:
        Commandable (_type_): _description_

    TODO:
        -DTJN
        -GRDS
        -INTS
        -MENU
        -PESU

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
