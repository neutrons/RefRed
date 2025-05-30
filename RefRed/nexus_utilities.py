import sys

import h5py
from mantid.api import FileFinder
from mantid.kernel import logger


def findNeXusFullPath(run_number):
    try:
        full_file_name = FileFinder.findRuns("REF_L_%d" % int(run_number))[0]
    except RuntimeError:
        logger.error("Could not find file: %s" % sys.exc_info()[1])
        full_file_name = ""
    return full_file_name


def get_run_number(nexus_full_path):
    try:
        with h5py.File(nexus_full_path, "r") as hf:
            _run_number = hf.get("entry/run_number")[0].decode()
        return _run_number
    except:
        logger.error("Could not find run number: %s" % sys.exc_info()[1])
        return None
