from enum import Enum
from typing import Optional
from instrumentation.siglent.commandable import Commandable, Flag
from instrumentation.siglent.measure import Measure
from pyvisa.resources.usb import USBInstrument


class BWLimit(Enum):
    BWL_20M = "20M"
    BWL_200M = "200M"
    BWL_FULL = "FULL"


class Coupling(Enum):
    AC = "AC"
    DC = "DC"
    GND = "GND"


class Impedance(Enum):
    ONE_MEG = "ONEMeg"
    FIFTY = "FIFTy"


class Channel(Commandable):
    def __init__(self, number: int, resource) -> None:
        self.number = number
        self.chanCmdRoot = f":CHANnel{self.number}"
        super().__init__(resource)

    def bwLimit(self, limit: Optional[BWLimit] = None) -> str:
        cmdRoot = f"{self.chanCmdRoot}:BWLimit"
        return self.dispatch_enum(cmdRoot, limit)

    def coupling(self, cpl: Optional[Coupling] = None):
        cmdRoot = f"{self.chanCmdRoot}:COUPling"
        return self.dispatch_enum(cmdRoot, cpl)

    def impedance(self, imp: Optional[Impedance] = None):
        # NOTE: SDS1104X-U only provides ONEMeg
        cmdRoot = f"{self.chanCmdRoot}:IMPedance"
        return self.dispatch_enum(cmdRoot, imp)

    def invert(self, inv: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:INVert"
        return self.dispatch_enum(cmdRoot, Flag.fromBool(inv))

    def label(self, state: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:LABel"
        flag = Flag.fromBool(state)
        return self.dispatch_enum(cmdRoot, flag)

    def labelText(self, label: Optional[str] = None):
        cmdRoot = f"{self.chanCmdRoot}:LABel:TEXT"
        return self.dispatch_quoted_string(cmdRoot, label)

    def visible(self, state: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:VIS"
        return self.dispatch_enum(cmdRoot, Flag.fromBool(state))

    def switch(self, state: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:SWITch"
        return self.dispatch_enum(cmdRoot, Flag.fromBool(state))


class ChannelList:
    def __init__(self, resource, numbers: list[int]) -> None:
        self.channels: list[Channel] = list(
            map(lambda x: Channel(x, resource), numbers)
        )

    def bwLimit(self, limit: Optional[BWLimit] = None) -> list[str]:
        return list(map(lambda x: x.bwLimit(limit), self.channels))

    def coupling(self, cpl: Optional[Coupling] = None) -> list[str]:
        return list(map(lambda x: x.coupling(cpl), self.channels))

    def impedance(self, imp: Optional[Impedance] = None) -> list[str]:
        return list(map(lambda x: x.impedance(imp), self.channels))

    def invert(self, inv: Optional[bool] = None) -> list[str]:
        return list(map(lambda x: x.invert(inv), self.channels))

    def label(self, state: Optional[bool] = None) -> list[str]:
        return list(map(lambda x: x.label(state), self.channels))

    def labelText(self, label: Optional[str] = None) -> list[str]:
        return list(map(lambda x: x.labelText(label), self.channels))

    def visible(self, vis: Optional[bool] = None) -> list[str]:
        return list(map(lambda x: x.visible(vis), self.channels))

    def switch(self, state: Optional[bool] = None) -> list[str]:
        return list(map(lambda x: x.switch(state), self.channels))


class Scope:
    RESOURCE_ID = "USB0::0xF4EC::0x1012::SDSAHBAQ6R1188::INSTR"

    def __init__(self, resource: USBInstrument) -> None:
        self.resource = resource

    def write(self, msg: str):
        self.resource.write(msg)

    def reset(self):
        return self.resource.write("*RST")

    def query(self, msg: str) -> str:
        return self.resource.query(msg)

    def channel(self, number: int) -> Channel:
        return Channel(number, self.resource)

    def measure(self) -> Measure:
        return Measure(self.resource)

    def channels(self, numbers: list[int]) -> ChannelList:
        return ChannelList(self.resource, numbers)
