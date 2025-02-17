import os

from qtpy import QtWidgets

from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader
from RefRed.load_reduced_data_set.stitching_ascii_widget import StitchingAsciiWidget


class LoadReducedDataSetHandler(object):
    last_row_loaded = -1

    def __init__(self, parent=None):
        self.parent = parent

    def run(self):
        _path = self.parent.path_ascii
        _filter = "Ascii File (*.txt);; All (*.*)"
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent, "Open Reduced Data Set", directory=_path, filter=_filter
        )

        QtWidgets.QApplication.processEvents()
        if not filename:  # user cancelled
            return

        _new_path = os.path.dirname(filename)
        self.parent.path_ascii = _new_path

        o_loaded_ascii = ReducedAsciiLoader(parent=self.parent, ascii_file_name=filename)
        if self.parent.o_stitching_ascii_widget is None:
            self.parent.o_stitching_ascii_widget = StitchingAsciiWidget(parent=self.parent)
        self.parent.o_stitching_ascii_widget.add_data(o_loaded_ascii)

        self.last_row_loaded = self.parent.o_stitching_ascii_widget.row_of_this_file
        self.plot()

    def plot(self):
        if self.parent.o_stitching_ascii_widget is not None:
            self.parent.o_stitching_ascii_widget.update_display()
