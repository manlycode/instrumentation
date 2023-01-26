from instrumentation.siglent.commandable import Commandable
from pyvisa.resources.usb import USBInstrument


class Measure(Commandable):
    def __init__(self, resource) -> None:
        self.resource: USBInstrument = resource
        self.chanCmdRoot = ":MEASure"

    def enable(self):
        pass
