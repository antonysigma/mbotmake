from parsimonious.grammar import Grammar
from pytest import approx

from mbotmake2.grammars.toolpath import STRICT, SYNTAX
from mbotmake2.transformers.toolpath import ToolpathTransformer

grammar = Grammar(STRICT + SYNTAX)


def test_FanDuty() -> None:
    ast = grammar.parse("M106 S183.6\n")

    transformer = ToolpathTransformer()
    transformer.visit(ast)
    assert len(transformer.commands) == 1
    assert transformer.commands[0].function == "fan_duty"
    assert "value" in transformer.commands[0].parameters
    assert transformer.commands[0].parameters["value"] == approx(183.6 / 255)


def test_SetFeedrate() -> None:
    ast = grammar.parse("G1 F7200\n")
    transformer = ToolpathTransformer()
    transformer.visit(ast)

    assert transformer.feedrate == approx(7200 / 60.0)


def test_MoveE() -> None:
    ast = grammar.parse("G1 E1.30602 F4200\n")

    transformer = ToolpathTransformer()
    transformer.visit(ast)
    assert transformer.feedrate == approx(4200 / 60.0)

    assert len(transformer.commands) == 1
    assert transformer.commands[0].function == "move"
    assert "a" in transformer.commands[0].parameters
    assert transformer.commands[0].parameters["a"] == approx(1.30602)
    assert transformer.commands[0].parameters["feedrate"] == approx(transformer.feedrate)


def test_Move2D() -> None:
    ast = grammar.parse("G1 X-5.625 Y-7.102 E3.29059\n")

    transformer = ToolpathTransformer()
    transformer.feedrate = 1234
    transformer.visit(ast)

    assert len(transformer.commands) == 1
    assert transformer.commands[0].function == "move"
    assert "a" in transformer.commands[0].parameters
    assert transformer.commands[0].parameters["a"] == approx(3.29059)
    assert transformer.commands[0].parameters["x"] == approx(-5.625)
    assert transformer.commands[0].parameters["y"] == approx(-7.102)
    assert transformer.commands[0].parameters["feedrate"] == 1234
    assert transformer.commands[0].tags[0] == "Infill"


def test_ToggleFan() -> None:
    ast = grammar.parse("M107\n")
    transformer = ToolpathTransformer()
    transformer.visit(ast)
    assert len(transformer.commands) == 1
    assert transformer.commands[0].function == "toggle_fan"


def test_Comment() -> None:
    assert grammar.parse(";\n")
    assert grammar.parse("; 123abc\n")
    assert grammar.parse("M107 ; 123abc\n")
    assert grammar.parse("M107; 123abc\n")


def test_ResetPosition() -> None:
    assert grammar.parse("G92 E0\n")
    ast = grammar.parse("G92 E0.0\n")

    transformer = ToolpathTransformer()
    transformer.printer_offset.a = 123
    transformer.cursor.a = 321
    transformer.visit(ast)
    assert transformer.printer_offset.a == approx(transformer.cursor.a)


def test_AbsolutePosition() -> None:
    assert grammar.parse("G90\n")


def test_ToolheadTemperature() -> None:
    ast = grammar.parse("M104 S180\n")

    transformer = ToolpathTransformer()
    transformer.visit(ast)
    assert transformer.extruder_temperature is not None
    assert transformer.extruder_temperature == approx(180)


def test_PrintingTime() -> None:
    assert grammar.parse("; estimated printing time (normal mode) = 28m 3s\n")
    ast = grammar.parse("; estimated printing time (normal mode) = 5h 28m 3s\n")

    transformer = ToolpathTransformer()
    transformer.visit(ast)
    assert transformer.printing_time_s is not None
    assert transformer.printing_time_s == (5 * 3600 + 28 * 60 + 3)
