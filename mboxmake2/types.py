from dataclasses import dataclass, field


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
