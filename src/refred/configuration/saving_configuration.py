import os
from typing import TYPE_CHECKING

from qtpy import QtWidgets

from refred.configuration.export_xml_config import ExportXMLConfig
from refred.gui_handling.gui_utility import GuiUtility
from refred.status_message_handler import StatusMessageHandler
from refred.utilities import makeSureFileHasExtension

if TYPE_CHECKING:
    from refred.main import MainGui


class SavingConfiguration(object):
    """Class to save the current configuration to an XML file."""

    def __init__(self, parent: "MainGui", filename: str = ""):
        self.parent = parent
        self.filename = filename

        StatusMessageHandler(parent=self.parent, message="Saving config ...", is_threaded=False)

    def run(self):
        if self.filename == "":
            _path = self.parent.path_config
            _filter = "XML (*.xml);; All Files (*.*)"

            file_dialog = QtWidgets.QFileDialog(self.parent, "Save Configuration File", _path, _filter)
            file_dialog.setViewMode(QtWidgets.QFileDialog.List)
            file_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            # file_dialog.setConfirmOverwrite(True)
            # by default, confirmation is enabled, if needed, it can be turned
            # off with
            # file_dialog.setOption(QtWidgets.QFileDialog.DontConfirmOverwrite, True)

            if file_dialog.exec_():
                filename = file_dialog.selectedFiles()[0]
                QtWidgets.QApplication.processEvents()
                self.filename = str(filename)
            else:
                # No operation
                return

        self.parent.path_config = os.path.dirname(self.filename)
        self.filename = makeSureFileHasExtension(self.filename)
        export_config = ExportXMLConfig(parent=self.parent)
        try:
            export_config.save(self.filename)
        except (PermissionError, IsADirectoryError) as e:
            StatusMessageHandler(parent=self.parent, message=f"Error: {e}", is_threaded=True)
            return

        StatusMessageHandler(parent=self.parent, message="Done!", is_threaded=True)

        o_gui_utility = GuiUtility(parent=self.parent)
        o_gui_utility.new_config_file_loaded(config_file_name=self.filename)
        o_gui_utility.gui_not_modified()
