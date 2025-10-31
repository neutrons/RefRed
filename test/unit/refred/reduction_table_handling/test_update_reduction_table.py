import unittest.mock as mock

# third party packages
import pytest

from refred.interfaces.mytablewidget import ReductionTableColumnIndex as TableCol
from refred.main import MainGui
from refred.tabledata import TableDataColumIndex
from test.utilities import load_run_from_reduction_table

wait = 2000


@pytest.mark.parametrize("is_display_checked", [True, False])
@mock.patch("refred.main.DisplayPlots")
@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
def test_update_reduction_table_thread(
    mock_file_finder_find_runs, mock_display_plots, is_display_checked, qtbot, file_finder_find_runs
):
    """Test of the communication between the main thread and CheckListRunCompatibilityThread"""
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)

    window_main.ui.reductionTable.cellWidget(0, 0).setChecked(is_display_checked)  # click "Plotted" checkbox
    load_run_from_reduction_table(window_main, 0, 1, "184975")  # type 184975 in "Data Run #" column and press Enter
    qtbot.wait(wait)

    if is_display_checked:
        mock_display_plots.assert_called_once()
    else:
        mock_display_plots.assert_not_called()

    # check that the reduction table was re-enabled after the thread returned
    assert window_main.ui.reductionTable.isEnabled()


@pytest.mark.parametrize("col", [1, 2])  # data run column, normalization run column
@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
def test_empty_cell_press_enter(mock_file_finder_find_runs, col, qtbot, file_finder_find_runs):
    """Test pressing Enter in empty cell in the reduction table before and after data has been loaded"""
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)

    # test pressing Enter in empty cell before any data has been loaded
    load_run_from_reduction_table(window_main, 0, col, "")
    qtbot.wait(wait)
    # check that the reduction table was re-enabled after the function returned
    assert window_main.ui.reductionTable.isEnabled()

    # test first loading a run, then clearing the cell and pressing Enter to clear loaded data
    load_run_from_reduction_table(window_main, 0, col, "184975")
    qtbot.wait(wait)
    # check that the data has been loaded
    assert window_main.big_table_data[0, col - 1] is not None
    # clear the cell and press Enter to clear the data
    load_run_from_reduction_table(window_main, 0, col, "")
    qtbot.wait(wait)
    # check that the data has been cleared
    assert window_main.big_table_data[0, col - 1] is None
    assert window_main.ui.reductionTable.isEnabled()


@mock.patch("refred.main.DisplayPlots")
@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
def test_load_run_auto_peak_finder(mock_file_finder_find_runs, mock_display_plots, qtbot, file_finder_find_runs):
    """Test that the auto-peak finder is only enabled if a new run is loaded"""
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)

    run1 = "188300"
    run2 = "188301"
    expected_peak = [130, 141]
    expected_back = [127, 144]
    expected_tof_range_auto = [31420.7610, 44712.6203]

    # load the first run
    load_run_from_reduction_table(window_main, row=0, col=1, run=run1)
    qtbot.wait(wait)
    # check the result of the auto-peak finder
    assert window_main.big_table_data[0, 0].peak == expected_peak
    assert window_main.big_table_data[0, 0].back == expected_back
    assert window_main.big_table_data[0, 0].tof_range_auto == pytest.approx(expected_tof_range_auto, 1e-6)

    # modify the peak and background ranges (users can change these in the UI)
    user_set_peak = ["132", "143"]
    user_set_back = ["128", "147"]
    user_set_tof = [31500.0, 44700.0]
    window_main.big_table_data[0, 0].peak = user_set_peak
    window_main.big_table_data[0, 0].back = user_set_back
    window_main.big_table_data[0, 0].tof_range_auto = user_set_tof
    # reload the same run
    load_run_from_reduction_table(window_main, row=0, col=1, run=run1)
    qtbot.wait(wait)
    # check that the auto-peak finder did not change the peak and background ranges
    assert window_main.big_table_data[0, 0].peak == user_set_peak
    assert window_main.big_table_data[0, 0].back == user_set_back
    assert window_main.big_table_data[0, 0].tof_range_auto == pytest.approx(user_set_tof, 1e-6)

    # load a different run in the cell
    load_run_from_reduction_table(window_main, row=0, col=1, run=run2)
    qtbot.wait(wait)
    # check that the peak and background ranges were updated
    assert window_main.big_table_data[0, 0].peak == user_set_peak
    assert window_main.big_table_data[0, 0].back == user_set_back
    assert window_main.big_table_data[0, 0].tof_range_auto == pytest.approx(user_set_tof, 1e-6)


@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
def test_clear_row_when_both_data_and_norm_runs_cleared(mock_file_finder_find_runs, qtbot, file_finder_find_runs):
    """Test that the row is cleared when both the data run and the normalization run have been cleared"""
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)

    row = 0
    reflected_run = "188300"
    load_run_from_reduction_table(window_main, row=row, col=TableCol.DATA_RUN, run=reflected_run)
    qtbot.wait(wait)

    normalization_run = "188232"
    load_run_from_reduction_table(window_main, row=row, col=TableCol.NORM_RUN, run=normalization_run)
    qtbot.wait(wait)

    # clear the text in the data run and normalization run cells
    load_run_from_reduction_table(window_main, row=row, col=TableCol.DATA_RUN, run="")
    load_run_from_reduction_table(window_main, row=row, col=TableCol.NORM_RUN, run="")
    qtbot.wait(wait)

    # verify that the internal state has been cleared
    assert window_main.big_table_data.get_data_by_column_enum(row, TableDataColumIndex.LR_DATA) is None
    assert window_main.big_table_data.get_data_by_column_enum(row, TableDataColumIndex.LR_NORM) is None
    assert window_main.big_table_data.get_data_by_column_enum(row, TableDataColumIndex.LR_CONFIG) is None

    # verify that the GUI row has been cleared
    ui_table = window_main.ui.reductionTable
    _nbr_col = ui_table.columnCount()
    for col_index in range(_nbr_col):
        item = ui_table.item(row, col_index)
        if item:
            assert item.text() == ""


if __name__ == "__main__":
    pytest.main([__file__])
