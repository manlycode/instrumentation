# -*- coding: utf-8 -*-

from pyvisa import ResourceManager

from instrumentation.JDS6600 import AWG
from instrumentation.siglent import Scope


rm = ResourceManager()


def build_awg() -> AWG:
    res = rm.open_resource(AWG.RESOURCE_ID)
    res.baud_rate = AWG.BAUD_RATE  # type: ignore
    return AWG(res)  # type: ignore


def build_scope() -> Scope:
    res = rm.open_resource(Scope.RESOURCE_ID)
    # res.encoding =  "utf_8"
    return Scope(res)  # type: ignore


awg = build_awg()

scope = build_scope()

__all__ = ["awg", "scope"]
