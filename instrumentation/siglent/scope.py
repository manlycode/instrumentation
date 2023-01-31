# -*- coding: utf-8 -*-

import time
from enum import Enum
from typing import Optional

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.channel import Channel, ChannelList
from instrumentation.siglent.commandable import Commandable
from instrumentation.siglent.measure import Measure


class ScopeId:
    def __init__(self, response: str):
        """
        Initialized ScopeId

        Args:
            response (str): String response from *IDC? query
        """
        splitResponse = response.strip().split(",")
        self.manufacturer = splitResponse[0]
        self.model = splitResponse[1]
        self.serial_num = splitResponse[2]
        self.firmware = splitResponse[3]


class HeaderMode(Enum):
    SHORT = "SHORT"
    LONG = "LONG"
    OFF = "OFF"


class Scope(Commandable):
    """
    Root object for

    Args:
        Commandable (_type_): _description_

    Returns:
        _type_: _description_

    TODO:
        - [✅] *IDN?(IdentificationNumber)
        - [✅] *OPC(OperationComplete)
        - [✅] *RST(Reset)
        (Pg. 18)

        - [ ] SCDP
        (Pg. 148)

        - [ ] *RCL
        - [ ] RCPN
        (Pg. 150)

        - [ ] INR? (Page 174)

    """

    RESOURCE_ID = "USB0::0xF4EC::0x1012::SDSAHBAQ6R1188::INSTR"

    def __init__(self, resource: USBInstrument) -> None:
        self.measure = Measure(resource)
        super().__init__(resource)

    def write(self, msg: str):
        self.resource.write(msg)

    def channel(self, number: int) -> Channel:
        return Channel(number, self.resource)

    def channels(self, numbers: list[int]) -> ChannelList:
        return ChannelList(self.resource, numbers)

    def comm_header(self, mode: Optional[HeaderMode] = None) -> Optional[str]:
        res = super().dispatch_enum("CHDR", mode)

        if res is not None:
            return res.val

        else:
            return None

    def auto_setup(self):
        super().write("ASET")
        time.sleep(4)

    def idn(self) -> ScopeId:
        """
        The *IDN? query identifies the instrument type and software version.
        The response consists of four different fields providing information
        on the manufacturer, the scope model, the serial number and the
        firmware revision.

        Returns:
            ScopeId: Identifying information for a scope
        """
        res = self.resource.query("*IDN?")
        return ScopeId(res)

    def opc(self, isCommand: bool = False) -> Optional[int]:
        """
        The *OPC command sets the operation complete bit in the Standard Event
        Status Register when all pending device operations have finished.

        The *OPC? query places an ASCII "1" in the output queue when all
        pending device operations have completed. The interface hangs until
        this query returns.

        Args:
            isCommand (bool, optional): Set to true to send as a command. Set
            to false to send as a query.

            Defaults to False.

        Returns:
            Optional[int]: Result of query when sent as query.
        """
        cmd = "*OPC"

        if isCommand:
            super().write(cmd)
            return None

        else:
            res = self.resource.query(f"{cmd}?")
            return int(res)

    def reset(self):
        """
        The *RST command initiates a device reset. This is the same as pressing
        `Default` on the front panel.
        """
        return self.resource.write("*RST")
