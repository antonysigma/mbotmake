from dataclasses import asdict

from parsimonious.nodes import NodeVisitor

from mbotmake2.types import Command, CoordE, Coords, CoordZ, MoveType

RELATIVE_MOVE = {"relative": {"a": False, "x": False, "y": False, "z": False}}


class Logging:
    unsupported_commands: set[str] = set()

    def logUnsupportedCommand(self, line: str) -> None:
        cmd = line.split(" ")[0]
        assert not (cmd == "G1" and len(line.split(" ")) > 1), f"Move command ignored: {line}"

        if cmd in self.unsupported_commands:
            return

        print(f"Skipping command: {cmd}")
        self.unsupported_commands.add(cmd)


class ToolpathTransformer(NodeVisitor):
    def __init__(self):
        self.extruder_temperature: float | None = None
        self.commands: list[Command] = []
        self.printer_offset = Coords(0, 0, 0)
        self.cursor = Coords(0, 0, 0)
        self.current_z: float = 0
        self.feedrate: float | None = None
        self.z_transitions: int = 0
        self.logging = Logging()
        self.printing_time_s: int | None = None

    def visit_Integer(self, node, _) -> int:
        return int(node.text)

    def visit_Decimal(self, node, _) -> float:
        return float(node.text)

    def visit_Unsupported(self, node, _) -> None:
        self.logging.logUnsupportedCommand(node.text)

    def visit_ToggleFan(self, _, __) -> None:
        self.commands.append(Command("toggle_fan", {"value": False}))

    def visit_FanDuty(self, _, visited_children) -> None:
        _, value = visited_children
        self.commands.append(Command("fan_duty", {"value": value / 255.0}))

    def visit_ResetPosition(self, _, __) -> None:
        self.printer_offset.a = self.cursor.a

    def visit_ToolheadTemperature(self, _, visited_children):
        _, temperature = visited_children

        if self.extruder_temperature is None or temperature > self.extruder_temperature:
            if self.extruder_temperature is not None:
                print(f"Overriding extruder temperature: {self.extruder_temperature} -> {temperature}")
            self.extruder_temperature = temperature

        self.commands.append(Command("set_toolhead_temperature", {"temperature": temperature}))

    def visit_Move(self, node, visited_children) -> None:
        _, (coords,) = visited_children

        if isinstance(coords, Coords):
            self.generateMove2DCommand(coords)

        elif isinstance(coords, CoordE):
            self.generateMoveECommand(coords)

        elif isinstance(coords, CoordZ):
            if coords.z > self.current_z:
                self.z_transitions += 1
                self.current_z = coords.z

            self.generateMove2DCommand(Coords(0, 0, 0))

        elif isinstance(coords, float):
            self.feedrate = coords

        else:
            raise RuntimeError(f"Unknown move command: {node.text}, {coords}")

    def generateMoveECommand(self, c: CoordE):
        self.feedrate = c.feedrate

        self.cursor = self.printer_offset + c.extruder_position
        self.commands.append(
            Command(
                "move",
                asdict(self.cursor) | {"feedrate": self.feedrate, "z": self.current_z},
                metadata=RELATIVE_MOVE,
                tags=[c.extruder_position.move_type.value],
            )
        )

    def generateMove2DCommand(self, coords: Coords) -> None:
        self.cursor = self.printer_offset + coords
        tag = coords.move_type
        # if G0, tag = MoveType.TravelMove

        self.commands.append(
            Command(
                "move",
                asdict(self.cursor) | {"feedrate": self.feedrate, "z": self.current_z},
                metadata=RELATIVE_MOVE,
                tags=[tag.value],
            )
        )

    def visit_Coord2D(self, _, visited_children) -> Coords:
        _, x, _, y, extruder_position, feedrate = visited_children

        if isinstance(feedrate, list):
            assert isinstance(feedrate[0], float)
            self.feedrate = feedrate[0]

        if isinstance(extruder_position, list):
            assert isinstance(extruder_position[0], Coords)
            return Coords(extruder_position[0].a, x, y)

        return Coords(0, x, y)

    def visit_CoordZ(self, _, visited_children) -> CoordZ:
        _, z, optional_feedrate = visited_children

        if isinstance(optional_feedrate, list):
            return CoordZ(z, optional_feedrate[0])

        return CoordZ(z)

    def visit_CoordE(self, _, visited_children) -> CoordE:
        extruder_position, feedrate = visited_children
        return CoordE(extruder_position, feedrate)

    def visit_Feedrate(self, _, visited_children) -> float:
        return visited_children[1] / 60.0

    def visit_ExtruderPosition(self, _, visited_children) -> Coords:
        _, value = visited_children
        return Coords(value, 0, 0)

    def visit_PrintingTime(self, _, visited_children) -> None:
        _, h, m, s = visited_children

        assert self.printing_time_s is None
        self.printing_time_s = 0
        if isinstance(h, list):
            assert isinstance(h[0], int)
            self.printing_time_s += h[0] * 3600

        if isinstance(m, list):
            assert isinstance(m[0], int)
            self.printing_time_s += m[0] * 60

        if isinstance(s, list):
            assert isinstance(s[0], int)
            self.printing_time_s += s[0]

    def visit_Hour(self, _, visited_children) -> int:
        _, value, _ = visited_children
        return value

    def visit_Minute(self, _, visited_children) -> int:
        _, value, _ = visited_children
        return value

    def visit_Second(self, _, visited_children) -> int:
        _, value, _ = visited_children
        return value

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
