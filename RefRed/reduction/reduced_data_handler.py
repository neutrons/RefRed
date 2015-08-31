from PyQt4 import QtGui, QtCore
from RefRed.gui_handling.gui_utility import GuiUtility
from distutils.util import strtobool


class ReducedDataHandler(object):
    
    big_table_data = None
    
    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data

    def populate_table(self):
        self.clear_stiching_table()
        self.fill_all_cells()
        
        
    def fill_all_cells(self):
        big_table_data = self.big_table_data
        for index_row, _lconfig in enumerate(big_table_data[:,2]):
            if _lconfig is None:
                return
            
            #run number
            _run_number = self.parent.ui.reductionTable.item(index_row, 1).text()
            _run_item = QtGui.QTableWidgetItem(_run_number)
            _run_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.parent.ui.dataStitchingTable.setItem(index_row, 0, _run_item)
            
            #auto SF
            _bruch = QtGui.QBrush()
            print('_lconfig.sf_auto_found_match ', _lconfig.sf_auto_found_match)
            if strtobool(_lconfig.sf_auto_found_match):
                _brush.setColor(QtCore.Qt.green)
            else:
                _brush.setColor(QtCore.Qt.red)
            sf_auto = "%.2f" %_lconfig.sf_auto
            _auto_item = QtGui.QTableWidgetItem(sf_auto)
            _auto_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _auto_item.setForeground(_brush)
            self.parent.ui.dataStitchingTable.setItem(index_row, 1, _auto_item)
            
            #manual SF
            _widget_manual = QtGui.QDoubleSpinBox()
            _widget_manual.setMinimum(0)
            _widget_manual.setValue(_lconfig.sf_manual)
            _widget_manual.setSingleStep(0.01)
            _widget_manual.valueChanged.connect(self.parent.data_stitching_table_manual_spin_box)
            self.parent.ui.dataStitchingTable.setCellWidget(index_row, 2, _widget_manual)
            
            #1 SF
            _item_1 = QtGui.QTableWidgetItem(str(1))
            _item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.parent.ui.dataStitchingTable.setItem(index_row, 3, _item_1)

    def clear_stiching_table(self):
        o_gui_utility = GuiUtility(parent = self.parent)
        o_gui_utility.clear_table(self.parent.ui.dataStitchingTable)
        
    def plot(self):
        print('plot')
        