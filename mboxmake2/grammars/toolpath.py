from parsimonious.grammar import Grammar

# ChamberTemperature = "M141"

NOT_STRICT = (
    "Line = (Move2D / MoveE / ResetPosition / FanDuty / ToggleFan "
    "/ ToolheadTemperature / BedTemperature / AbsolutePositioning "
    "/ Unsupported / Comment) Comment? newline\n\n"
)

STRICT = (
    "Line = (Move2D / MoveE / ResetPosition / FanDuty / ToggleFan "
    "/ ToolheadTemperature / BedTemperature / AbsolutePositioning "
    "/ Comment) Comment? newline\n\n"
)

SYNTAX = r"""
BlankLine = ~r"[ \t\r]*\n"i
Comment = ~r"[ \t]*;[^\n]*"i

ToolheadTemperature = "M104 S" Integer
BedTemperature = "M140 S" Integer
FanDuty = "M106 S" Decimal
ToggleFan = "M107"
Unsupported = ~r"[MG][0-9]+[^\n;]*"i

AbsolutePositioning = "G90"
ResetPosition = "G92 E" ("0.0" / "0")

Move2D = MoveCommand Coord2D
MoveE = MoveCommand CoordZ
Coord2D = "X" Decimal " Y" Decimal " E" Decimal
CoordZ = ExtruderPosition? "F" (Decimal / Integer)

ExtruderPosition = "E" (Decimal / Integer) " "
MoveCommand = "G1 "

Integer = ~"[0-9]+"i
Decimal = ~r"-?[1-9][0-9]*\.[0-9]+"i
newline = "\n"
"""

grammar = Grammar("Document = (Line / BlankLine)+\n" + NOT_STRICT + SYNTAX)
