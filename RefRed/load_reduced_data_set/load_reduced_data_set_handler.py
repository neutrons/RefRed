from qtpy import QtWidgets
import os
from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader
from RefRed.load_reduced_data_set.stitching_ascii_widget import StitchingAsciiWidget


class LoadReducedDataSetHandler(object):

    last_row_loaded = -1

    def __init__(self, parent=None):
        self.parent = parent

    def run(self):
        _path = self.parent.path_ascii
        _filter = u"Ascii File (*.txt);; All (*.*)"
        filename = str(QtWidgets.QFileDialog.getOpenFileName(self.parent, 'Open Reduced Data Set',
                                                     directory=_path,
                                                     filter=_filter))

        QtWidgets.QApplication.processEvents()
        if not (filename== ""):

            _new_path = os.path.dirname(filename)
            self.parent.path_ascii = _new_path

            o_loaded_ascii = ReducedAsciiLoader(parent=self.parent,
                                                ascii_file_name=filename)
            if self.parent.o_stitching_ascii_widget is None:
                self.parent.o_stitching_ascii_widget = StitchingAsciiWidget(parent=self.parent,
                                                                            loaded_ascii=o_loaded_ascii)
            else:
                self.parent.o_stitching_ascii_widget.add_data(o_loaded_ascii)

            self.last_row_loaded = self.parent.o_stitching_ascii_widget.row_of_this_file
            self.plot()

    def plot(self):
        big_table_data = self.parent.big_table_data
        data = big_table_data[0,0]
        if data is None:
            o_user_configuration = self.parent.o_user_configuration
            _isylog = o_user_configuration.is_reduced_plot_stitching_tab_ylog
            _isxlog = o_user_configuration.is_reduced_plot_stitching_tab_xlog
        else:
            _isylog = data.all_plot_axis.is_reduced_plot_stitching_tab_ylog
            _isxlog = data.all_plot_axis.is_reduced_plot_stitching_tab_xlog

        if self.parent.o_stitching_ascii_widget is None:
            return

        self.parent.o_stitching_ascii_widget.update_display(isxlog=_isxlog,
                                                            isylog=_isylog,
                                                            force_row=self.last_row_loaded)
