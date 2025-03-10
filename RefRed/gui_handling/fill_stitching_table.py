from distutils.util import strtobool
from typing import Optional

from qtpy import QtCore, QtGui, QtWidgets

from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.tabledata import TableData


class ParentHandler(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data: Optional[TableData] = self.parent.big_table_data if parent else None


class FillStitchingTable(ParentHandler):
    def __init__(self, parent=None, row_index=0):
        super(FillStitchingTable, self).__init__(parent=parent)
        self.row_index = row_index

    def fillRow(self, row_index=0):
        self._row_index = row_index
        self._lconfig = self.big_table_data.reduction_config(self._row_index)
        if self._lconfig is None:
            return

        o_gui = GuiUtility(parent=self.parent)
        stitching_type = o_gui.getStitchingType()

        self.fillTableRunNumber()

        if stitching_type == "absolute":
            self.fillTableForAbsoluteNormalization()
        elif stitching_type == "auto":
            self.fillTableForAutoStitching()
        else:
            self.fillTableForManualStitching()

    def fillTableRunNumber(self):
        _run_number = self.parent.ui.reductionTable.item(self._row_index, 1).text()
        _run_item = QtWidgets.QTableWidgetItem(_run_number)
        _run_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.parent.ui.dataStitchingTable.setItem(self._row_index, 0, _run_item)

    def fillTableForAbsoluteNormalization(self):
        _sf = self._lconfig.sf_abs_normalization
        self.fillTableForAbsoluteAndAuto(_sf)

    def fillTableForAutoStitching(self):
        _sf = self._lconfig.sf_auto
        self.fillTableForAbsoluteAndAuto(_sf)

    def fillTableForAbsoluteAndAuto(self, _sf):
        _color = QtGui.QColor(QtCore.Qt.red)
        if strtobool(str(self._lconfig.sf_auto_found_match)):
            _color = QtGui.QColor(QtCore.Qt.darkGreen)

        sf = "%.4f" % _sf
        _auto_item = QtWidgets.QTableWidgetItem(sf)
        _auto_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        _auto_item.setForeground(_color)
        self.parent.ui.dataStitchingTable.setItem(self._row_index, 1, _auto_item)

    def fillTableForManualStitching(self):
        try:
            # assume PyQt4
            _widget_manual = QtGui.QDoubleSpinBox()
        except AttributeError:
            # assume PyQt5
            _widget_manual = QtWidgets.QDoubleSpinBox()

        _widget_manual.setMinimum(0.0)
        sf_manual = self._lconfig.sf_manual
        _widget_manual.setValue(sf_manual)
        _widget_manual.setSingleStep(0.001)
        _widget_manual.setDecimals(6)
        _widget_manual.valueChanged.connect(self.parent.data_stitching_table_manual_spin_box)
        self.parent.ui.dataStitchingTable.setCellWidget(self._row_index, 1, _widget_manual)
