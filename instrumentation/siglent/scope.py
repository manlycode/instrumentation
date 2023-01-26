from enum import Enum
from typing import Optional

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


class Flag(Enum):
    ON = "ON"
    OFF = "OFF"

    @staticmethod
    def fromBool(val: Optional[bool] = None):
        if val is False:
            return Flag.OFF

        if val is True:
            return Flag.ON

        return None


class Channel:
    def __init__(self, number: int, resource) -> None:
        self.number = number
        self.resource: USBInstrument = resource
        self.chanCmdRoot = f":CHANnel{self.number}"

    def __dispatch_enum(self, cmdRoot: str, arg):
        if arg is None:
            return self.__dispatch_string(cmdRoot, None)

        else:
            return self.__dispatch_string(cmdRoot, arg.value)

    def __dispatch_quoted_string(self, cmdRoot: str, arg):
        if arg is None:
            cmd = f"{cmdRoot}?"
            return self.resource.query(cmd).rstrip().strip('"')

        else:
            cmd = f'{cmdRoot} "{arg}"'
            self.resource.write(cmd)
            return None

    def __dispatch_string(self, cmdRoot: str, arg):
        if arg is None:
            cmd = f"{cmdRoot}?"
            print(f"query.cmd: {cmd}")
            return self.resource.query(cmd).rstrip()

        else:
            cmd = f"{cmdRoot} {arg}"
            print(f"write.cmd: {cmd}")
            print(self.resource.write(cmd))
            return None

    def bwLimit(self, limit: Optional[BWLimit] = None) -> str:
        cmdRoot = f"{self.chanCmdRoot}:BWLimit"
        return self.__dispatch_enum(cmdRoot, limit)

    def coupling(self, cpl: Optional[Coupling] = None):
        cmdRoot = f"{self.chanCmdRoot}:COUPling"
        return self.__dispatch_enum(cmdRoot, cpl)

    def impedance(self, imp: Optional[Impedance] = None):
        # NOTE: SDS1104X-U only provides ONEMeg
        cmdRoot = f"{self.chanCmdRoot}:IMPedance"
        return self.__dispatch_enum(cmdRoot, imp)

    def invert(self, inv: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:INVert"
        return self.__dispatch_enum(cmdRoot, Flag.fromBool(inv))

    def label(self, state: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:LABel"
        flag = Flag.fromBool(state)
        return self.__dispatch_enum(cmdRoot, flag)

    def labelText(self, label: Optional[str] = None):
        cmdRoot = f"{self.chanCmdRoot}:LABel:TEXT"
        return self.__dispatch_quoted_string(cmdRoot, label)

    def visible(self, state: Optional[bool] = None):
        cmdRoot = f"{self.chanCmdRoot}:VIS"
        return self.__dispatch_enum(cmdRoot, Flag.fromBool(state))


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
        return list(map(lambda x: x.invert(vis), self.channels))


class Scope:
    RESOURCE_ID = "USB0::0xF4EC::0x1012::SDSAHBAQ6R1188::INSTR"

    def __init__(self, resource: USBInstrument) -> None:
        self.resource = resource

    def write(self, msg: str):
        self.resource.write(msg)

    def query(self, msg: str) -> str:
        return self.resource.query(msg)

    def channel(self, number: int) -> Channel:
        return Channel(number, self.resource)

    def channels(self, numbers: list[int]) -> ChannelList:
        return ChannelList(self.resource, numbers)
