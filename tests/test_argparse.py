from mbotmake2.__main__ import parseArgs


def test_extruder_args() -> None:
    assert parseArgs(["-e", "SmartExtPlus"])
    assert parseArgs(["--extruder", "SmartExtPlus"])

    assert parseArgs(["-e", "ToughExt"])
    assert parseArgs(["--extruder", "ToughExt"])


def test_machine_args() -> None:
    assert parseArgs(["-m", "RepPlus"])
