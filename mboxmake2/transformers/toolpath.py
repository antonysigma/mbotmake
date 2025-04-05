from parsimonious.nodes import NodeVisitor

from mboxmake2.types import Command


class ToolpathTransformer(NodeVisitor):
    def __init__(self):
        self.extruder_temperature: float | None = None
        self.commands: list[Command] = []

    def visit_Integer(self, node, _) -> int:
        return int(node.text)

    def visit_Decimal(self, node, _) -> float:
        return float(node.text)

    def visit_ToggleFan(self, _, __) -> None:
        self.commands.append(Command("toggle_fan", {"value": False}))

    def visit_FanDuty(self, _, visited_children) -> None:
        _, value = visited_children
        self.commands.append(Command("fan_duty", {"value": value / 255.0}))

    def visit_ToolheadTemperature(self, _, visited_children):
        _, temperature = visited_children
        print(f"Overriding extruder temperature to: {temperature}")
        self.extruder_temperature = temperature

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
