# -*- coding: utf-8 -*-
from time import sleep
from tests import awg


def test_awg_enable():
    awg.enable_channels(True, True)
    assert awg.enable_channels() == [True, True]
    awg.enable_channels(False, True)
    assert awg.enable_channels() == [False, True]
    awg.enable_channels(False, False)
    assert awg.enable_channels() == [False, False]
    awg.enable_channels(True, False)
    assert awg.enable_channels() == [True, False]
