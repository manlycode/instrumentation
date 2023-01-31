# -*- coding: utf-8 -*-

from enum import Enum, auto
from typing import Optional

from instrumentation.siglent.commandable import Commandable, Flag
from instrumentation.siglent.si_value import SIValue


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


class Coupling(Enum):
    A1M = "A1M"
    A50 = "A50"
    D1M = "D1M"
    D50 = "D50"
    GND = "GND"


class Voltage(SIValue):
    @classmethod
    def V(cls, value: float):
        return cls(value, "V")

    @classmethod
    def mV(cls, value: float):
        return cls(value, "mV")

    @classmethod
    def uV(cls, value: float):
        return cls(value, "uV")


class Skew(SIValue):
    @classmethod
    def nS(cls, value: float):
        return cls(value, "NS")


class Unit(Enum):
    V = "V"
    A = "A"


class Channel(Commandable):
    """
    The CHANNEL subsystem commands control the analog channels. Channels
    areindependently programmable for offset, probe, coupling, bandwidth
    limit, inversion, and more functions. The channel index (1, 2, 3, or 4)
    specified in the command selects the analog channel that is affected by
    the command.

    Args:
        Commandable (_type_): _description_

    Supports the following SYCPI Channel commands (See pg. 40)
        - ATTN
        - BWL
        - CPL
        - OFST
        - SKEW
        - TRA
        - UNIT
        - VDIV
        - INVS
    """

    def __init__(self, number: int, resource) -> None:
        self.number = number
        self.name = f"C{self.number}"
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
        cmd = f"{self.name}:ATTN"
        res = self.dispatch_enum(cmd, attn)

        if res is None:
            return None

        else:
            return Attenuation(res.val)

    def bandwith_limit(self, state: Optional[bool] = None) -> Optional[bool]:
        """
        BANDWIDTH_LIMIT enables or disables the bandwidth- limiting low-pass
        filter. If the bandwidth filters are on, it will limit the bandwidth to
        reduce display noise. When you turn Bandwidth Limit ON, the Bandwidth
        Limit value is set to 20 MHz. It also filters the signal to reduce
        noise and other unwanted high frequency components.

        The BANDWIDTH_LIMIT? query returns whether the bandwidth filters are
        on.

        Args:
            state (Optional[bool], optional):
                - `True` sets the bandwith limit to `20M`.
                - `False` sets the bandwith limit to `FULL`.
                - `None` queries the bandwith limit for the given channel.

        Returns:
            bool: Bandwith mode of the given channel when queried.
                - `True`: Bandwith limit == `20M`.
                - `False`: Bandwith limit == `FULL`.
        """
        cmd = "BWL"
        if state is not None:
            self.write(f"{cmd} {self.name},{Flag.fromBool(state).value}")
            return None

        else:
            res = self.query(f"{cmd}?")
            resArray = res.val.split(",")
            idx = (2 * (self.number - 1)) + 1
            flagValue = resArray[idx].strip()

            return Flag(flagValue).toBool()

    def coupling(self, cpl: Optional[Coupling] = None) -> Optional[Coupling]:
        """
        The COUPLING command selects the coupling mode of the specified input
        channel.

        The COUPLING? query returns the coupling mode of the specified channel.

        Args:
            cpl (Optional[Coupling], optional): Coupling to set.

            Defaults to None.

        Returns:
            Optional[Coupling]: Coupling of the channel
        """
        cmd = f"{self.name}:CPL"
        res = self.dispatch_enum(cmd, cpl)

        if res is not None:
            return Coupling(res.val)

        else:
            return None

    def offset(self, offset: Optional[Voltage] = None) -> Optional[Voltage]:
        """
        The OFFSET command allows adjustment of the vertical offset of the
        specified input channel. The maximum ranges depend on the fixed
        sensitivity setting.

        The OFFSET? query returns the offset value of the specified channel.

        Args:
            offset (Optional[Voltage], optional): Voltage of the channel.

            Defaults to None.

        Returns:
            Optional[Voltage]: The offset (in `V`)

        """
        cmdRoot = f"{self.name}:OFST"

        if offset is not None:
            cmd = f"{cmdRoot} {offset}"
            self.write(cmd)
            return None

        else:
            res = self.query(f"{cmdRoot}?")
            return Voltage.parse(res.val)

    def skew(self, ns: Optional[Skew] = None) -> Optional[Skew]:
        """
        The SKEW command sets the channel-to-channel skew factor for the
        specified channel. Each analog channel can be adjusted + or -100 ns for
        a total of 200 ns difference between channels. You can use the
        oscilloscope's skew control to remove cable-delay errors between
        channels.

        The SKEW? query returns the skew value of the specified trace.

        Args:
            ns (Optional[Skew], optional): Duration to skew channel.

            Defaults to None.

        Returns:
            Optional[Skew]: _description_
        """
        cmdRoot = f"{self.name}:SKEW"

        if ns is not None:
            cmd = f"{cmdRoot} {ns}"
            self.write(cmd)
            return None

        else:
            res = self.query(f"{cmdRoot}?")
            return Skew.parse(res.val)

    def trace(self, state: Optional[bool] = None) -> Optional[bool]:
        """
        The TRACE command turns the display of the specified channel on or off.

        The TRACE? query returns the current display setting for the specified
        channel.

        Args:
            state (Optional[bool], optional):
                - `True` turns the channelon.
                - `False` turns the cnannel off.
                - `None` returns the state of the channel.

            Defaults to None.

        Returns:
            Optional[bool]: _description_
        """
        cmd = f"{self.name}:TRA"
        return self.dispatch_bool(cmd, state)

    def unit(self, unit: Optional[Unit] = None) -> Optional[Unit]:
        """
        The UNIT command sets the unit of the specified trace. Measurement
        results, channel sensitivity, and trigger level will reflect the
        measurement units you select.

        The UNIT? query returns the unit of the specified trace.

        Args:
            unit (Optional[Unit], optional): Unit to change channel to.

            Defaults to None.

        Returns:
            Optional[Unit]: Unit the hannel is currently set to.
        """
        cmd = f"{self.name}:UNIT"
        res = self.dispatch_enum(cmd, unit)

        if res is not None:
            return Unit(res.val)

        return None

    def volt_div(self, v_gain: Optional[Voltage] = None) -> Optional[Voltage]:
        """
        The VOLT_DIV command sets the vertical sensitivity in Volts/div.

        If the probe attenuation is changed, the scale value is multiplied by
        the probe's attenuation factor.

        The VOLT_DIV? query returns the vertical sensitivity of the specified
        channel.

        Args:
            v_gain (Optional[Voltage], optional): Volts/Division.

            Defaults to None.

        Returns:
            Optional[Voltage]: Volts/Division.
        """
        cmdRoot = f"{self.name}:VDIV"

        if v_gain is not None:
            cmd = f"{cmdRoot} {v_gain}"
            self.write(cmd)
            return None

        else:
            res = self.query(f"{cmdRoot}?")
            return Voltage.parse(res.val)

    def invert(self, inv: Optional[bool] = None) -> Optional[bool]:
        """
        The INVERTSET command mathematically inverts the specified traces or
        the math waveform.

        The INVERTSET? query returns the current state of the channel
        inversion.


        Args:
            inv (Optional[bool], optional):
                - True: Invert the channel.
                - False: Don't invert the channel.
                - None: Query invert status

            Defaults to None.

        Returns:
            Optional[bool]: State of the channel's invert flag.
        """
        cmd = f"{self.name}:INVS"
        return self.dispatch_bool(cmd, inv)


