# -*- coding: utf-8 -*-

from enum import IntEnum
from typing import Optional

from pyvisa.resources.usb import USBInstrument


class WaveForm(IntEnum):
    SINE = 0
    SQUARE = 1
    PULSE = 2
    TRIANGLE = 3
    PARTIAL_SINE = 4
    CMOS_WAVE = 5
    DC_LEVEL = 6
    HALF_WAVE = 7
    FULL_WAVE = 8
    POSITIVE_STEP = 9
    NEGATIVE_STEP = 10
    NOISE = 11
    EXPONENTIAL = 12
    EXPONENTIAL_DECAY = 13
    MULTI_TONE = 14
    SINC = 15
    LORENZ_PULSE = 16


class Freq:
    def __init__(self, value: int, scale: int) -> None:
        self.value = value
        self.scale = scale

    def __str__(self):
        return f"{self.value},{self.scale}"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, type(self)) and (self.value, self.scale) == (
            __o.value,
            __o.scale,
        )

    @staticmethod
    def _Hz(val: float):
        return Freq(int(val * 100), 0)

    @staticmethod
    def _listOf(funcRef, values):
        results = list(map(funcRef, values))

        if len(results) <= 1:
            return results[0]

        else:
            return results

    @staticmethod
    def Hz(*values: float):
        return Freq._listOf(Freq._Hz, values)

    @staticmethod
    def _kHz(val: float):
        return Freq(int(val * 10000), 1)

    @staticmethod
    def kHz(*values: float):
        return Freq._listOf(Freq._kHz, values)

    @staticmethod
    def _MHz(val: float):
        return Freq(int(val * 100000000), 2)

    @staticmethod
    def MHz(*values: float):
        return Freq._listOf(Freq._MHz, values)

    @staticmethod
    def _mHz(val: float):
        return Freq(int(val * 100), 3)

    @staticmethod
    def mHz(*values: float):
        return Freq._listOf(Freq._mHz, values)

    @staticmethod
    def _uHz(val: float):
        return Freq(int(val * 100), 4)

    @staticmethod
    def uHz(*values: float):
        return Freq._listOf(Freq._uHz, values)


class ChanEnabled:
    def __init__(self, value: bool) -> None:
        self.value = value

    def __str__(self) -> str:
        if self.value:
            return "1"

        else:
            return "0"


class Channel:
    def __init__(self, number: int, resource: USBInstrument) -> None:
        self.number = number
        self.resource = resource

    def __dispatch(self, cmd: str) -> Optional[str]:
        # result = self.resource.query(f"{cmd}\r\n")
        result = self.resource.query(f"{cmd}")

        if isinstance(result, str):
            return result.strip()

        else:
            return result

    def waveForm(self, wf: Optional[WaveForm] = None) -> Optional[str]:
        cmdOffset = 0
        if wf is not None:
            cmd = f":w2{self.number+cmdOffset}={wf.value}."

        else:
            cmd = f":r2{self.number+cmdOffset}=."

        return self.__dispatch(cmd)

    def frequency(self, freq: Optional[Freq] = None) -> Optional[str]:
        cmdOffset = 2
        if freq is None:
            cmd = f":r2{self.number+cmdOffset}=."

        else:
            cmd = f":w2{self.number+cmdOffset}={freq}."

        return self.__dispatch(cmd)

    def phase(self, degrees: Optional[float] = None):
        if self.number == 1:
            raise RuntimeError("Can't do that")

        if degrees is not None:
            value = int(degrees * 10)
            cmd = f":w31={value}."

        else:
            cmd = ":r31=."

        return self.__dispatch(cmd)

    def amplitude(self, volts: Optional[float] = None):
        cmdOffset = 4
        if volts is not None:
            value = int(volts * 1000.0)
            cmd = f":w2{self.number+cmdOffset}={value}."

        else:
            cmd = f":r2{self.number+cmdOffset}=."

        return self.__dispatch(cmd)

    def offset(self, volts: Optional[float] = None):
        cmdOffset = 6
        if volts is not None:
            value = 1000 + int((volts * 100.0))
            cmd = f":w2{self.number+cmdOffset}={value}."

        else:
            cmd = f":r2{self.number+cmdOffset}=."

        return self.__dispatch(cmd)


class ChannelList:
    def __init__(self, resource, numbers: list[int]) -> None:
        self.channels: list[Channel] = list(
            map(lambda x: Channel(x, resource), numbers)
        )

    def waveForm(
        self, limit: Optional[WaveForm] = None
    ) -> list[Optional[str]]:
        return list(map(lambda x: x.waveForm(limit), self.channels))

    def frequency(self, limit: Optional[Freq] = None) -> list[Optional[str]]:
        return list(map(lambda x: x.frequency(limit), self.channels))

    def offset(self, offset: Optional[float] = None) -> list[Optional[str]]:
        return list(map(lambda x: x.offset(offset), self.channels))

    def amplitude(self, volts: Optional[float] = None) -> list[Optional[str]]:
        return list(map(lambda x: x.amplitude(volts), self.channels))


class AWG:
    RESOURCE_ID = "ASRL1::INSTR"
    BAUD_RATE = 115200

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

    def enable_channels(
        self, c1_on: Optional[bool] = None, c2_on: Optional[bool] = None
    ):
        if (c1_on is not None) and (c2_on is not None):
            cmd = f":w20={ChanEnabled(c1_on)},{ChanEnabled(c2_on)}."
            self.resource.query(cmd)

            return None
        else:
            cmd = ":r20=."
            res = self.resource.query(cmd)
            str_values = res.split("=")[1].rstrip().replace(".", "").split(",")
            values = list(map(lambda x: x == "1", str_values))

            return values

    def print_all_values(self):
        for x in range(int(100)):
            cmd = f"r{x}=."
            print(self.resource.query(cmd))
