from PyQt4 import QtCore
import RefRed.nexus_utilities


class LocateRunThread(QtCore.QThread):

    def setup(self, parent, run_number, index):
        self.parent = parent
        self.run_number = run_number
        self.index = index

    def run(self):
        try:
            full_file_name = RefRed.nexus_utilities.findNeXusFullPath(self.run_number)
        except:
            full_file_name = ''

        if full_file_name == '':
            self.parent.number_of_runs = self.parent.number_of_runs - 1
            self.parent.list_nxs.pop()
        else:
            self.parent.list_nxs[self.index] = full_file_name
            self.parent.runs_found += 1

    def stop(self):
        # TODO: investigate why this was implemented this way and remove this method
        pass

    def pause(self):
        # TODO: investigate why this was implemented this way and remove this method
        pass
