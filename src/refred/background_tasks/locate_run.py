from qtpy import QtCore

import refred.nexus_utilities
from refred.nexus_utilities import nxs_has_required_properties


class LocateRunThread(QtCore.QThread):  # type: ignore
    def setup(self, parent, run_number, index):
        self.parent = parent
        self.run_number = run_number
        self.index = index

    def run(self):
        """Tasks to be performed when .start() is called."""
        full_file_name = refred.nexus_utilities.find_nexus_full_path(self.run_number)

        if full_file_name and nxs_has_required_properties(full_file_name):
            self.parent.list_nxs[self.index] = full_file_name
            self.parent.runs_found += 1
        else:
            self.parent.number_of_runs = self.parent.number_of_runs - 1
            self.parent.list_nxs.pop(self.index)

    def stop(self):
        # TODO: investigate why this was implemented this way and remove this method
        pass

    def pause(self):
        # TODO: investigate why this was implemented this way and remove this method
        pass
