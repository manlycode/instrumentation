# -*- coding: utf-8 -*-

from pyvisa.resources.usb import USBInstrument

from instrumentation.siglent.commandable import Commandable


class SerialTrigger(Commandable):
    """

    To set up a serial trigger, set the trigger type to Serial using the
    command TRSE SERIAL. Then set the appropriate trigger criteria according
    to serial trigger type (using TRIIC:CON, etc.)

    These commands are used for the following serial bus protocols: I2C, SPI,
    UART, CAN, and LIN.
    (Pg. 209)

    Args:
        Commandable (_type_): _description_

    TODO:
        - [ ] TRIIC:SCL
        - [ ] TRIIC:SDA
        - [ ] TRIIC:CON
        - [ ] TRIIC:ADDR
        - [ ] TRIIC:DATA
        - [ ] TRIIC:DAT2
        - [ ] TRIIC:QUAL
        - [ ] TRIIC:RW
        - [ ] TRIIC:ALEN
        - [ ] TRIIC:DLEN
        - [ ] TRSPI:CLK
        - [ ] TRSPI:CLK:EDG
        - [ ] TRSPI:CLK:TIM
        - [ ] TRSPI:MOSI
        - [ ] TRSPI:MISO
        - [ ] TRSPI:CSTP
        - [ ] TRSPI:CS
        - [ ] TRSPI:NCS
        - [ ] TRSPI:TRTY
        - [ ] TRSPI:DATA
        - [ ] TRSPI:DLEN
        - [ ] TRSPI:BIT
        - [ ] TRUART:RX
        - [ ] TRUART:TX
        - [ ] TRUART:TRTY
        - [ ] TRUART:CON
        - [ ] TRUART:QUAL
        - [ ] TRUART:DATA
        - [ ] TRUART:BAUD
        - [ ] TRUART:DLEN
        - [ ] TRUART:PAR
        - [ ] TRUART:POL
        - [ ] TRUART:STOP
        - [ ] TRUART:BIT
        - [ ] TRCAN:CANH
        - [ ] TRCAN:CON
        - [ ] TRCAN:ID
        - [ ] TRCAN:IDL
        - [ ] TRCAN:DATA
        - [ ] TRCAN:DAT2
        - [ ] TRCAN:BAUD
        - [ ] TRLIN:SRC
        - [ ] TRLIN:CON
        - [ ] TRLIN:ID
        - [ ] TRLIN:DATA
        - [ ] TRLIN:DAT2
        - [ ] TRLIN:BAUD

    """

    def __init__(self, resource: USBInstrument) -> None:
        super().__init__(resource)
