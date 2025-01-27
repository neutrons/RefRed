import numpy as np
from qtpy import QtWidgets
from qtpy.QtCore import Qt  # type: ignore

from RefRed.gui_handling.gui_utility import GuiUtility


class StitchingAsciiWidget(object):
    loaded_ascii_array = []
    tableUi = None
    stitchingPlot = None
    parent = None
    isylog = True
    isxlog = True
    yaxistype = "RvsQ"
    row_of_this_file = 0

    def __init__(self, parent=None):
        self.parent = parent
        self.tableUi = parent.ui.reducedAsciiDataSetTable
        self.stitchingPlot = parent.ui.data_stitching_plot

    def add_data(self, newloaded_ascii):
        row_of_this_file = self.get_row_of_this_file(newloaded_ascii)
        if row_of_this_file == -1:
            # add row
            row_of_this_file = len(self.loaded_ascii_array)
            self.loaded_ascii_array.append(newloaded_ascii)
        else:
            # replace
            self.loaded_ascii_array[row_of_this_file] = newloaded_ascii
        self.row_of_this_file = row_of_this_file

        # Update the table
        _item = QtWidgets.QTableWidgetItem(str(newloaded_ascii.short_ascii_file_name))
        self.tableUi.setItem(row_of_this_file, 0, _item)
        _widget = self.tableUi.cellWidget(row_of_this_file, 1)
        _widget.setEnabled(True)
        _widget.setCheckState(Qt.Checked)

    def remove_data(self, list_file_to_remove=None):
        if list_file_to_remove is None:
            return
        _loaded_ascii_array = self.loaded_ascii_array
        _new_loaded_ascii_array = []
        for _loaded_ascii in _loaded_ascii_array:
            _name = _loaded_ascii.short_ascii_file_name
            if _name in list_file_to_remove:
                continue
            _new_loaded_ascii_array.append(_loaded_ascii)

        self.loaded_ascii_array = _new_loaded_ascii_array

    def remove_all_data(self):
        self.loaded_ascii_array = []

    def get_row_of_this_file(self, loaded_ascii):
        newFilename = loaded_ascii.ascii_file_name

        nbrRow = len(self.loaded_ascii_array)
        for i in range(nbrRow):
            _tmpObject = self.loaded_ascii_array[i]
            _name = _tmpObject.ascii_file_name

            if _name == newFilename:
                return i
        return -1

    def update_status(self):
        nbrRow = len(self.loaded_ascii_array)
        for i in range(nbrRow):
            _data_object = self.loaded_ascii_array[i]

            _item_state = self.parent.ui.reducedAsciiDataSetTable.cellWidget(i, 1).checkState()
            if _item_state == 2:
                _data_object.isEnabled = True
            else:
                _data_object.isEnabled = False

            self.loaded_ascii_array[i] = _data_object

    def update_display(self):
        if self.loaded_ascii_array == []:
            return

        for i in range(len(self.loaded_ascii_array)):
            if self.tableUi.cellWidget(i, 1).checkState():
                _q_axis = self.loaded_ascii_array[i].col1
                _y_axis = self.loaded_ascii_array[i].col2
                _e_axis = self.loaded_ascii_array[i].col3

                [_y_axis_red, _e_axis_red] = self.format_data_from_ymode_selected(_q_axis, _y_axis, _e_axis)

                self.stitchingPlot.errorbar(_q_axis, _y_axis_red, yerr=_e_axis_red)

    def format_data_from_ymode_selected(self, q_axis, y_axis, e_axis):
        data_type = self.get_selected_reduced_output()
        [final_y_axis, final_e_axis] = self.get_formated_output(data_type, q_axis, y_axis, e_axis)
        return [final_y_axis, final_e_axis]

    def get_formated_output(self, data_type, _q_axis, _y_axis, _e_axis):
        try:
            # R vs Q selected
            if data_type == "RvsQ":
                return [_y_axis, _e_axis]

            # RQ4 vs Q selected
            if data_type == "RQ4vsQ":
                _q_axis_4 = _q_axis**4
                _final_y_axis = _y_axis * _q_axis_4
                _final_e_axis = _e_axis * _q_axis_4
                return [_final_y_axis, _final_e_axis]

            # Log(R) vs Q
            _final_y_axis = np.log(_y_axis)
            # _final_e_axis = np.log(_e_axis)
            _final_e_axis = _e_axis  # FIXME
        except:
            _final_e_axis = _e_axis
            _final_y_axis = _y_axis

        return [_final_y_axis, _final_e_axis]

    def get_selected_reduced_output(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        return o_gui_utility.get_reduced_yaxis_type()

    def display_loaded_ascii(self, _data_object):
        """
        plot data coming from ascii file loaded
        """
        _q_axis = _data_object.col1
        _y_axis = _data_object.col2
        _e_axis = _data_object.col3

        self.stitchingPlot.errorbar(_q_axis, _y_axis, yerr=_e_axis)
        self.stitchingPlot.draw()
