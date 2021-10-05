from qtpy.QtGui import QPixmap, QIcon
from qtpy.QtWidgets import QMainWindow, QCheckBox, QTableWidgetItem, QFileDialog
from qtpy.QtCore import QSize, QSettings
from xml.dom import minidom
import numpy as np
import os
import time

from RefRed.interfaces.display_metadata_interface import Ui_MainWindow as MainWindow
from RefRed.gui_handling.gui_utility import GuiUtility
import RefRed.utilities


class DisplayMetadata(QMainWindow):

    parent = None
    lrdata = None

    row = 0
    col = 0

    dom = None
    fields = None
    table = []
    list_metadata_selected = []
    mt_run = None

    list_keys = []
    list_values = []

    def __init__(self, parent=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.setWindowModality(False)
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.metadataTable.setColumnWidth(0, 300)
        self.ui.metadataTable.setColumnWidth(1, 200)
        self.ui.metadataTable.setColumnWidth(2, 200)

        self.ui.configureTable.setColumnWidth(0, 70)
        self.ui.configureTable.setColumnWidth(1, 300)
        self.ui.configureTable.setColumnWidth(2, 300)
        self.ui.configureTable.setColumnWidth(3, 300)

        self.retrieve_lradata()
        self.init_gui()
        self.initListMetadata()

        self.retrieveListMetadataPreviouslySelected()
        self.populateMetadataTable()
        self.populateConfigTable()

    def retrieve_lradata(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        col_selected = o_gui_utility.get_current_table_reduction_column_selected()
        row_selected = o_gui_utility.get_current_table_reduction_row_selected()
        self.col = col_selected
        self.row = row_selected
        big_table_data = self.parent.big_table_data
        self.lrdata = big_table_data[row_selected, col_selected - 1]

    def initListMetadata(self):
        wks = self.lrdata.workspace
        self.mt_run = wks.getRun()
        self.list_keys = list(self.mt_run.keys())
        sz = len(self.list_keys)
        self.list_values = np.zeros(sz, dtype=bool)

    def liveEditSearchLineEdit(self, str_value):
        self.populateMetadataTable()
        self.populateConfigTable()

    def clearSearchLineEdit(self):
        self.ui.searchLineEdit.setText('')
        self.populateMetadataTable()
        self.populateConfigTable()

    def clearMetadataTable(self):
        _meta_table = self.ui.metadataTable
        nbr_row = _meta_table.rowCount()
        for i in range(nbr_row):
            _meta_table.removeRow(0)
        _meta_table.show()

    def clearConfigTable(self):
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        for i in range(nbr_row):
            _config_table.removeRow(0)
        _config_table.show()

    def populateMetadataTable(self):
        self.clearMetadataTable()
        list_metadata_selected = self.list_metadata_selected
        if list_metadata_selected is None:
            self.ui.saveMetadataAsAsciiButton.setEnabled(False)
            return
        else:
            list_keys = self.list_keys
            search_string = str(self.ui.searchLineEdit.text())
            _index = 0
            for _key in list_keys:
                if _key in list_metadata_selected:
                    _name = _key
                    if (search_string != '') and (not (search_string.lower() in _name.lower())):
                        continue

                    self.ui.metadataTable.insertRow(_index)

                    _nameItem = QTableWidgetItem(_name)
                    self.ui.metadataTable.setItem(_index, 0, _nameItem)

                    [value, units] = self.retrieveValueUnits(_name)
                    _valueItem = QTableWidgetItem(value)
                    self.ui.metadataTable.setItem(_index, 1, _valueItem)
                    _unitsItem = QTableWidgetItem(units)
                    self.ui.metadataTable.setItem(_index, 2, _unitsItem)

                    _index += 1
        self.ui.saveMetadataAsAsciiButton.setEnabled(True)

    def populateConfigTable(self):
        self.clearConfigTable()
        list_keys = self.list_keys
        list_values = self.list_values
        search_string = str(self.ui.searchLineEdit.text()).lower()

        _metadata_table = self.list_metadata_selected
        _index = 0
        for _key in list_keys:
            _name = _key

            if (search_string.strip() != '') and (not (search_string in _name.lower())):
                continue

            self.ui.configureTable.insertRow(_index)

            _nameItem = QTableWidgetItem(_name)
            self.ui.configureTable.setItem(_index, 1, _nameItem)

            _yesNo = QCheckBox()
            _id = list_keys.index(_name)
            _value = list_values[_id]
            _yesNo.setChecked(_value)
            _yesNo.setText('')
            _yesNo.stateChanged.connect(self.configTableEdited)
            self.ui.configureTable.setCellWidget(_index, 0, _yesNo)

            [value, units] = self.retrieveValueUnits(_name)
            _valueItem = QTableWidgetItem(value)
            self.ui.configureTable.setItem(_index, 2, _valueItem)
            _unitsItem = QTableWidgetItem(units)
            self.ui.configureTable.setItem(_index, 3, _unitsItem)

            _index += 1

    def retrieveValueUnits(self, _name):
        mt_run = self.mt_run
        _value = mt_run.getProperty(_name).value
        if isinstance(_value, float):
            _value = str(_value)
        elif len(_value) == 1:
            _value = str(_value)
        elif type(_value) == type(""):
            _value = _value
        else:
            _value = '[' + str(_value[0]) + ',...]' + '-> (' + str(len(_value)) + ' entries)'
        _units = mt_run.getProperty(_name).units
        return [_value, _units]

    def retrieveListMetadataPreviouslySelected(self):
        settings = QSettings()
        nbr_metadata = str(settings.value("nbr_metadata"))
        list_metadata_selected = []
        if nbr_metadata is not '':
            for index in range(int(nbr_metadata)):
                _name = 'metadata_#%d' % index
                _value = str(settings.value(_name))
                list_metadata_selected.append(_value)
        self.list_metadata_selected = list_metadata_selected
        _list_values = self.list_values
        for idx, val in enumerate(self.list_keys):
            if val in list_metadata_selected:
                _list_values[idx] = True
            else:
                _list_values[idx] = False
        self.list_values = _list_values

    def init_gui(self):
        _run_number = self.retrieve_run_number()
        title = 'Metadata of run %s' % _run_number
        self.setWindowTitle(title)
        magIcon = QPixmap('../icons/magnifier.png')
        self.ui.searchLabel.setPixmap(magIcon)
        clearIcon = QIcon('../icons/clear.png')
        self.ui.clearButton.setIcon(clearIcon)
        sz = QSize(15, 15)
        self.ui.clearButton.setIconSize(sz)

    def retrieve_run_number(self):
        _col = self.col
        _row = self.row
        run_number = self.parent.ui.reductionTable.item(_row, _col).text()
        return run_number

    def close_gui(self):
        self.close()

    def getNodeValue(self, node, flag):
        try:
            _tmp = node.getElementsByTagName(flag)
            _value = _tmp[0].childNodes[0].nodeValue
        except:
            _value = ''
        return _value

    def userChangedTab(self, tab_index):
        if tab_index == 0:  # user is back on metadata tab
            self.list_metadata_selected = self.getNewListMetadataSelected()
            self.populateMetadataTable()

    def getNewListMetadataSelected(self):
        _list_keys = self.list_keys
        _list_values = self.list_values
        _list_metadata_selected = []
        for idx, val in enumerate(_list_values):
            if val == True:
                _list_metadata_selected.append(_list_keys[idx])
        return _list_metadata_selected

        # _config_table = self.ui.configureTable
        # nbr_row = _config_table.rowCount()
        # _list_metadata_selected = []
        # for r in range(nbr_row):
        # _is_selected = _config_table.cellWidget(r,0).isChecked()
        # if _is_selected:
        # _name = _config_table.item(r,1).text()
        # _list_metadata_selected.append(_name)
        # return _list_metadata_selected

    def configTableEdited(self, value):
        _list_keys = self.list_keys
        _list_values = self.list_values
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        _list_metadata_selected = []
        for r in range(nbr_row):
            _is_selected = _config_table.cellWidget(r, 0).isChecked()
            _name = _config_table.item(r, 1).text()
            if _is_selected:
                _list_metadata_selected.append(_name)
            _index = _list_keys.index(_name)
            _list_values[_index] = _is_selected

        self.list_values = _list_values
        self.list_metadata_selected = _list_metadata_selected

    def saveListMetadataSelected(self):
        list_metadata_selected = self.list_metadata_selected
        settings = QSettings()
        nbr_metadata = len(list_metadata_selected)
        settings.setValue('nbr_metadata', nbr_metadata)
        for index, metadata in enumerate(list_metadata_selected):
            name = 'metadata_#%d' % index
            settings.setValue(name, metadata)

    def saveMetadataListAsAscii(self):
        _filter = 'List Metadata (*_metadata.txt);;All(*.*)'
        _run_number = self.active_data.run_number
        _default_name = self.parent.path_ascii + '/' + _run_number + '_metadata.txt'
        filename = QFileDialog.getSaveFileName(self, 'Save Metadata into ASCII', _default_name, filter=_filter)
        if filename == '':
            return

        self.parent.path_config = os.path.dirname(filename)

        text = ['# Metadata Selected for run ' + _run_number]
        text.append('#Name - Value - Units')

        _metadata_table = self.ui.metadataTable
        nbr_row = _metadata_table.rowCount()
        for r in range(nbr_row):
            _line = (
                _metadata_table.item(r, 0).text()
                + ' '
                + str(_metadata_table.item(r, 1).text())
                + ' '
                + str(_metadata_table.item(r, 2).text())
            )
            text.append(_line)
        RefRed.utilities.write_ascii_file(filename, text)

    def exportConfiguration(self):
        _filter = "Metadata Configuration (*_metadata.cfg);; All (*.*)"
        _date = time.strftime("%d_%m_%Y")
        _default_name = self.parent.path_config + '/' + _date + '_metadata.cfg'
        filename = QFileDialog.getSaveFileName(self, 'Export Metadata Configuration', _default_name, filter=(_filter))
        if filename == '':
            return

        self.parent.path_config = os.path.dirname(filename)

        list_metadata_selected = self.list_metadata_selected
        text = []
        for _name in list_metadata_selected:
            text.append(_name)

        RefRed.utilities.write_ascii_file(filename, text)

    def importConfiguration(self):
        _filter = "Metadata Configuration (*_metadata.cfg);; All (*.*)"
        _default_path = self.parent.path_config
        filename = QFileDialog.getOpenFileName(
            self, 'Import Metadata Configuration', directory=_default_path, filter=(_filter)
        )
        if filename == '':
            return

        data = RefRed.utilities.import_ascii_file(filename)
        self.list_metadata_selected = data
        self.checkTrueImportedMetadataFromConfigFile()

    def checkTrueImportedMetadataFromConfigFile(self):
        list_metadata_selected = self.list_metadata_selected
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        for r in range(nbr_row):
            _name = self.ui.configureTable.item(r, 1).text()
            _yesNo = QCheckBox()
            if _name in list_metadata_selected:
                _yesNo.setChecked(True)
            _yesNo.setText('')
            self.ui.configureTable.setCellWidget(r, 0, _yesNo)

    def unselectAll(self):
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        for r in range(nbr_row):
            _name = self.ui.configureTable.item(r, 1).text()
            _yesNo = QCheckBox()
            _yesNo.setText('')
            self.ui.configureTable.setCellWidget(r, 0, _yesNo)

    def closeEvent(self, event=None):
        self.saveListMetadataSelected()
