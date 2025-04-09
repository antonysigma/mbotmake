from dataclasses import dataclass, field
from enum import Enum
from typing import Self


@dataclass
class Command:
    function: str
    parameters: dict
    metadata: dict = field(default_factory=lambda: {})
    tags: list[str] = field(default_factory=lambda: [])


class MoveType(Enum):
    TravelMove = "Travel Move"
    Infill = "Infill"
    Leaky = "Leaky Travel Move"
    Retract = "Retract"


@dataclass
class Coords:
    a: float  # Extruder position
    x: float
    y: float

    def __add__(self, x: Self):
        return Coords(
            self.a + x.a,
            self.x + x.x,
            self.y + x.y,
        )


def detectMoveType(prev: Coords, current: Coords) -> MoveType:
    if current.a < prev.a:
        return MoveType.Retract

    if current.a > prev.a:
        return MoveType.Infill

    return MoveType.Leaky


@dataclass
class CoordZ:
    z: float
    feedrate: float | None = None


@dataclass
class CoordE:
    extruder_position: Coords
    feedrate: float


@dataclass
class PrinterSettings:
    duration_s: int
    total_commands: int
    num_z_transitions: int
    extruder_temperature: int
    extrusion_distance_mm: float
    bounding_box: dict


class MachineType(Enum):
    REPLICATOR5 = 1
    REPLICATORPlUS = 2
    REPLICATORMINI = 3
    REPLICATORMINIPLUS = 4


class ExtruderType(Enum):
    SMARTEXTRUDER = 1
    SMARTEXTRUDERPLUS = 2
    TOUGHEXTRUDER = 3
    EXPERIMENTALEXTRUDER = 4
