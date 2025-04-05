from dataclasses import dataclass, field
from enum import Enum
from typing import Self


@dataclass
class Command:
    function: str
    parameters: dict
    metadata: dict = field(default_factory=lambda: {})
    tags: list[str] = field(default_factory=lambda: [])


@dataclass
class Coords:
    A: float  # Extruder position
    X: float
    Y: float
    Z: float

    def __add__(self, x: Self):
        return Coords(
            self.A + x.A,
            self.B + x.B,
            self.C + x.C,
            self.Z + x.Z,
        )


class MoveType(Enum):
    TravelMove = "TravelMove"
    Infill = "Infill"
    Leaky = "LeakyTravelMove"
    Retract = "Retract"
