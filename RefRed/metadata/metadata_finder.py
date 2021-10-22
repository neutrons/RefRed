from pathlib import Path
from qtpy.QtGui import QPalette, QPixmap, QIcon
from qtpy.QtWidgets import (
    QMainWindow,
    QCheckBox,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
    QPushButton,
)
from qtpy.QtCore import Qt, QSize, QSettings
from mantid.simpleapi import LoadEventNexus
import os
import time
import numpy as np

from RefRed.interfaces import load_ui
from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker
from RefRed.decorators import waiting_effects
from RefRed.widgets import getSaveFileName
import RefRed.utilities
import RefRed.nexus_utilities


class MetadataFinder(QMainWindow):

    _open_instances = []
    parent = None

    list_metadata_selected = []
    list_nxs = []
    list_filename = []
    list_runs = []

    list_values = []
    list_keys = []

    WARNING_NBR_FILES = 10

    first_load = True

    def __init__(self, parent=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.setWindowModality(False)
        self._open_instances.append(self)
        self.ui = load_ui("metadata_finder_interface.ui", self)

        self.initGui()

    def initList(self):
        self.list_runs = []
        self.list_filename = []
        self.list_nxs = []

    def initGui(self):
        self.ui.inputErrorLabel.setVisible(False)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.red)
        self.ui.inputErrorLabel.setPalette(palette)

        # as long as issue with routine not fixed
        self.ui.saveAsciiButton.setVisible(False)

        self.ui.configureTable.setColumnWidth(0, 70)
        self.ui.configureTable.setColumnWidth(1, 300)
        self.ui.configureTable.setColumnWidth(2, 300)
        self.ui.configureTable.setColumnWidth(3, 300)

        magIcon = QPixmap("../icons/magnifier.png")
        self.ui.searchLabel.setPixmap(magIcon)
        clearIcon = QIcon("../icons/clear.png")
        self.ui.clearButton.setIcon(clearIcon)
        sz = QSize(15, 15)
        self.ui.clearButton.setIconSize(sz)
        # self.ui.clearButton.setVisible(False)
        # self.ui.searchLabel.setVisible(False)
        # self.ui.searchLineEdit.setVisible(False)

    def initListMetadata(self):
        _nxs = self.list_nxs[0]
        mt_run = _nxs.getRun()
        self.list_keys = list(mt_run.keys())
        sz = len(self.list_keys)
        self.list_values = np.zeros(sz, dtype=bool)

    def searchLineEditLive(self, txt):
        self.populateconfigureTable()
        self.list_metadata_selected = self.getNewListMetadataSelected()
        self.loadAndPopulateMetadataTable()

    def searchLineEditClear(self):
        self.ui.searchLineEdit.setText("")
        self.populateconfigureTable()

    def retrieveListMetadataPreviouslySelected(self):
        settings = QSettings()
        nbr_metadata = str(settings.value("nbr_metadata"))
        list_metadata_selected = []
        if nbr_metadata != "":
            for index in range(int(nbr_metadata)):
                _name = "metadata_#%d" % index
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

    def clearMetadataTable(self):
        _meta_table = self.ui.metadataTable
        nbr_row = _meta_table.rowCount()
        for i in range(nbr_row):
            _meta_table.removeRow(0)
        nbr_column = _meta_table.columnCount()
        if nbr_column > 2:
            for j in range(nbr_column, 1, -1):
                _meta_table.removeColumn(j)
        _meta_table.show()

    def clearConfigureTable(self):
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        for i in range(nbr_row):
            _config_table.removeRow(0)
        _config_table.show()

    @waiting_effects
    def runNumberEditEvent(self):
        self.initList()
        self.clearMetadataTable()
        self.loadNxs()
        self.populateMetadataTable()
        self.populateconfigureTable()
        self.ui.runNumberEdit.setText("")
        self.updateGUI()
        self.list_metadata_selected = self.getNewListMetadataSelected()
        self.loadAndPopulateMetadataTable()

    def updateGUI(self):
        if self.list_nxs != []:
            config_widget_status = True
        else:
            config_widget_status = False
        self.ui.unselectAll.setEnabled(config_widget_status)
        self.ui.exportConfiguration.setEnabled(config_widget_status)
        self.ui.importConfiguration.setEnabled(config_widget_status)
        self.ui.saveAsciiButton.setEnabled(config_widget_status)

    def populateconfigureTable(self):
        if self.ui.inputErrorLabel.isVisible():
            return
        if self.list_filename == []:
            return
        self.clearConfigureTable()
        # _filename = self.list_filename[0]
        # nxs = LoadEventNexus(Filename=_filename)

        nxs = self.list_nxs[0]
        if self.first_load:
            self.first_load = False
            # mt_run = nxs.getRun()
            # self.list_keys = mt_run.keys()
            self.initListMetadata()
            self.retrieveListMetadataPreviouslySelected()

        list_keys = self.list_keys
        list_values = self.list_values
        search_string = str(self.ui.searchLineEdit.text()).lower()

        _index = 0
        for _key in list_keys:
            _name = _key
            if (search_string.strip() != "") and (not (search_string in _name.lower())):
                continue

            self.ui.configureTable.insertRow(_index)

            _yesNo = QCheckBox()
            _id = list_keys.index(_name)
            _value = list_values[_id]
            _yesNo.setChecked(_value)
            _yesNo.setText("")
            _yesNo.stateChanged.connect(self.configTableEdited)
            self.ui.configureTable.setCellWidget(_index, 0, _yesNo)

            _nameItem = QTableWidgetItem(_name)
            self.ui.configureTable.setItem(_index, 1, _nameItem)

            [value, units] = self.retrieveValueUnits(nxs.getRun(), _name)
            _valueItem = QTableWidgetItem(value)
            self.ui.configureTable.setItem(_index, 2, _valueItem)
            _unitsItem = QTableWidgetItem(units)
            self.ui.configureTable.setItem(_index, 3, _unitsItem)

            _index += 1

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

    def retrieveValueUnits(self, mt_run, _name):
        _name = str(_name)
        _value = mt_run.getProperty(_name).value
        if isinstance(_value, float):
            _value = str(_value)
        elif len(_value) == 1:
            _value = str(_value)
        elif isinstance(_value, list):
            _value = _value
        else:
            _value = f"[{_value[0]},...]-> ({len(_value)} entries)"
        _units = mt_run.getProperty(_name).units
        return [_value, _units]

    def loadAndPopulateMetadataTable(self):
        self.loadNxs()
        self.populateMetadataTable()

    def loadNxs(self):
        self.clearMetadataTable()
        run_sequence = self.ui.runNumberEdit.text()
        oListRuns = RunSequenceBreaker(run_sequence)
        _list_runs = oListRuns.getFinalList()
        if len(_list_runs) > self.WARNING_NBR_FILES:
            msgBox = QMessageBox()
            _str = "Program is about to load {:%d} files. Do you want to continue ?".format(
                len(_list_runs)
            )
            msgBox.setText(_str)
            msgBox.addButton(QPushButton("NO"), QMessageBox.NoRole)
            msgBox.addButton(QPushButton("YES"), QMessageBox.YesRole)
            ret = msgBox.exec_()
            if ret == 0:
                self.ui.inputErrorLabel.setVisible(False)
                return

        if _list_runs[0] == -1:
            if self.list_nxs == []:
                return
            else:
                _list_runs = self.list_runs
                # _list_nxs = self.list_nxs
                # _list_filename = self.list_filename

        elif _list_runs[0] == -2:
            self.ui.inputErrorLabel.setVisible(True)
            return

        else:
            self.list_runs = _list_runs
            self.list_filename = []
            self.list_nxs = []
            for _runs in _list_runs:
                try:
                    _filename = RefRed.nexus_utilities.findNeXusFullPath(_runs)
                except RuntimeError:
                    self.ui.inputErrorLabel.setVisible(True)
                    return
                self.list_filename.append(_filename)
                randomString = RefRed.utilities.generate_random_workspace_name()
                print(("About to load %s" % _filename))
                _nxs = LoadEventNexus(
                    Filename=_filename, OutputWorkspace=randomString, MetaDataOnly=True
                )
                self.list_nxs.append(_nxs)

        self.ui.inputErrorLabel.setVisible(False)
        list_metadata_selected = self.list_metadata_selected

        _header = ["Run #", "IPTS"]
        for name in list_metadata_selected:
            self.ui.metadataTable.insertColumn(2)
            _header.append(name)
        self.ui.metadataTable.setHorizontalHeaderLabels(_header)
        # list_nxs = self.list_nxs

    def populateMetadataTable(self):
        list_metadata_selected = self.list_metadata_selected

        _index = 0
        for i in range(len(self.list_nxs)):
            self.ui.metadataTable.insertRow(_index)

            _nxs = self.list_nxs[i]
            mt_run = _nxs.getRun()

            _runs = self.list_runs[i]
            _runItem = QTableWidgetItem(str(_runs))
            self.ui.metadataTable.setItem(_index, 0, _runItem)

            _filename = self.list_filename[i]
            _ipts = self.getIPTS(_filename)
            _iptsItem = QTableWidgetItem(_ipts)
            self.ui.metadataTable.setItem(_index, 1, _iptsItem)

            column_index = 0
            for name in list_metadata_selected:
                [value, units] = self.retrieveValueUnits(mt_run, name)
                _str = str(value) + " " + str(units)
                _item = QTableWidgetItem(_str)
                self.ui.metadataTable.setItem(_index, 2 + column_index, _item)
                column_index += 1

            _index += 1

    def unselectAllClicked(self):
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        for r in range(nbr_row):
            # _name = self.ui.configureTable.item(r, 1).text()
            _yesNo = QCheckBox()
            _yesNo.setText("")
            self.ui.configureTable.setCellWidget(r, 0, _yesNo)

    def closeEvent(self, event=None):
        self.saveListMetadataSelected()

    def saveListMetadataSelected(self):
        list_metadata_selected = self.list_metadata_selected
        settings = QSettings()
        nbr_metadata = len(list_metadata_selected)
        settings.setValue("nbr_metadata", nbr_metadata)
        for index, metadata in enumerate(list_metadata_selected):
            name = "metadata_#%d" % index
            settings.setValue(name, metadata)

    def importConfigurationClicked(self):
        _filter = "Metadata Configuration (*_metadata.cfg);; All (*.*)"
        _default_path = self.parent.path_config

        rst = QFileDialog.getOpenFileName(
            self,
            "Import Metadata Configuration",
            directory=_default_path,
            filter=(_filter),
        )
        if isinstance(rst, tuple):
            filename, _ = rst
        else:
            filename = rst

        if filename == "":
            return

        data = RefRed.utilities.import_ascii_file(filename)
        self.list_metadata_selected = data
        self.populateconfigureTable()

    def exportConfigurationClicked(self):
        _filter = "Metadata Configuration (*_metadata.cfg);; All (*.*)"
        _date = time.strftime("%d_%m_%Y")
        _default_name = Path(self.parent.path_config) / f"{_date}_metadata.cfg"
        _caption = "Export Metadata Configuration"
        filename, _ = getSaveFileName(self, _caption, str(_default_name), _filter)

        if filename:
            self.parent.path_config = os.path.dirname(filename)

            list_metadata_selected = self.list_metadata_selected
            text = []
            for _name in list_metadata_selected:
                text.append(_name)

            filename = RefRed.utilities.makeSureFileHasExtension(
                filename, default_ext=".cfg"
            )
            RefRed.utilities.write_ascii_file(filename, text)

    def getIPTS(self, filename):
        parse_path = filename.split("/")
        return parse_path[3]

    def userChangedTab(self, int_value):
        if int_value == 0:  # metadata
            self.list_metadata_selected = self.getNewListMetadataSelected()
            self.loadAndPopulateMetadataTable()

    def getNewListMetadataSelected(self):
        _config_table = self.ui.configureTable
        nbr_row = _config_table.rowCount()
        if nbr_row == 0:
            return self.list_metadata_selected
        _list_metadata_selected = []
        for r in range(nbr_row):
            _is_selected = _config_table.cellWidget(r, 0).isChecked()
            if _is_selected:
                _name = _config_table.item(r, 1).text()
                _list_metadata_selected.append(_name)
        return _list_metadata_selected

    def saveMetadataListAsAsciiFile(self):
        if self.list_runs == []:
            return
        _filter = "List Metadata (*_metadata.txt);;All(*.*)"
        _run_number = str(self.list_runs[0])
        _default_name = Path(self.parent.path_ascii) / f"{_run_number}_metadata.txt"
        _caption = "Save Metadata into ASCII"
        filename, _ = getSaveFileName(self, _caption, str(_default_name), _filter)

        if filename:
            self.parent.path_config = os.path.dirname(filename)
            text = ["# Metadata Selected for run " + _run_number]
            text.append("#Name - Value - Units")

            _metadata_table = self.ui.metadataTable
            nbr_row = _metadata_table.rowCount()
            text = [
                " ".join([str(_metadata_table.item(r, i).text()) for i in range(3)])
                for r in range(nbr_row)
            ]
            RefRed.utilities.write_ascii_file(filename, text)
