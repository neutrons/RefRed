from qtpy.QtWidgets import QDialog

from RefRed.interfaces import load_ui
from RefRed.utilities import removeEmptyStrElementAndUpdateIndexSelected


class IncidentMediumListEditor(QDialog):
    sf_gui = None
    current_index = -1

    def __init__(self, parent=None):
        self.sf_gui = parent

        QDialog.__init__(self, parent=parent)
        self.setWindowModality(False)
        self.ui = load_ui("incident_medium_list_editor_interface.ui", self)
        self.initGui()

    def initGui(self):
        _list = [
            str(self.sf_gui.incidentMediumComboBox.itemText(i))
            for i in range(1, self.sf_gui.incidentMediumComboBox.count())
        ]
        self.current_index = self.sf_gui.incidentMediumComboBox.currentIndex() - 1
        [_list, _] = removeEmptyStrElementAndUpdateIndexSelected(_list, self.current_index)
        self.fillGui(_list)

    def fillGui(self, _list):
        _text = "\n".join(_list)
        self.ui.textEdit.setText(_text)

    def validateEvent(self):
        text_medium = str(self.ui.textEdit.toPlainText())
        text_list = text_medium.split("\n")
        [text_list, current_index] = removeEmptyStrElementAndUpdateIndexSelected(text_list, self.current_index)
        text_list.insert(0, "Select or Define Incident Medium ...")
        self.sf_gui.incidentMediumComboBox.clear()
        self.sf_gui.incidentMediumComboBox.addItems(text_list)
        self.sf_gui.incidentMediumComboBox.setCurrentIndex(current_index)
        self.close()
