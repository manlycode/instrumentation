from enum import Enum
from typing import Optional

from pyvisa.resources.usb import USBInstrument


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


class Commandable:
    def __init__(self, resource) -> None:
        self.resource: USBInstrument = resource

    def dispatch_enum(self, cmdRoot: str, arg):
        if arg is None:
            return self.__dispatch_string(cmdRoot, None)

        else:
            return self.__dispatch_string(cmdRoot, arg.value)

    def dispatch_quoted_string(self, cmdRoot: str, arg):
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