class ChannelList:
    def __init__(self, resource, numbers: list[int]) -> None:
        self.channels: list[Channel] = list(
            map(lambda x: Channel(x, resource), numbers)
        )

    def attenuation(
        self, attn: Optional[Attenuation] = None
    ) -> list[Optional[Attenuation]]:
        return list(map(lambda x: x.attenuation(attn), self.channels))

    def bandwith_limit(
        self, state: Optional[bool] = None
    ) -> list[Optional[bool]]:
        return list(map(lambda x: x.bandwith_limit(state), self.channels))

    def coupling(
        self, cpl: Optional[Coupling] = None
    ) -> list[Optional[Coupling]]:
        return list(map(lambda x: x.coupling(cpl), self.channels))

    def offset(
        self, offset: Optional[Voltage] = None
    ) -> list[Optional[Voltage]]:
        return list(map(lambda x: x.offset(offset), self.channels))

    def skew(self, ns: Optional[Skew] = None) -> list[Optional[Skew]]:
        return list(map(lambda x: x.skew(ns), self.channels))

    def trace(self, state: Optional[bool] = None) -> list[Optional[bool]]:
        return list(map(lambda x: x.trace(state), self.channels))

    def unit(self, unit: Optional[Unit] = None) -> list[Optional[Unit]]:
        return list(map(lambda x: x.unit(unit), self.channels))

    def volt_div(
        self, v_gain: Optional[Voltage] = None
    ) -> list[Optional[Voltage]]:
        return list(map(lambda x: x.volt_div(v_gain), self.channels))

    def invert(self, inv: Optional[bool] = None) -> list[Optional[bool]]:
        return list(map(lambda x: x.invert(inv), self.channels))
