from enum import Enum, auto
from typing import Optional

from instrumentation.siglent.commandable import Commandable, Flag


class Attenuation(Enum):
    _0_1 = "0.1"
    _0_2 = "0.2"
    _0_5 = "0.5"
    _1 = "1"
    _2 = "2"
    _5 = "5"
    _10 = "10"
    _20 = "20"
    _50 = "50"
    _100 = "100"
    _200 = "200"
    _500 = "500"
    _1000 = "1000"
    _2000 = "2000"
    _5000 = "5000"
    _10000 = "10000"


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
        - [✅] ATTN
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
        self.cmdRoot = f"C{self.number}"
        super().__init__(resource)

    def attenuation(
        self, attn: Optional[Attenuation] = None
    ) -> Optional[Attenuation]:
        """
        The ATTENUATION command specifies the probe attenuation factor for the
        selected channel. The probe attenuation factor may be 0.1 to 10000.

        This command does not change the actual input sensitivity of the
        oscilloscope. It changes the reference constants for scaling the
        display factors, for making automatic measurements, and for setting
        trigger levels.

        The ATTENUATION? query returns the current probe attenuation factor for
        the selected channel.

        Args:
            attn (Optional[Attenuation], optional): _description_. Defaults to
            None.

        Returns:
            Optional[Attenuation]: _description_
        """
        cmd = f"{self.cmdRoot}:ATTENUATION"
        res = self.dispatch_enum(cmd, attn)

        if attn is not None:
            return None

        else:
            resVal = res.strip().split(" ")[1]
            return Attenuation(resVal)

    def bwLimit(self, limit: Optional[BWLimit] = None) -> str:
        cmd = f"{self.cmdRoot}:BWLimit"
        return self.dispatch_enum(cmd, limit)

    def coupling(self, cpl: Optional[Coupling] = None):
        cmd = f"{self.cmdRoot}:COUPling"
        return self.dispatch_enum(cmd, cpl)

    def invert(self, inv: Optional[bool] = None):
        cmd = f"{self.cmdRoot}:INVert"
        return self.dispatch_enum(cmd, Flag.fromBool(inv))

    def label(self, state: Optional[bool] = None):
        cmd = f"{self.cmdRoot}:LABel"
        flag = Flag.fromBool(state)
        return self.dispatch_enum(cmd, flag)

    def labelText(self, label: Optional[str] = None):
        cmd = f"{self.cmdRoot}:LABel:TEXT"
        return self.dispatch_quoted_string(cmd, label)

    def visible(self, state: Optional[bool] = None):
        cmd = f"{self.cmdRoot}:VIS"
        return self.dispatch_enum(cmd, Flag.fromBool(state))

    def switch(self, state: Optional[bool] = None):
        cmd = f"{self.cmdRoot}:SWITch"
        return self.dispatch_enum(cmd, Flag.fromBool(state))

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
