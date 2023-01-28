import re


class SIValue:
    def __init__(self, value: float, unit: str = "V") -> None:
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f"{self.value}{self.unit}"

    @classmethod
    def parse(cls, value: str):
        result = re.match(r"(-*\d+\.\d+E[+|-]\d+)(\D+)", value)

        if result is not None:
            value = result.group(1)
            unit = result.group(2)

            if value is not None:
                if unit is not None:
                    return cls(float(value), unit)

        raise RuntimeError("Coudln't parse offset")
