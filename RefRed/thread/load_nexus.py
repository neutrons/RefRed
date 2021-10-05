from qtpy import QtCore
from mantid.simpleapi import LoadEventNexus


class LoadNexus(QtCore.QThread):
    def setup(self, parent, filename, output_wks, metadata_only=False):
        self.parent = parent
        self.filename = filename
        self.output_wks = output_wks
        self.metadata_only = metadata_only

    def run(self):
        # try:
        _workspace = LoadEventNexus(
            Filename=self.filename, OutputWorkspace=self.output_wks, MetadataOnly=self.metadata_only
        )

        self.parent.runs_loaded += 1
        self.parent.list_wks.append(_workspace)
        # except:
        #   self.parent.number_of_runs = self.parent.number_of_runs - 1

    def stop(self):
        pass

    def pause(self):
        pass
