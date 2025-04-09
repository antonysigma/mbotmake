from parsimonious.grammar import Grammar

# ChamberTemperature = "M141"

NOT_STRICT = (
    "Line = (Move / ResetPosition / FanDuty / ToggleFan "
    "/ ToolheadTemperature / BedTemperature / AbsolutePositioning / AbsolutePositioningForExtruders "
    "/ Unsupported / Comment) InlineComment? newline\n\n"
)

STRICT = (
    "Line = (Move / ResetPosition / FanDuty / ToggleFan "
    "/ ToolheadTemperature / BedTemperature / AbsolutePositioning / AbsolutePositioningForExtruders "
    "/ Comment) InlineComment? newline\n\n"
)

SYNTAX = r"""
BlankLine = ~r"[ \t\r]*\n"i
Comment = ";" (PrintingTime / IgnoredComment)

IgnoredComment = ~r"[^\n]*"i
InlineComment = ~r"[ \t]*;[^\n]*"i

ToolheadTemperature = "M104 S" Integer
BedTemperature = "M140 S" Integer
FanDuty = "M106 S" Decimal
ToggleFan = "M107"
Unsupported = ~r"[MG][0-9]+[^\n;]*"i

AbsolutePositioning = "G90"
AbsolutePositioningForExtruders = "M82"
ResetPosition = "G92 E" ("0.0" / "0")

Move = "G1" (Coord2D / CoordE / CoordZ / Feedrate)
CoordZ = " Z" Decimal Feedrate?
Coord2D = " X" Decimal " Y" Decimal ExtruderPosition? Feedrate?
CoordE = ExtruderPosition Feedrate

ExtruderPosition = " E" Decimal
Feedrate = " F" Decimal

PrintingTime = ~r" estimated printing time [^=]*="i Hour? Minute? Second?
Hour = " " Integer "h"
Minute = " " Integer "m"
Second = " " Integer "s"

Integer = ~"[0-9]+"i
Decimal = ~r"-?(\d+\.\d+|\d+|\.\d+)"i
newline = "\n"
"""

grammar = Grammar("Document = (Line / BlankLine)+\n" + NOT_STRICT + SYNTAX)
