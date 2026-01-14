import sys

import h5py
from mantid.api import FileFinder
from mantid.kernel import logger
from mantid.simpleapi import Load

# Required Nexus properties for data reduction
REQUIRED_PROPERTIES = [
    "BL4B:CS:ExpPl:OperatingMode",
]


def find_nexus_full_path(run_number: int) -> str:
    try:
        full_file_name = FileFinder.findRuns(f"REF_L_{run_number}")[0]
    except (RuntimeError, ValueError):
        logger.error(f"Could not find file: {sys.exc_info()[1]}")
        full_file_name = ""
    return full_file_name


def get_run_number(nexus_full_path: str) -> str | None:
    try:
        with h5py.File(nexus_full_path, "r") as hf:
            _run_number = hf.get("entry/run_number")[0].decode()
        return _run_number
    except:
        logger.error(f"Could not find run number: {sys.exc_info()[1]}")
        return None


def nxs_has_required_properties(nexus_file: str) -> bool:
    try:
        ws = Load(nexus_file)
        for prop in REQUIRED_PROPERTIES:
            _ = ws.getRun().getProperty(prop).value
    except RuntimeError as e:
        logger.error(f"Missing properties in {nexus_file} - {e}")
        return False
    return True
