# standard imports

# third party imports
from qtpy import QtCore, QtGui, QtWidgets

# application imports
from RefRed import WINDOW_TITLE
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.interfaces.mytablewidget import ReductionTableColumnIndex
from RefRed.plot.clear_plots import ClearPlots
from RefRed.tabledata import TableData


class ReductionTableHandler(object):

    from_row = -1
    to_row = -1

    def __init__(self, parent=None):
        self.parent = parent
        self.table = parent.ui.reductionTable

    def full_clear(self):
        self.__clear_big_table_data()
        self.clear_reduction_table()
        self.__clear_metadata()
        self.__clear_plots()
        self.__reset_default_config_file_name()

    def __reset_default_config_file_name(self):
        str_new_window_title = "%s%s" % (WINDOW_TITLE, self.parent.default_loaded_file)
        self.parent.setWindowTitle(str_new_window_title)
        self.parent.ui.previewLive.setEnabled(False)
        self.parent.ui.actionExportScript.setEnabled(False)

    def clear_rows_selected(self):
        self.__get_range_row_selected()
        if self.__is_row_displayed_in_range_selected():
            self.__clear_metadata()
            self.__clear_plots()
        self.__clear_rows_big_table_data()
        self.__clear_rows_reduction_table()
        self.__shift_none_empty_rows_reduction_table()
        self.__to_do_if_table_empty()

    def __to_do_if_table_empty(self):
        """If the table is now empty, various reset algos"""
        _cell_value = str(self.table.item(0, 1).text())
        if _cell_value == "":
            self.__reset_default_config_file_name()

    def __clear_rows_reduction_table(self):
        _from_row = self.from_row
        _to_row = self.to_row
        _nbr_col = self.table.columnCount()
        for row_index in range(_from_row, _to_row + 1):
            for col_index in range(_nbr_col):
                self.__clear_reduction_table_cell(row_index, col_index)

    def __shift_none_empty_rows_reduction_table(self):
        """Shift rows in the reduction table to eliminate empty rows"""
        _nbr_row = self.parent.REDUCTIONTABLE_MAX_ROWCOUNT
        _to_row = self.to_row
        if _to_row == (_nbr_row - 1):
            return

        _from_row = self.from_row
        _row_offset = 0
        _nbr_col = self.table.columnCount()
        for row_index in range(_to_row + 1, _nbr_row):
            _target_row_index = _from_row + _row_offset
            for col_index in range(_nbr_col):
                self.__copy_reduction_table_cell_value(row_index, _target_row_index, col_index)
            _row_offset += 1

    def __clear_rows_big_table_data(self):
        r"""Delete rows with indexes in the range [self.from_row, self.to_row]

        The table is appended with as many rows as deleted to keep the size unchanged. The
        elements of the appended rows are all `None`
        """
        self.parent.big_table_data.expunge_rows(self.from_row, self.to_row + 1)

    def __is_row_displayed_in_range_selected(self):
        _range_selected = list(range(self.from_row, self.to_row + 1))
        o_gui_utility = GuiUtility(parent=self.parent)
        _row_displayed = o_gui_utility.get_current_table_reduction_check_box_checked()
        if _row_displayed == -1:
            return False
        if _row_displayed in _range_selected:
            return True
        return False

    def __get_range_row_selected(self):
        selected_range = self.table.selectedRanges()
        self.to_row = selected_range[0].bottomRow()
        self.from_row = selected_range[0].topRow()

    def __clear_metadata(self):
        parent = self.parent
        parent.ui.metadataProtonChargeValue.setText("N/A")
        parent.ui.metadataProtonChargeUnits.setText("units")
        parent.ui.metadataLambdaRequestedValue.setText("N/A")
        parent.ui.metadataLambdaRequestedUnits.setText("units")
        parent.ui.metadatathiValue.setText("N/A")
        parent.ui.metadatathiUnits.setText("units")
        parent.ui.metadatatthdValue.setText("N/A")
        parent.ui.metadatatthdUnits.setText("units")
        parent.ui.metadataS1WValue.setText("N/A")
        parent.ui.metadataS1HValue.setText("N/A")
        parent.ui.metadataS2WValue.setText("N/A")
        parent.ui.metadataS2HValue.setText("N/A")

    def __clear_plots(self):
        ClearPlots(
            self.parent,
            is_data=True,
            is_norm=True,
            plot_yt=True,
            plot_yi=True,
            plot_it=True,
            plot_ix=True,
        )

    def clear_reduction_table(self):
        nbr_row = self.table.rowCount()
        nbr_col = self.table.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):  # skips first column: plotted checkbox
                self.__clear_reduction_table_cell(_row, _col)

    def __clear_big_table_data(self):
        self.parent.big_table_data = TableData(self.parent.REDUCTIONTABLE_MAX_ROWCOUNT)

    def __copy_reduction_table_cell_value(self, from_row, to_row, col):
        """Copy the table cell value from one row to another in the same column"""
        # copy cell containing text
        from_item = self.__get_table_cell_item(from_row, col)
        to_item = self.__get_table_cell_item(to_row, col)
        if from_item and to_item:
            text = from_item.text()
            text_foreground = from_item.foreground()
            to_item.setText(text)
            to_item.setForeground(text_foreground)
        # copy cell containing checkbox
        from_checkbox = self.__get_table_cell_checkbox_widget(from_row, col)
        to_checkbox = self.__get_table_cell_checkbox_widget(to_row, col)
        if from_checkbox and to_checkbox:
            checked = from_checkbox.isChecked()
            to_checkbox.setChecked(checked)

    def __clear_reduction_table_cell(self, row: int, col: int):
        """
        Clear the reduction table cell given by row and col
        - cells containing a QTableWidgetItem are set to empty string
        - cells containing a QCheckBox are set as unchecked
        """
        item = self.__get_table_cell_item(row, col)
        if item:
            item.setText("")
            item.setForeground(QtGui.QBrush(QtCore.Qt.black))  # type: ignore
            item.setBackground(QtGui.QBrush())  # reset to default color
            if col in (ReductionTableColumnIndex.DATA_RUN, ReductionTableColumnIndex.NORM_RUN):
                flags = QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled  # type: ignore
            else:
                flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled  # type: ignore
            item.setFlags(flags)
        checkbox_widget = self.__get_table_cell_checkbox_widget(row, col)
        if checkbox_widget:
            checkbox_widget.setChecked(False)
            checkbox_widget.setEnabled(True)

    def set_table_item_text(self, row: int, col: int, text: str):
        """
        Set the text in the reduction table cell given by row and col

        Parameters
        ----------
        row: int
        col: int
        text: str

        Raises
        ------
        ValueError
            If the cell does not contain a QTableWidgetItem
        """
        item = self.__get_table_cell_item(row, col)
        if item is None:
            raise ValueError("Reduction table cell does not contain a QTableWidgetItem")
        item.setText(text)

    def __get_table_cell_item(self, row, col):
        """Get QTableWidgetItem in the reduction table cell given by row and col"""
        return self.table.item(row, col)

    def __get_table_cell_checkbox_widget(self, row, col):
        """
        Get QCheckBox widget in the reduction table cell given by row and col,
        whether it's the topmost cell widget or a child of the cell widget
        """
        cell_widget = self.table.cellWidget(row, col)
        if cell_widget is None:
            return None
        # check if the cell widget is a checkbox
        if isinstance(cell_widget, QtWidgets.QCheckBox):
            return cell_widget
        # check if the cell widget has a checkbox as a child
        checkbox = cell_widget.findChild(QtWidgets.QCheckBox)
        return checkbox

    def set_checkbox_state(self, row: int, col: int, checked: bool):
        """
        Set the state of the checkbox in the reduction table cell given by row and col

        Parameters
        ----------
        row: int
        col: int
        checked: bool

        Raises
        ------
        ValueError
            If the cell does not contain a QCheckBox
        """
        checkbox = self.__get_table_cell_checkbox_widget(row, col)
        if checkbox is None:
            raise ValueError("Reduction table cell does not contain a QCheckBox")
        checkbox.setChecked(checked)
