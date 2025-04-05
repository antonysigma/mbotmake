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
    a: float  # Extruder position
    x: float
    y: float
    z: float

    def __add__(self, x: Self):
        return Coords(
            self.a + x.a,
            self.x + x.x,
            self.y + x.y,
            self.z + x.z,
        )


class MoveType(Enum):
    TravelMove = "TravelMove"
    Infill = "Infill"
    Leaky = "LeakyTravelMove"
    Retract = "Retract"
