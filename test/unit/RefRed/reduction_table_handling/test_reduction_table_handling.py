from unittest import mock

import pytest
from qtpy import QtWidgets

from RefRed.interfaces.mytablewidget import ReductionTableColumnIndex
from RefRed.main import MainGui
from RefRed.reduction_table_handling.reduction_table_handler import ReductionTableHandler

NBR_ROWS = 6


@pytest.fixture
def setup_main_window_reduction_table():
    window_main = MainGui()
    table = window_main.ui.reductionTable
    for irow in range(NBR_ROWS):
        data_run = str(1000 + irow)
        norm_run = str(2000 + irow)
        table.item(irow, ReductionTableColumnIndex.DATA_RUN).setText(data_run)
        table.item(irow, ReductionTableColumnIndex.NORM_RUN).setText(norm_run)
        table.item(irow, ReductionTableColumnIndex.TWO_THETA).setText("3.0")
        table.item(irow, ReductionTableColumnIndex.LAMBDA_MIN).setText("2.5")
        table.item(irow, ReductionTableColumnIndex.LAMBDA_MAX).setText("6.5")
        table.item(irow, ReductionTableColumnIndex.Q_MIN).setText("0.1")
        table.item(irow, ReductionTableColumnIndex.Q_MAX).setText("1.7")
        table.item(irow, ReductionTableColumnIndex.COMMENTS).setText("comment " + data_run)
    yield window_main


class TestReductionTableHandling:
    def test_clear_reduction_table(self, setup_main_window_reduction_table, qtbot):
        window_main = setup_main_window_reduction_table
        qtbot.addWidget(window_main)
        table = window_main.ui.reductionTable

        for i in range(NBR_ROWS):
            assert table.item(i, ReductionTableColumnIndex.DATA_RUN).text() == str(1000 + i)
            assert table.item(i, ReductionTableColumnIndex.NORM_RUN).text() == str(2000 + i)

        handler = ReductionTableHandler(parent=window_main)
        handler.full_clear()

        for i in range(NBR_ROWS):
            assert table.item(i, ReductionTableColumnIndex.DATA_RUN).text() == ""
            assert table.item(i, ReductionTableColumnIndex.NORM_RUN).text() == ""
            assert table.item(i, ReductionTableColumnIndex.TWO_THETA).text() == ""
            assert table.item(i, ReductionTableColumnIndex.LAMBDA_MAX).text() == ""
            assert table.item(i, ReductionTableColumnIndex.LAMBDA_MAX).text() == ""
            assert table.item(i, ReductionTableColumnIndex.Q_MIN).text() == ""
            assert table.item(i, ReductionTableColumnIndex.Q_MAX).text() == ""
            assert table.item(i, ReductionTableColumnIndex.COMMENTS).text() == ""
            plotted_checkbox = table.cellWidget(i, ReductionTableColumnIndex.PLOTTED)
            assert not plotted_checkbox.isChecked()
            const_q_checkbox = table.cellWidget(i, ReductionTableColumnIndex.CONST_Q_BINS).findChild(
                QtWidgets.QCheckBox
            )
            assert not const_q_checkbox.isChecked()

    def test_clear_rows_selected(self, setup_main_window_reduction_table, qtbot):
        window_main = setup_main_window_reduction_table
        qtbot.addWidget(window_main)
        from_row = 2
        to_row = 3  # inclusive
        nbr_deleted = to_row + 1 - from_row

        # clear selected rows
        with mock.patch.object(ReductionTableHandler, "_ReductionTableHandler__get_range_row_selected"):
            handler = ReductionTableHandler(parent=window_main)
            handler.from_row = from_row
            handler.to_row = to_row
            handler.clear_rows_selected()

        table = window_main.ui.reductionTable
        # check that the rows up to from_row are unchanged
        for i in range(from_row):
            assert table.item(i, ReductionTableColumnIndex.DATA_RUN).text() == str(1000 + i)
            assert table.item(i, ReductionTableColumnIndex.NORM_RUN).text() == str(2000 + i)
        # check that the rows after to_row have been shifted up
        for i in range(from_row, NBR_ROWS - nbr_deleted):
            assert table.item(i, ReductionTableColumnIndex.DATA_RUN).text() == str(1000 + i + nbr_deleted)
            assert table.item(i, ReductionTableColumnIndex.NORM_RUN).text() == str(2000 + i + nbr_deleted)
        # check that the rows below are cleared
        for i in range(NBR_ROWS - nbr_deleted, NBR_ROWS):
            assert table.item(i, ReductionTableColumnIndex.DATA_RUN).text() == ""
            assert table.item(i, ReductionTableColumnIndex.NORM_RUN).text() == ""
