# -*- coding: utf-8 -*-
from instrumentation.JDS6600.awg import Freq
from tests import awg


def test_awg_freq_hz():
    single = Freq.Hz(100)
    assert single.value == 10000
    assert single.scale == 0

    multiple = Freq.Hz(100, 200)
    assert multiple[0] == Freq.Hz(100)
    assert multiple[0] == Freq.Hz(100)

    multiple = Freq.kHz(100, 200)
    assert multiple[0] == Freq.kHz(100)
    assert multiple[0] == Freq.kHz(100)

    multiple = Freq.MHz(100, 200)
    assert multiple[0] == Freq.MHz(100)
    assert multiple[0] == Freq.MHz(100)

    multiple = Freq.mHz(100, 200)
    assert multiple[0] == Freq.mHz(100)
    assert multiple[0] == Freq.mHz(100)

    multiple = Freq.uHz(100, 200)
    assert multiple[0] == Freq.uHz(100)
    assert multiple[0] == Freq.uHz(100)


def test_awg_enable():
    awg.enable_channels(True, True)
    assert awg.enable_channels() == [True, True]
    awg.enable_channels(False, True)
    assert awg.enable_channels() == [False, True]
    awg.enable_channels(False, False)
    assert awg.enable_channels() == [False, False]
    awg.enable_channels(True, False)
    assert awg.enable_channels() == [True, False]
