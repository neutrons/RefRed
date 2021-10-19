from qtpy import QtGui, QtWidgets
from xml.dom import minidom
from numpy import empty
from RefRed.interfaces import load_ui
import RefRed.colors


class PreviewConfig(QtWidgets.QMainWindow):

    system_name = [
        "instrument_name",
        "timestamp",
        "python_version",
        "platform",
        "architecture",
        "mantid_version",
    ]

    data_name = [
        "peak_selection_type",
        "from_peak_pixels",
        "to_peak_pixels",
        "peak_discrete_selection",
        "background_flag",
        "back_roi1_from",
        "back_roi1_to",
        "back_roi2_from",
        "back_roi2_to",
        "clocking_from",
        "clocking_to",
        "tof_range_flag",
        "from_tof_range",
        "to_tof_range",
        "data_sets",
        "x_min_pixel",
        "x_max_pixel",
        "x_range_flag",
        "tthd_value",
        "ths_value",
        "norm_flag",
        "norm_x_range_flag",
        "norm_x_max",
        "norm_x_min",
        "norm_from_peak_pixels",
        "norm_to_peak_pixels",
        "norm_background_flag",
        "norm_from_back_pixels",
        "norm_to_back_pixels",
        "norm_dataset",
        "q_min",
        "q_step",
        "auto_q_binning",
        "overlap_lowest_error",
        "overlap_mean_value",
        "angle_offset",
        "angle_offset_error",
        "scaling_factor_flag",
        "scaling_factor_file",
        "slits_width_flag",
        "geometry_correction_switch",
        "incident_medium_list",
        "incident_medium_index_selected",
        "fourth_column_flag",
        "fourth_column_dq0",
        "fourth_column_dq_over_q",
    ]

    _data_table = []
    _system_table = []
    _title = "Configuration File Preview"
    _colored_row = [14, 29]  # highlights data and norm rows

    def __init__(
        self,
        parent=None,
        is_live=False,
        filename=None,
        geometry_parent=None,
        window_offset=[0, 0],
        check_format=False,
    ):
        self.parent = parent

        if check_format:
            self.file_name = filename
            self.check_format()
            return

        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui("preview_configuration.ui", self)
        _title = self._title
        self.setWindowTitle(_title)

        if geometry_parent:
            current_geometry = self.geometry()
            current_geometry.setLeft(
                geometry_parent.left() + geometry_parent.width() + window_offset[0]
            )
            current_geometry.setTop(geometry_parent.top() + window_offset[1])
            self.setGeometry(current_geometry)

        if not filename:
            if not is_live:
                _file_name = self._browse_file_name()
                if _file_name == "":
                    return
            else:
                _file_name = self.parent.current_loaded_file
        else:
            _file_name = filename
            # disable browse button
            self.ui.menuFile.setEnabled(False)

        self.file_name = _file_name
        self.ui.config_file_name.setText(_file_name)
        self._display_raw_file()
        self._display_table()

    def check_format(self):
        _dom = minidom.parse(self.file_name)

        # system data
        _system_table = empty((len(self.system_name)), dtype=object)
        for _index, _name in enumerate(self.system_name):
            _value = str(_dom.getElementsByTagName(_name)[0].childNodes[0].data)
            _system_table[_index] = str(_value)

            refl_data = _dom.getElementsByTagName("RefLData")
            nbr_row = len(refl_data)
            _data_table = empty((nbr_row, len(self.data_name)), dtype=object)
            for _row_index, _run_node in enumerate(refl_data):
                for _child_index, _child_name in enumerate(self.data_name):
                    _value = self.get_node_value(_run_node, _child_name)
                    _data_table[_row_index, _child_index] = str(_value)
            self._data_table = _data_table

    def action_browse_button(self):
        _file_name = self._browse_file_name()
        if _file_name == "":
            return

        self.file_name = _file_name
        self.ui.config_file_name.setText(_file_name)
        self._display_raw_file()
        self._display_table()

    def _display_raw_file(self):
        with open(self.file_name, "r") as _file:
            data = _file.read()
        self.ui.rawTextEdit.setText(data)

    def _display_table(self):
        self.init_table_label()
        _dom = minidom.parse(self.file_name)
        self._work_on_system_data(_dom)
        self._work_on_runs_data(_dom)

    def init_table_label(self):
        self.ui.previewTableWidget.setRowCount(len(self.data_name))
        self.ui.previewTableWidget.setVerticalHeaderLabels(self.data_name)

        self.ui.systemTableWidget.setRowCount(len(self.system_name))
        self.ui.systemTableWidget.setVerticalHeaderLabels(self.system_name)

    def _work_on_runs_data(self, _dom):
        self._retrieve_runs_data(_dom)
        self._populate_runs_data()

    def _retrieve_runs_data(self, _dom):
        refl_data = _dom.getElementsByTagName("RefLData")
        nbr_row = len(refl_data)
        _data_table = empty((nbr_row, len(self.data_name)), dtype=object)
        for _row_index, _run_node in enumerate(refl_data):
            for _child_index, _child_name in enumerate(self.data_name):
                _value = self.get_node_value(_run_node, _child_name)
                _data_table[_row_index, _child_index] = str(_value)
        self._data_table = _data_table

    def _populate_runs_data(self):
        _data_table = self._data_table
        (nbr_column, nbr_row) = _data_table.shape
        self.ui.previewTableWidget.setColumnCount(nbr_column)
        for _column in range(nbr_column):
            for _row in range(nbr_row):
                _item = QtWidgets.QTableWidgetItem(_data_table[_column, _row])
                if _row in self._colored_row:
                    _brush = QtGui.QBrush()
                    _brush.setColor(RefRed.colors.VALUE_OK)
                    _item.setForeground(_brush)
                self.ui.previewTableWidget.setItem(_row, _column, _item)

    #        self.ui.previewTableWidget.resizeColumnsToContents()

    def get_node_value(self, node, flag):
        try:
            _tmp = node.getElementsByTagName(flag)
            _value = _tmp[0].childNodes[0].nodeValue
        except RuntimeError:
            _value = ""
        return _value

    def _work_on_system_data(self, _dom):
        self._retrieve_runs_system(_dom)
        self._populate_runs_system()

    def _retrieve_runs_system(self, _dom):
        _system_table = empty((len(self.system_name)), dtype=object)
        for _index, _name in enumerate(self.system_name):
            _value = str(_dom.getElementsByTagName(_name)[0].childNodes[0].data)
            _system_table[_index] = str(_value)

        self._system_table = _system_table

    def _populate_runs_system(self):
        _system_table = self._system_table
        nbr_row = len(_system_table)
        self.ui.systemTableWidget.setColumnCount(1)

        for _row in range(nbr_row):
            _item = QtWidgets.QTableWidgetItem(_system_table[_row])
            # if _row in self._colored_row:
            # _brush = QtGui.QBrush()
            # _brush.setColor(RefRed.colors.VALUE_OK)
            # _item.setForeground(_brush)
            self.ui.systemTableWidget.setItem(_row, 0, _item)
        self.ui.systemTableWidget.resizeColumnsToContents()

    def _browse_file_name(self):
        rst = QtWidgets.QFileDialog.getOpenFileName(
            self,
            caption="Select Configuration File",
            directory=self.parent.path_config,
            filter="Config (*.xml)",
        )

        if isinstance(rst, tuple):
            filename, _ = rst
        else:
            filename = rst

        return str(filename)
