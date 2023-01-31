from time import sleep

import pyvisa

from instrumentation.JDS6600.awg import Freq
from instrumentation.siglent.measure import MDType, ParamValue
from instrumentation.siglent.si_value import SIValue

from ..JDS6600 import AWG, WaveForm
from ..siglent import Coupling, Scope

rm = pyvisa.ResourceManager()


def build_awg() -> AWG:
    res = rm.open_resource(AWG.RESOURCE_ID)
    res.baud_rate = AWG.BAUD_RATE  # type: ignore
    return AWG(res)  # type: ignore


def build_scope() -> Scope:
    res = rm.open_resource(Scope.RESOURCE_ID)
    return Scope(res)  # type: ignore


scope = build_scope()
awg = build_awg()


def run_step(awg_freq: int):
    sleep_duration = 3

    if awg_freq < 100:
        sleep_duration = 6

    awg.channel(1).frequency(Freq.Hz(awg_freq))
    sleep(sleep_duration)

    if awg_freq > 100:
        scope.auto_setup()
        sleep(sleep_duration)

    measured_freq = scope.measure.cymometer()
    if awg_freq <= 10:
        measured_freq = SIValue.parse(f"{awg_freq}Hz")

    p2p_1 = scope.measure.parameter_value(ParamValue.PKPK, 1)
    p2p_2 = scope.measure.parameter_value(ParamValue.PKPK, 2)
    phase_shift = scope.measure.measure_delay(MDType.PHA, 1, 2)

    # print(f"freq:   {measured_freq}")
    # print(f"p2p_1:           {p2p_1}")
    # print(f"p2p_2:           {p2p_2}")
    # print(f"phase_shift:     {p2p_2}")

    return [measured_freq, p2p_1, p2p_2, phase_shift]


def runScript():
    awg_res = rm.open_resource(AWG.RESOURCE_ID)
    awg_res.baud_rate = AWG.BAUD_RATE

    # Setup Scope
    scope.reset()
    sleep(5)

    # Setup Waves
    awg.channel(1).frequency(Freq.Hz(100))
    awg.channel(1).waveForm(WaveForm.SINE)
    awg.channel(1).offset(0.0)
    awg.channel(1).amplitude(1.0)
    scope.channels([1, 2]).coupling(Coupling.A1M)
    scope.channels([1, 2]).bandwith_limit(True)
    sleep(1)

    scope.auto_setup()
    sleep(5)

    freqs_to_test = [
        5,
        10,
        20,  # Phase won't register under 30
        30,
        50,
        100,
        200,
        400,
        800,
        1600,
        2000,
        4000,
        8000,
        1000,
        2000,
    ]

    for freq in freqs_to_test:
        result = run_step(freq)
        print(
            f"{result[0].value}{result[0].unit} {result[1].value} {result[2].value} {result[3].value}"  # type: ignore
        )
