from dataclasses import dataclass


@dataclass
class Command:
    function: str
    metadata: dict
    parameters: dict
    tags: list[str]
