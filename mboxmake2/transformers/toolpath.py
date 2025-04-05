from parsimonious.nodes import NodeVisitor

from mboxmake2.types import Command, Coords, MoveType


class ToolpathTransformer(NodeVisitor):
    def __init__(self):
        self.extruder_temperature: float | None = None
        self.commands: list[Command] = []
        self.printer_offset = Coords(0, 0, 0, 0)
        self.cursor = Coords(0, 0, 0, 0)
        self.feedrate: float | None = None

    def visit_Integer(self, node, _) -> int:
        return int(node.text)

    def visit_Decimal(self, node, _) -> float:
        return float(node.text)

    def visit_ToggleFan(self, _, __) -> None:
        self.commands.append(Command("toggle_fan", {"value": False}))

    def visit_FanDuty(self, _, visited_children) -> None:
        _, value = visited_children
        self.commands.append(Command("fan_duty", {"value": value / 255.0}))

    def visit_ResetPosition(self, _, __) -> None:
        self.printer_offset.A = self.cursor.A

    def visit_ToolheadTemperature(self, _, visited_children):
        _, temperature = visited_children
        print(f"Overriding extruder temperature to: {temperature}")
        self.extruder_temperature = temperature

    def visit_MoveE(self, _, visited_children) -> None:
        _, (feedrate, extruder_position) = visited_children
        self.feedrate = feedrate

        if extruder_position is None:
            return

        assert isinstance(extruder_position, Coords)
        a = extruder_position.A
        if a == 0:
            tag = MoveType.Leaky
        elif a > 0:
            tag = MoveType.Infill
        else:
            tag = MoveType.Retract

        self.cursor = self.printer_offset + extruder_position

        self.commands.append(
            Command(
                "move",
                self.cursor | {"feedrate": self.feedrate},
                metadata={"relative": {"a": False, "x": False, "y": False, "z": False}},
                tag=[str(tag)],
            )
        )

    def visit_Coord2D(self, _, visited_children) -> Coords:
        _, x, _, y, _, a = visited_children
        return Coords(a, x, y, 0)

    def visit_CoordZ(self, _, visited_children) -> tuple[float, Coords | None]:
        optional_extruder_position, _, (feedrate,) = visited_children
        normalized_feedrate = feedrate / 60.0

        if isinstance(optional_extruder_position, Coords):
            return normalized_feedrate, optional_extruder_position

        return normalized_feedrate, None

    def visit_ExtruderPosition(self, _, visited_children) -> Coords:
        _, value, _ = visited_children
        return Coords(value, 0, 0, 0)

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
