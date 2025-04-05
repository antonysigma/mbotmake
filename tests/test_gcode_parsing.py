from mboxmake2.grammars.toolpath import grammar


def test_prusa_gcode_file() -> None:
    with open("testcases/prusaslicer_gcode/cube.gcode", "r") as file:
        assert grammar.parse(file.read())
