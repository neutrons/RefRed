from qtpy import QtGui, QtCore
from qtpy import QtWidgets
from RefRed.gui_handling.gui_utility import GuiUtility
from distutils.util import strtobool


class ParentHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data


class FillStitchingTable(ParentHandler):

    def __init__(self, parent=None, row_index=0):
        super(FillStitchingTable, self).__init__(parent = parent)
        self.row_index = row_index

    def fillRow(self, row_index=0):
        self._row_index = row_index
        self._lconfig = self.big_table_data[self._row_index, 2]
        if self._lconfig is None:
            return

        o_gui = GuiUtility(parent = self.parent)
        stitching_type = o_gui.getStitchingType()

        self.fillTableRunNumber()

        if stitching_type is 'absolute':
            self.fillTableForAbsoluteNormalization()
        elif stitching_type is 'auto':
            self.fillTableForAutoStitching()
        else:
            self.fillTableForManualStitching()

        self.fillTableForClocking()

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
        _brush = QtGui.QBrush()
        if strtobool(str(self._lconfig.sf_auto_found_match)):
            _brush.setColor(QtCore.Qt.darkGreen)
        else:
            _brush.setColor(QtCore.Qt.red)

        sf = "%.4f" %_sf
        _auto_item = QtWidgets.QTableWidgetItem(sf)
        _auto_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        _auto_item.setForeground(_brush)
        self.parent.ui.dataStitchingTable.setItem(self._row_index, 1, _auto_item)

    def fillTableForManualStitching(self):
        _widget_manual = QtGui.QDoubleSpinBox()
        _widget_manual.setMinimum(0.)
        sf_manual = self._lconfig.sf_manual
        _widget_manual.setValue(sf_manual)
        _widget_manual.setSingleStep(0.001)
        _widget_manual.valueChanged.connect(self.parent.data_stitching_table_manual_spin_box)
        self.parent.ui.dataStitchingTable.setCellWidget(self._row_index, 1, _widget_manual)

    def fillTableForClocking(self):
        sf_clock = "%.4f" % self._lconfig.sf_clocking
        _item_clock = QtWidgets.QTableWidgetItem(sf_clock)
        _item_clock.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        _brush = QtGui.QBrush()
        if self._lconfig.is_sf_clocking_used:
            _brush.setColor(QtCore.Qt.darkGreen)
        else:
            _brush.setColor(QtCore.Qt.red)
        _item_clock.setForeground(_brush)
        self.parent.ui.dataStitchingTable.setItem(self._row_index, 2, _item_clock)
