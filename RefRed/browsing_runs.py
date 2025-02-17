import os

from qtpy import QtWidgets

from RefRed import nexus_utilities


class BrowsingRuns(object):
    list_files = None
    list_runs = None

    def __init__(self, parent=None, data_type="data"):
        self.parent = parent
        self.data_type = data_type

        self._select_files()
        self._populate_line_edit()

    def _select_files(self):
        _path = self.parent.path_config
        _filter = "NeXus (*.nxs);;All (*.*)"
        _title = "Select %s NeXus files" % self.data_type
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self.parent, _title, _path, _filter)

        QtWidgets.QApplication.processEvents()

        if len(filenames) == 0:
            self.parent.browsed_files[self.data_type] = None
        else:
            self.list_files = filenames
            self.parent.browsed_files[self.data_type] = filenames
            self.parent.path_config = os.path.dirname(filenames[0])

    def _populate_line_edit(self):
        # NOTE: skip for empty input
        if self.list_files is None:
            return

        _list_runs = [nexus_utilities.get_run_number(_run) for _run in self.list_files]
        _list_runs = [me for me in _list_runs if me is not None]
        _unique_list_runs = set(_list_runs)

        str_list = ",".join(_unique_list_runs) if len(_unique_list_runs) > 0 else ""

        if self.data_type == "data":
            self.parent.ui.data_sequence_lineEdit.setText(str_list)
        else:
            self.parent.ui.norm_sequence_lineEdit.setText(str_list)
