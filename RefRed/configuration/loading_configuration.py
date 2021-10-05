import os
from qtpy import QtGui, QtCore, QtWidgets
from xml.dom import minidom
from numpy import empty
from RefRed.lconfigdataset import LConfigDataset
from RefRed.configuration.populate_reduction_table_from_lconfigdataset import (
    PopulateReductionTableFromLConfigDataSet as PopulateReductionTable,
)
from RefRed.configuration.load_reduction_table_from_lconfigdataset import (
    LoadReductionTableFromLConfigDataSet as LoadReductionTable,
)
from RefRed.gui_handling.scaling_factor_widgets_handler import ScalingFactorWidgetsHandler
from RefRed.plot.clear_plots import ClearPlots
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.utilities import str2bool
from RefRed.status_message_handler import StatusMessageHandler


class LoadingConfiguration(object):

    parent = None
    load_config_worked = True
    filename = ''
    dom = None

    def __init__(self, parent=None):
        self.parent = parent
        self.filename = ''
        StatusMessageHandler(parent=self.parent, message='Loading config ...', is_threaded=False)

    def run(self):
        _path = self.parent.path_config
        _filter = "XML (*.xml);; All Files (*.*)"
        filename = ""
        file_dialog = QtWidgets.QFileDialog(self.parent, 'Open Configuration File', _path, _filter)
        file_dialog.setViewMode(QtWidgets.QFileDialog.List)
        if file_dialog.exec_():
            filename = file_dialog.selectedFiles()
        if isinstance(filename, list):
            filename = filename[-1]
        QtWidgets.QApplication.processEvents()
        if not (filename == "") and os.path.isfile(filename):
            self.filename = str(filename)
            self.loading()
            message = 'Done!'
        else:
            message = 'User Canceled loading!'

        StatusMessageHandler(parent=self.parent, message=message, is_threaded=True)

    def loading(self):
        self.parent.path_config = os.path.dirname(self.filename)
        self.clear_reductionTable()
        self.clear_display()
        self.display_name_config_file()
        self.load_config_in_big_table_data()
        self.populate_reduction_table_from_lconfigdataset()
        self.load_reduction_table_from_lconfigdataset()
        self.reset_gui_modified_status()
        self.live_preview_config_status()

    def live_preview_config_status(self):
        self.parent.ui.previewLive.setEnabled(True)
        self.parent.ui.actionExportScript.setEnabled(True)

    def reset_gui_modified_status(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        o_gui_utility.gui_not_modified()

    def display_name_config_file(self):
        o_gui = GuiUtility(parent=self.parent)
        o_gui.new_config_file_loaded(config_file_name=self.filename)

    def load_config_in_big_table_data(self):
        filename = self.filename
        self.dom = minidom.parse(filename)
        self.populate_big_table_data_with_lconfig()
        self.populate_main_gui_general_settings()

    def populate_big_table_data_with_lconfig(self):
        dom = self.dom
        RefLData = dom.getElementsByTagName('RefLData')

        big_table_data = empty((self.parent.nbr_row_table_reduction, 3), dtype=object)
        _row = 0
        for node in RefLData:
            _metadataObject = self.getMetadataObject(node)
            big_table_data[_row, 2] = _metadataObject
            _row += 1

        self.parent.big_table_data = big_table_data

    def populate_main_gui_general_settings(self):
        dom = self.dom
        RefLData = dom.getElementsByTagName('RefLData')
        node_0 = RefLData[0]

        q_step = self.getNodeValue(node_0, 'q_step')
        if q_step == '':
            q_step = '0.01'
        self.parent.ui.qStep.setText(q_step)

        q_min = self.getNodeValue(node_0, 'q_min')
        if q_min == '':
            q_min = '0.005'
        _gui_metadata = self.parent.gui_metadata
        _gui_metadata['q_min'] = q_min
        self.parent.gui_metadata = _gui_metadata

        angle_offset = self.getNodeValue(node_0, 'angle_offset')
        self.parent.ui.angleOffsetValue.setText(angle_offset)

        angle_offset_error = self.getNodeValue(node_0, 'angle_offset_error')
        self.parent.ui.angleOffsetError.setText(angle_offset_error)

        scaling_factor_file = self.getNodeValue(node_0, 'scaling_factor_file')
        self.parent.full_scaling_factor_file_name = scaling_factor_file
        short_scaling_factor_file = os.path.basename(scaling_factor_file)
        self.parent.ui.scalingFactorFile.setText(short_scaling_factor_file)

        o_scaling_factor_widget = ScalingFactorWidgetsHandler(parent=self.parent)
        o_scaling_factor_widget.fill_incident_medium_list(scaling_factor_file)
        # +1 to make mantid friendly
        index_selected = int(self.getNodeValue(node_0, 'incident_medium_index_selected')) + 1
        o_scaling_factor_widget.set_index_selected(index_selected)

        self.parent.path_ascii = os.path.dirname(scaling_factor_file)
        scaling_factor_flag = str2bool(self.getNodeValue(node_0, 'scaling_factor_flag'))
        o_scaling_factor_widget.checkbox(status=scaling_factor_flag)
        o_scaling_factor_widget.set_enabled(status=scaling_factor_flag)

    def getMetadataObject(self, node):
        iMetadata = LConfigDataset()

        _peak_min = self.getNodeValue(node, 'from_peak_pixels')
        _peak_max = self.getNodeValue(node, 'to_peak_pixels')
        iMetadata.data_peak = [_peak_min, _peak_max]

        _back_min = self.getNodeValue(node, 'back_roi1_from')
        _back_max = self.getNodeValue(node, 'back_roi1_to')
        iMetadata.data_back = [_back_min, _back_max]

        _low_res_min = self.getNodeValue(node, 'x_min_pixel')
        _low_res_max = self.getNodeValue(node, 'x_max_pixel')
        iMetadata.data_low_res = [_low_res_min, _low_res_max]

        _back_flag = self.getNodeValue(node, 'background_flag')
        iMetadata.data_back_flag = _back_flag

        _low_res_flag = self.getNodeValue(node, 'x_range_flag')
        iMetadata.data_low_res_flag = _low_res_flag

        _clocking_min = self.getNodeValue(node, 'clocking_from')
        _clocking_max = self.getNodeValue(node, 'clocking_to')
        iMetadata.data_clocking = [_clocking_min, _clocking_max]

        _tof_min = self.getNodeValue(node, 'from_tof_range')
        _tof_max = self.getNodeValue(node, 'to_tof_range')
        if float(_tof_min) < 500:  # ms
            _tof_min = str(float(_tof_min) * 1000)
            _tof_max = str(float(_tof_max) * 1000)
        iMetadata.tof_range = [_tof_min, _tof_max]

        _q_min = self.getNodeValue(node, 'from_q_range')
        _q_max = self.getNodeValue(node, 'to_q_range')
        iMetadata.q_range = [_q_min, _q_max]

        _lambda_min = self.getNodeValue(node, 'from_lambda_range')
        _lambda_max = self.getNodeValue(node, 'to_lambda_range')
        iMetadata.lambda_range = [_lambda_min, _lambda_max]

        iMetadata.tof_units = 'micros'

        _data_sets = self.getNodeValue(node, 'data_sets')
        _data_sets = _data_sets.split(',')
        iMetadata.data_sets = [str(x) for x in _data_sets]

        _tof_auto = self.getNodeValue(node, 'tof_range_flag')
        iMetadata.tof_auto_flag = _tof_auto

        _norm_flag = self.getNodeValue(node, 'norm_flag')
        iMetadata.norm_flag = _norm_flag

        _peak_min = self.getNodeValue(node, 'norm_from_peak_pixels')
        _peak_max = self.getNodeValue(node, 'norm_to_peak_pixels')
        iMetadata.norm_peak = [_peak_min, _peak_max]

        _back_min = self.getNodeValue(node, 'norm_from_back_pixels')
        _back_max = self.getNodeValue(node, 'norm_to_back_pixels')
        iMetadata.norm_back = [_back_min, _back_max]

        _norm_sets = self.getNodeValue(node, 'norm_dataset')
        _norm_sets = _norm_sets.split(',')
        iMetadata.norm_sets = [str(x) for x in _norm_sets]

        _low_res_min = self.getNodeValue(node, 'norm_x_min')
        _low_res_max = self.getNodeValue(node, 'norm_x_max')
        iMetadata.norm_low_res = [_low_res_min, _low_res_max]

        _back_flag = self.getNodeValue(node, 'norm_background_flag')
        iMetadata.norm_back_flag = _back_flag

        _low_res_flag = self.getNodeValue(node, 'norm_x_range_flag')
        iMetadata.norm_low_res_flag = _low_res_flag

        try:
            _data_full_file_name = self.getNodeValue(node, 'data_full_file_name')
            _data_full_file_name = _data_full_file_name.split(',')
            _data_full_file_name = [str(x) for x in _data_full_file_name]
        except:
            _data_full_file_name = ['']
        iMetadata.data_full_file_name = _data_full_file_name

        try:
            _norm_full_file_name = self.getNodeValue(node, 'norm_full_file_name')
            _norm_full_file_name = _norm_full_file_name.split(',')
            _norm_full_fil_name = [str(x) for x in _norm_full_file_name]
        except:
            _norm_full_file_name = ['']
        iMetadata.norm_full_file_name = _norm_full_file_name

        return iMetadata

    def getNodeValue(self, node, flag):
        try:
            _tmp = node.getElementsByTagName(flag)
            _value = _tmp[0].childNodes[0].nodeValue
        except:
            _value = ''
        return _value

    def clear_display(self):
        ClearPlots(parent=self.parent, is_data=True, is_norm=True, all_plots=True)

    def clear_reductionTable(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        _brush_color = QtGui.QBrush()
        _brush_color.setColor(QtCore.Qt.black)
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")
                self.parent.ui.reductionTable.item(_row, _col).setForeground(_brush_color)

    def populate_reduction_table_from_lconfigdataset(self):
        PopulateReductionTable(parent=self.parent)
        QtWidgets.QApplication.processEvents()

    def load_reduction_table_from_lconfigdataset(self):
        LoadReductionTable(parent=self.parent)
