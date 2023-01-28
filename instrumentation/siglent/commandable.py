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

    def toBool(self) -> bool:
        if self == Flag.ON:
            return True
        else:
            return False


class Response:
    def __init__(self, res: str) -> None:
        parts = res.rstrip().split(" ")
        self.header, self.val = parts[0], parts[1]


class Commandable:
    def __init__(self, resource) -> None:
        self.resource: USBInstrument = resource

    def dispatch_enum(self, cmdRoot: str, arg) -> Optional[Response]:
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

    def write(self, cmd: str) -> int:
        return self.resource.write(cmd)

    def query(self, cmd: str) -> Response:
        res = self.resource.query(cmd)
        return Response(res)

    def __dispatch_string(self, cmdRoot: str, arg) -> Optional[Response]:
        if arg is None:
            cmd = f"{cmdRoot}?"
            res = self.resource.query(cmd)
            return Response(res)

        else:
            cmd = f"{cmdRoot} {arg}"
            self.resource.write(cmd)
            return None
