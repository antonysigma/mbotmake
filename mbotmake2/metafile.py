import json
from dataclasses import asdict
from importlib import resources
from pathlib import Path
from uuid import uuid4

from mbotmake2.types import ExtruderType, MachineType, PrinterSettings


def metaJson5th(meta: dict):
    """Update botType for Replicator 5th Gen"""
    meta["bot_type"] = "replicator_5"
    meta["miracle_config"]["_bot"] = "replicator_5"
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["x"] = -125
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["y"] = -99
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["z"] = 0.2
    return meta


def metaJsonPlus(meta: dict):
    """Update botType for Replicator+"""
    meta["bot_type"] = "replicator_b"
    meta["miracle_config"]["_bot"] = "replicator_b"
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["x"] = -150
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["y"] = -100
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["z"] = 0.2
    return meta


def metaJsonMini(meta: dict):
    """Update botType for Replicator Mini"""
    meta["bot_type"] = "mini_4"
    meta["miracle_config"]["_bot"] = "mini_4"
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["x"] = -59
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["y"] = -48
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["z"] = 1
    return meta


def metaJsonMiniPlus(meta: dict):
    """Update botType for Replicator Mini+"""
    meta["bot_type"] = "mini_8"
    meta["miracle_config"]["_bot"] = "mini_8"
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["x"] = -59
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["y"] = 37
    meta["miracle_config"]["gaggles"]["default"]["startPosition"]["z"] = 0.2
    return meta


def metaJsonSmartExtruder(meta: dict):
    """Updates Tool types for Smart Extruder"""
    meta["tool_type"] = "mk12"
    meta["tool_types"] = ["mk12"]
    meta["miracle_config"]["_extruders"] = ["mk12"]

    return meta


def metaJsonSmartExtruderPlus(meta: dict):
    """Updates Tool types for Smart Extruder+"""
    meta["tool_type"] = "mk13"
    meta["tool_types"] = ["mk13"]
    meta["miracle_config"]["_extruders"] = ["mk13"]

    return meta


def metaJsonToughSmartExtruderPlus(meta: dict):
    """Updates Tool types for Tough Smart Extruder+"""
    meta["tool_type"] = "mk13_impla"
    meta["tool_types"] = ["mk13_impla"]
    meta["miracle_config"]["_extruders"] = ["mk13_impla"]

    return meta


def metaJsonExperimentalExtruderPlus(meta: dict):
    """Updates Tool types for Experimental Extruder"""
    meta["tool_type"] = "mk13_experimental"
    meta["tool_types"] = ["mk13_experimental"]
    meta["miracle_config"]["_extruders"] = ["mk13_experimental"]

    return meta


METAJSON_PATH = resources.files("mbotmake2").joinpath("templates/Makerbot_RepPlus.meta.json")


def generateMetajson(
    outfile: Path,
    printer_settings: PrinterSettings,
    machinetype: MachineType,
    extrudertype: ExtruderType,
) -> None:
    with METAJSON_PATH.open("r") as metajson:
        meta = json.load(metajson)

    match machinetype:
        case MachineType.REPLICATOR5:
            meta = metaJson5th(meta)
        case MachineType.REPLICATORPlUS:
            meta = metaJsonPlus(meta)
        case MachineType.REPLICATORMINI:
            meta = metaJsonMini(meta)
        case MachineType.REPLICATORMINIPLUS:
            meta = metaJsonMiniPlus(meta)

    match extrudertype:
        case ExtruderType.SMARTEXTRUDER:
            meta = metaJsonSmartExtruder(meta)
        case ExtruderType.SMARTEXTRUDERPLUS:
            meta = metaJsonSmartExtruderPlus(meta)
        case ExtruderType.TOUGHEXTRUDER:
            meta = metaJsonToughSmartExtruderPlus(meta)
        case ExtruderType.EXPERIMENTALEXTRUDER:
            meta = metaJsonExperimentalExtruderPlus(meta)

    vardict = asdict(printer_settings)

    # I have no idea what this is supposed to be
    vardict["commanded_duration_s"] = vardict["duration_s"] / 2

    vardict["num_z_layers"] = vardict["num_z_transitions"] + 1
    vardict["platform_temperature"] = 0.0
    vardict["extruder_temperatures"] = [vardict["extruder_temperature"]]
    vardict["extrusion_distances_mm"] = [vardict["extrusion_distance_mm"]]

    vardict["extrusion_mass_g"] = vardict["extrusion_distance_mm"] * 0.00305
    vardict["extrusion_masses_g"] = [vardict["extrusion_mass_g"]]
    vardict["uuid"] = str(uuid4())

    with open(outfile, "w") as metafile:
        json.dump(meta | vardict, metafile, indent=2)
