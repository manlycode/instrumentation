from enum import Enum
from typing import Optional
from instrumentation.siglent.commandable import Commandable, Flag
from pyvisa.resources.usb import USBInstrument


class Source(Enum):
    C1 = "C1"
    C2 = "C2"


class Simple(Commandable):
    def __init__(self, resource) -> None:
        self.resource: USBInstrument = resource
        self.cmdRoot = ":MEASure:SIMPle"
        super().__init__(resource)

    def source(self, source: Optional[Source] = None) -> Optional[str]:
        cmd = f"{self.cmdRoot}:SOUR"
        return self.dispatch_enum(cmd, source)


class Measure(Commandable):
    def __init__(self, resource) -> None:
        self.resource: USBInstrument = resource
        self.cmdRoot = ":MEASure"
        self.simple = Simple(self.resource)
        super().__init__(resource)

    def enable(self, state: Optional[bool] = None) -> Optional[str]:
        return self.dispatch_enum(self.cmdRoot, Flag.fromBool(state))
