from mboxmake2.types import Command, MoveType, PrinterSettings


def collectPrinterSettings(
    commands: list[Command], z_transitions: int
) -> PrinterSettings:
    toolpathfilelength = len(commands)
    extrusion_distance = max(
        c.parameters["a"] for c in commands if c.function == "move"
    )

    tool0temp = max(
        c.parameters["temperature"]
        for c in commands
        if c.function == "set_toolhead_temperature"
    )

    printcoords = [
        c.parameters
        for c in commands
        if set(c.tags) & {MoveType.Infill.value, MoveType.Leaky.value}
    ]

    bbox = {
        "x_max": max(c["x"] for c in printcoords),
        "x_min": min(c["x"] for c in printcoords),
        "y_max": max(c["y"] for c in printcoords),
        "y_min": min(c["y"] for c in printcoords),
        "z_max": max(c["z"] for c in printcoords),
        "z_min": min(c["z"] for c in printcoords),
    }

    # Make sure bounding box is centered near the origin in X/Y and at the bottom of Z.
    xrel = (bbox["x_max"] + bbox["x_min"]) / (bbox["x_max"] - bbox["x_min"])
    yrel = (bbox["y_max"] + bbox["y_min"]) / (bbox["y_max"] - bbox["y_min"])
    zrel = (bbox["z_max"] + bbox["z_min"]) / (bbox["z_max"] - bbox["z_min"])
    print(f"xrel: {xrel}; yrel: {yrel}; zrel: {zrel}")
    # assert -0.15 < xrel < 0.15, xrel
    # assert -0.15 < yrel < 0.15, yrel
    # assert  0.95 < zrel < 1.05, zrel
    assert 0 < bbox["z_min"] < 0.5, (
        f"Potential extrusion collision: z_min = {bbox['z_min']}"
    )

    return PrinterSettings(
        duration_s=0.0,
        total_commands=toolpathfilelength,
        num_z_transitions=z_transitions,
        extruder_temperature=tool0temp,
        extrusion_distance_mm=extrusion_distance,
        bounding_box=bbox,
    )
