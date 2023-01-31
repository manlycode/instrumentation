# -*- coding: utf-8 -*-

import re
from typing import Optional


class SIValue:
    def __init__(
        self, value: Optional[float], unit: Optional[str] = "V"
    ) -> None:
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        if self.unit == "****":
            return self.unit
        return f"{self.value}{self.unit}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, SIValue):
            return (self.unit == __o.unit) and (self.value == __o.value)

        return False

    @classmethod
    def parse(cls, value: str):
        if value == "****":
            return SIValue(None, "****")
        result = re.match(r"(-*\d+(\.\d+E[+|-]\d+)*)(\D+)", value)

        if result is not None:
            value = result.group(1)
            unit = result.group(3)

            if value is not None:
                if unit is not None:
                    return cls(float(value), unit)

        raise RuntimeError("Coudln't parse offset")
