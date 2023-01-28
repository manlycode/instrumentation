from enum import Enum, auto
from typing import Optional

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable, Flag


class ScopeId:
    def __init__(self, response: str):
        """
        Initialized ScopeId

        Args:
            response (str): String response from *IDC? query
        """
        splitResponse = response.strip().split(",")
        self.manufacturer = splitResponse[0]
        self.model = splitResponse[1]
        self.serial_num = splitResponse[2]
        self.firmware = splitResponse[3]


class HeaderMode(Enum):
    SHORT = "SHORT"
    LONG = "LONG"
    OFF = "OFF"


class Value(Enum):
    PKPK = auto()
    MAX = auto()
    MIN = auto()
    AMPL = auto()
    TOP = auto()
    BASE = auto()
    CMEAN = auto()
    MEAN = auto()
    RMS = auto()
    CRMS = auto()
    OVSN = auto()
    FPRE = auto()
    OVSP = auto()
    RPRE = auto()
    PER = auto()
    FREQ = auto()
    PWID = auto()
    NWID = auto()
    RISE = auto()
    FALL = auto()
    WID = auto()
    DUTY = auto()
    NDUTY = auto()
    ALL = auto()


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
    """
    The CHANNEL subsystem commands control the analog channels. Channels
    areindependently programmable for offset, probe, coupling, bandwidth
    limit, inversion, and more functions. The channel index (1, 2, 3, or 4)
    specified in the command selects the analog channel that is affected by
    the command.

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] ATTN
        - [ ] BWL
        - [ ] CPL
        - [ ] OFST
        - [ ] SKEW
        - [ ] TRA
        - [ ] UNIT
        - [ ] VDIV
        - [ ] INVS


    """

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

    def parameter_value(self, value: Value):
        cmd = f":C{self.number}:PARAMETER_VALUE? {value.name}"
        result = self.resource.query(cmd)
        split_result = str.split(result, ",")[1]
        print(split_result)

        return self.resource.query(cmd)


class ChannelList:
    def __init__(self, resource, numbers: list[int]) -> None:
        self.channels: list[Channel] = list(
            map(lambda x: Channel(x, resource), numbers)
        )

    def bwLimit(self, limit: Optional[BWLimit] = None) -> list[str]:
        return list(map(lambda x: x.bwLimit(limit), self.channels))

    def coupling(self, cpl: Optional[Coupling] = None) -> list[str]:
        return list(map(lambda x: x.coupling(cpl), self.channels))

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


class Scope(Commandable):
    """
    Root object for

    Args:
        Commandable (_type_): _description_

    Returns:
        _type_: _description_

    TODO:
        - [✅] *IDN?(IdentificationNumber)
        - [✅] *OPC(OperationComplete)
        - [✅] *RST(Reset)
        (Pg. 18)

        - [ ] SCDP
        (Pg. 148)

        - [ ] *RCL
        - [ ] RCPN
        (Pg. 150)

        - [ ] INR? (Page 174)

    """

    RESOURCE_ID = "USB0::0xF4EC::0x1012::SDSAHBAQ6R1188::INSTR"

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)

    def write(self, msg: str):
        self.resource.write(msg)

    def query(self, msg: str) -> str:
        return self.resource.query(msg)

    def channel(self, number: int) -> Channel:
        return Channel(number, self.resource)

    def channels(self, numbers: list[int]) -> ChannelList:
        return ChannelList(self.resource, numbers)

    def comm_header(self, mode: Optional[HeaderMode] = None) -> str:
        return super().dispatch_enum("CHDR", mode)

    def auto_setup(self):
        super().write("ASET")

    def idn(self) -> ScopeId:
        """
        The *IDN? query identifies the instrument type and software version.
        The response consists of four different fields providing information
        on the manufacturer, the scope model, the serial number and the
        firmware revision.

        Returns:
            ScopeId: Identifying information for a scope
        """
        res = super().query("*IDN?")
        return ScopeId(res)

    def opc(self, isCommand: bool = False) -> Optional[int]:
        """
        The *OPC command sets the operation complete bit in the Standard Event
        Status Register when all pending device operations have finished.

        The *OPC? query places an ASCII "1" in the output queue when all
        pending device operations have completed. The interface hangs until
        this query returns.

        Args:
            isCommand (bool, optional): Set to true to send as a command. Set
            to false to send as a query.

            Defaults to False.

        Returns:
            Optional[int]: Result of query when sent as query.
        """
        cmd = "*OPC"
        if isCommand:
            super().write(cmd)
            return None

        else:
            res = super().query(f"{cmd}?").strip()
            return int(res)

    def reset(self):
        """
        The *RST command initiates a device reset. This is the same as pressing
        `Default` on the front panel.
        """
        return self.resource.write("*RST")
