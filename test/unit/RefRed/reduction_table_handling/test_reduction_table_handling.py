from RefRed.interfaces.mytablewidget import ReductionTableColumnIndex
from RefRed.main import MainGui
from RefRed.reduction_table_handling.reduction_table_handler import ReductionTableHandler


def test_clear_reduction_table(qtbot):
    window_main = MainGui()
    qtbot.addWidget(window_main)

    col_run_nbr = ReductionTableColumnIndex.DATA_RUN
    window_main.ui.reductionTable.item(0, col_run_nbr).setText("10001")
    window_main.ui.reductionTable.item(1, col_run_nbr).setText("10002")

    handler = ReductionTableHandler(parent=window_main)
    handler.full_clear()

    assert window_main.ui.reductionTable.item(0, col_run_nbr).text() == ""
    assert window_main.ui.reductionTable.item(1, col_run_nbr).text() == ""
