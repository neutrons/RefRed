from mantid.api import FileFinder

from refred.nexus_utilities import nxs_has_required_properties

INSTRUMENT_SHORT_NAME = "REF_L"


class LocateListRun(object):
    list_run: list[int] = []
    list_nexus_found: list[str] = []
    list_run_found: list[int] = []
    list_run_not_found: list[int] = []
    list_run_missing_properties: list[int] = []

    def __init__(self, list_run: list[int] | None = None):
        if list_run is None:
            return
        self.list_run = list_run
        self.init_parameters()

        for run in list_run:
            # Try to find the nexus file for each run
            try:
                nexus_file_name: str = FileFinder.findRuns(f"{INSTRUMENT_SHORT_NAME}_{run}")[0]
                self.list_nexus_found.append(nexus_file_name)
                self.list_run_found.append(run)
            # TODO: specify exception (Glass)
            except:
                self.list_run_not_found.append(run)

        for nexus_file in self.list_nexus_found[:]:
            if not nxs_has_required_properties(nexus_file):
                index = self.list_nexus_found.index(nexus_file)
                run_missing = self.list_run_found[index]
                self.list_run_missing_properties.append(run_missing)
                self.list_nexus_found.pop(index)
                self.list_run_found.pop(index)

    def init_parameters(self):
        self.list_run = []
        self.list_nexus_found = []
        self.list_run_found = []
        self.list_run_not_found = []
        self.list_run_missing_properties = []
