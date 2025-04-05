from parsimonious.nodes import NodeVisitor


class ToolpathTransformer(NodeVisitor):
    extruder_temperature: float | None = None

    def visit_Integer(self, node, _) -> int:
        return int(node.text)

    def visit_Decimal(self, node, _) -> float:
        return float(node.text)

    def visit_ToolheadTemperature(self, _, visited_children):
        _, temperature = visited_children
        print(f"Overriding extruder temperature to: {temperature}")
        self.extruder_temperature = temperature

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
