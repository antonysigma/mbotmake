from mbotmake2.grammars.toolpath import grammar
from mbotmake2.transformers.toolpath import ToolpathTransformer


def test_prusa_gcode_file() -> None:
    with open("testcases/prusaslicer_gcode/cube.gcode", "r") as file:
        ast = grammar.parse(file.read())
        transformer = ToolpathTransformer()
        assert transformer.visit(ast)
