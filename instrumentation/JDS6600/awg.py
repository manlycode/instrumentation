from pyvisa import ResourceManager
from enum import IntEnum


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
        return f'{self.value},{self.scale}'

    def Hz(val: float):
        return Freq(int(val*100), 0)

    def kHz(val: float):
        return Freq(int(val*10000), 1)

    def MHz(val: float):
        return Freq(int(val*100000000), 2)

    def mHz(val: float):
        return Freq(int(val*100), 3)

    def uHz(val: float):
        return Freq(int(val*100), 4)


class Channel:
    def __init__(self, number: int, resource) -> None:
        self.number = number
        self.resource = resource

    def waveForm(self, wf: WaveForm = None) -> str:
        cmdOffset = 0
        if wf is None:
            cmd = f':r2{self.number+cmdOffset}=.'
            print(cmd)
            return self.resource.query(cmd)

        else:
            cmd = f':w2{self.number+cmdOffset}={wf.value}.\n'
            print(cmd)
            return self.resource.write(cmd)

    def frequency(self, freq: Freq = None) -> str:
        cmdOffset = 2
        if freq is None:
            cmd = f':r2{self.number+cmdOffset}=.'
            print(cmd)
            return self.resource.query(cmd)

        else:
            cmd = f':w2{self.number+cmdOffset}={freq}.\n'
            print(cmd)
            return self.resource.write(cmd)


class ChannelList():
    def __init__(self, resource, numbers: list[int]) -> None:
        self.channels: list[Channel] = map(
            lambda x: Channel(x, resource), numbers
            )

    def waveForm(self, limit: WaveForm = None) -> list[str]:
        return list(map(lambda x: x.waveForm(limit), self.channels))

    def frequency(self, limit: WaveForm = None) -> list[str]:
        return list(map(lambda x: x.frequency(limit), self.channels))


class AWG:
    resourceID = "ASRL1::INSTR"
    baudRate = 115200

    def __init__(self, rm: ResourceManager) -> None:
        self.rm = rm
        self.resource = self.rm.open_resource(AWG.resourceID)
        self.resource.baud_rate = 115200

    def write(self, msg: str):
        self.resource.write(msg)

    def query(self, msg: str) -> str:
        return self.resource.query(msg)

    def channel(self, number: int) -> Channel:
        return Channel(number, self.resource)

    def channels(self, numbers: list[int]) -> ChannelList:
        return ChannelList(self.resource, numbers)
