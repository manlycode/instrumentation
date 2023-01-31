# -*- coding: utf-8 -*-
from enum import Enum, auto

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable
from instrumentation.siglent.si_value import SIValue


class MeasureDelayType(Enum):
    """
    The phase difference between two channels.
    (rising edge - rising edge)
    """

    PHA = "PHA"
    """
    Delay between two channels.
    (first rising edge - first rising edge)
    """
    FRR = "FRR"
    """
    Delay between two channels.
    (first rising edge - first falling edge)
    """
    FRF = "FRF"
    """
    Delay between two channels.
    (first falling edge - first rising edge)
    """
    FFR = "FFR"
    """
    Delay between two channels.
    (first falling edge - first falling edge)
    """
    FFF = "FFF"
    """
    Delay between two channels.
    (first rising edge - last rising edge)
    """
    LRR = "LRR"
    """
    Delay between two channels.
    (first rising edge - last falling edge)
    """
    LRF = "LRF"
    """
    Delay between two channels.
    (first falling edge - last rising edge)
    """
    LFR = "LFR"

    """
    Delay between two channels.
    (first falling edge - last rising edge)
    """
    LFF = "LFF"
    """
    Delay between two channels.
    (edge – edge of the same type)
    """
    SKEW = "SKEW"


class ParamValue(Enum):
    PKPK = auto()
    MAX = auto()
    MIN = auto()
    AMPL = auto()
    TOP = auto()
    BASE = auto()
    CMEAN = auto()
    MEAN = auto()
    STDEV = auto()
    VSTD = auto()
    RMS = auto()
    CRMS = auto()
    OVSN = auto()
    FPRE = auto()
    OVSP = auto()
    RPRE = auto()
    LEVELX = auto()
    PER = auto()
    FREQ = auto()
    PWID = auto()
    NWID = auto()
    RISE = auto()
    FALL = auto()
    WID = auto()
    DUTY = auto()
    NDUTY = auto()
    DELAY = auto()
    TIMEL = auto()
    ALL = auto()


MDType = MeasureDelayType


class Measure(Commandable):
    """
    The commands in the MEASURE subsystem are used to make parametric
    measurements on displayed waveforms.

    To make a measurement, the portion of the waveform required for that
    measurement must be displayed on the oscilloscope screen.
    (Pg. 113)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [✅] CYMT?
        - [ ] MEAD
        - [ ] PACU
        - [ ] PAVA?
        - [ ] PASTAT
        - [ ] MEACL
        - [ ] MEGS
        - [ ] MEGA
        - [ ] MEGB
    """

    def __init__(self, resource: USBInstrument) -> None:
        self.resource = resource
        self.header = self.resource.query("CHDR?").rstrip()

        super().__init__(resource)

    def cymometer(self) -> SIValue:
        """
        The CYMOMETER? query measures and returns the frequency counter of the
        specified source. The counter measurement counts the trigger level
        crossings at the selected trigger slope and displays the results in
        MHz/kHz/Hz.

        Returns:
            SIValue:
                - unit: MHz/kHz/Hz
                - value: Frequency
        """
        cmd = "CYMT?"
        self.resource.write("CHDR LONG")
        res = super().query(cmd)

        return SIValue.parse(res.val)

    def disable_header(self):
        self.header = self.resource.query("CHDR?").rstrip()
        self.resource.write("CHDR OFF")

    def restore_header(self):
        self.resource.write(f"CHDR {self.header}")

    def measure_delay(
        self, type: MeasureDelayType, src_a: int, src_b: int
    ) -> SIValue:
        """
        The MEASURE_DELY command places the instrument in the continuous
        measurement mode and starts a type of delay measurement.

        The MEASURE_DELY? query returns the measured value of delay type.
        """
        source = f"C{src_a}-C{src_b}"
        cmd = f"{source}:MEAD? {type.value}"
        self.resource.write("CHDR LONG")
        self.resource.write(cmd)

        result = self.resource.read(encoding="mac_latin2")
        value_unit = result.rstrip().split(" ")[1].split(",")[1]

        return SIValue.parse(value_unit)

    def parameter_value(self, param_val: ParamValue, src: int) -> SIValue:
        """
        The PARAMETER_VALUE query measures and returns the specified
        measurement value present on the selected waveform.

        There are three uses for this command:
        Usage 1:
            Specify the source and the measurement. See the command “MEAD?” to
            get the measured value of delay measurement.

        Usage 2:
            Use “PAVA? CUST<x>” to get customized.

        Usage 3 :
            Use “PAVA? STAT<x>” to get statistics.
        """
        source = f"C{src}"
        cmd = f"{source}:PAVA? {param_val.name}"
        self.resource.write(cmd)

        result = self.resource.read(encoding="mac_latin2")

        value_unit = result.rstrip().split(" ")[1].split(",")[1]
        return SIValue.parse(value_unit)
