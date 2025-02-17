from RefRed.utilities import removeEmptyStrElementAndUpdateIndexSelected


class CheckSfRunReductionButtonStatus(object):
    sf_gui = None

    def __init__(self, parent=None):
        self.sf_gui = parent

    def isIncidentMediumReady(self):
        _list = [
            str(self.sf_gui.incidentMediumComboBox.itemText(i))
            for i in range(1, self.sf_gui.incidentMediumComboBox.count())
        ]
        _current_index = self.sf_gui.incidentMediumComboBox.currentIndex() - 1
        [_list, current_index] = removeEmptyStrElementAndUpdateIndexSelected(_list, _current_index)
        if _list == [] or current_index == -1:
            return False
        return True

    def isBigTableReady(self):
        nbr_row = self.sf_gui.tableWidget.rowCount()
        for _row in range(nbr_row):
            peak1 = str(self.sf_gui.tableWidget.item(_row, 10).text())
            peak2 = str(self.sf_gui.tableWidget.item(_row, 11).text())
            back1 = str(self.sf_gui.tableWidget.item(_row, 12).text())
            back2 = str(self.sf_gui.tableWidget.item(_row, 13).text())

            if (peak1 == "N/A") or (peak2 == "N/A") or (back1 == "N/A") or (back2 == "N/A"):
                return False

            if int(peak1) < int(back1):
                return False

            if int(back2) < int(peak2):
                return False

        return True

    def isOutputFileNameReady(self):
        output_file_name = self.sf_gui.sfFileNameLabel.text()
        if output_file_name == "N/A":
            return False
        return True

    def isEverythingReady(self):
        return self.isIncidentMediumReady() and self.isBigTableReady() and self.isOutputFileNameReady()
