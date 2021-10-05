import sys
from mantid.kernel import logger
from mantid.api import FileFinder
import h5py

def findNeXusFullPath(run_number):
    try:
        full_file_name = FileFinder.findRuns("REF_L_%d" % int(run_number))[0]
    except RuntimeError:
        logger.error("Could not find file: %s" % sys.exc_info()[1])
        full_file_name = ''
    return full_file_name


def get_run_number(nexus_full_path):
    with h5py.File(nexus_full_path, 'r') as hf:
        _run_number = hf.get('entry/run_number')
        return _run_number[0]
