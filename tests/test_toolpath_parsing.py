from parsimonious.grammar import Grammar
from pytest import approx

from mboxmake2.grammars.toolpath import STRICT, SYNTAX
from mboxmake2.transformers.toolpath import ToolpathTransformer

grammar = Grammar(STRICT + SYNTAX)


def test_FanDuty() -> None:
    assert grammar.parse("M106 S183.6\n")


def test_Move() -> None:
    assert grammar.parse("G1 X-5.625 Y-7.102 E3.29059\n")
    assert grammar.parse("G1 E1.30602 F4200\n")
    assert grammar.parse("G1 F7200\n")


def test_ToggleFam() -> None:
    assert grammar.parse("M107\n")


def test_Comment() -> None:
    assert grammar.parse(";\n")
    assert grammar.parse("; 123abc\n")
    assert grammar.parse("M107 ; 123abc\n")
    assert grammar.parse("M107; 123abc\n")


def test_ResetPosition() -> None:
    assert grammar.parse("G92 E0\n")
    assert grammar.parse("G92 E0.0\n")


def test_AbsolutePosition() -> None:
    assert grammar.parse("G90\n")


def test_ToolheadTemperature() -> None:
    ast = grammar.parse("M104 S180\n")

    transformer = ToolpathTransformer()
    transformer.visit(ast)
    assert transformer.extruder_temperature is not None
    assert transformer.extruder_temperature == approx(180)
