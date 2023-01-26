from typing import Optional
from instrumentation.siglent.commandable import Commandable, Flag
from pyvisa.resources.usb import USBInstrument


class Measure(Commandable):
    def __init__(self, resource) -> None:
        self.resource: USBInstrument = resource
        self.cmdRoot = ":MEASure"
        super().__init__(resource)

    def enable(self, state: Optional[bool] = None) -> Optional[str]:
        return self.dispatch_enum(self.cmdRoot, Flag.fromBool(state))