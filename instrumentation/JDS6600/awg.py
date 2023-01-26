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

    @staticmethod
    def Hz(val: float):
        return Freq(int(val * 100), 0)

    @staticmethod
    def kHz(val: float):
        return Freq(int(val * 10000), 1)

    @staticmethod
    def MHz(val: float):
        return Freq(int(val * 100000000), 2)

    @staticmethod
    def mHz(val: float):
        return Freq(int(val * 100), 3)

    @staticmethod
    def uHz(val: float):
        return Freq(int(val * 100), 4)


class Channel:
    def __init__(self, number: int, resource: USBInstrument) -> None:
        self.number = number
        self.resource = resource

    def __dispatch(self, cmd: str) -> Optional[str]:
        result = self.resource.query(f"{cmd}\r\n")

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
