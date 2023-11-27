from RefRed.main import MainGui

# third party packages
import pytest
from qtpy.QtCore import Qt
import unittest.mock as mock

wait = 200


class Event(object):
    val = None

    def __init__(self, val=None):
        self.val = val

    def key(self):
        return self.val


class MockLocateListRun(object):
    """Mock return value for LocateListRun"""

    list_run = []
    list_nexus_found = ['/SNS/REF_L/IPTS-26776/nexus/REF_L_184975.nxs.h5']
    list_run_found = [184975]
    list_run_not_found = []


@pytest.mark.parametrize("is_display_checked", [True, False])
@mock.patch(
    "RefRed.calculations.check_list_run_compatibility_thread.CheckListRunCompatibilityThread.updating_reductionTable_metadata"  # noqa E501
)
@mock.patch("RefRed.calculations.check_list_run_compatibility_thread.CheckListRunCompatibilityThread.loading_lr_data")
@mock.patch(
    "RefRed.calculations.check_list_run_compatibility_thread.CheckListRunCompatibilityThread.update_lconfigdataset"
)
@mock.patch("RefRed.calculations.check_list_run_compatibility_thread.AddListNexus")
@mock.patch("RefRed.main.ReductionTableCheckBox")
@mock.patch("RefRed.main.DisplayPlots")
@mock.patch("RefRed.reduction_table_handling.update_reduction_table.LocateListRun")
def test_update_reduction_table_thread(
    mock_locate_list_run,
    mock_display_plots,
    mock_reduction_table_checkbox,
    mock_add_list_nexus,
    mock_update_lconfigdataset,
    mock_loading_lr_data,
    mock_updating_reductionTable_metadata,
    is_display_checked,
    qtbot,
):
    """Test of the communication between the main thread and CheckListRunCompatibilityThread

    Note: This only tests the signalling between the main thread and the thread spawned by
    CheckListRunCompatibilityThread. The actual logic updating run data and plots is mocked.
    """
    mock_locate_list_run.return_value = MockLocateListRun()
    mock_add_list_nexus.return_value = mock.Mock(ws=True)

    window_main = MainGui()
    qtbot.addWidget(window_main)
    # set the display checkbox to the desired value
    window_main.ui.reductionTable.cellWidget(0, 0).setChecked(is_display_checked)
    # set a run number in the reduction table
    window_main.ui.reductionTable.setCurrentCell(0, 1)
    window_main.ui.reductionTable.currentItem().setText("184975")

    # press Enter in run number cell to trigger update_reduction_table
    window_main.ui.reductionTable.keyPressEvent(Event(Qt.Key_Return))
    qtbot.wait(wait)

    # check mocked functions in the spawned thread
    mock_update_lconfigdataset.assert_called_once()
    mock_loading_lr_data.assert_called_once()
    mock_updating_reductionTable_metadata.assert_called_once()

    # check that display plots is only called if the checkbox is checked
    if is_display_checked:
        mock_display_plots.assert_called_once()
    else:
        mock_display_plots.assert_not_called()

    # check that the reduction table was re-enabled after the thread returned
    assert window_main.ui.reductionTable.isEnabled()


@pytest.mark.parametrize("column", [1, 2])  # data run column, normalization run column
@mock.patch("RefRed.reduction_table_handling.update_reduction_table.LocateListRun")
def test_update_reduction_table_clear_cell(mock_locate_list_run, data_server, qtbot, column):
    """Test pressing Enter in empty cell in the reduction table"""
    mock_locate_list_run.return_value = MockLocateListRun()

    window_main = MainGui()
    qtbot.addWidget(window_main)

    # test pressing Enter in empty cell before any data has been loaded
    window_main.ui.reductionTable.setCurrentCell(0, column)
    window_main.ui.table_reduction_cell_enter_pressed()
    qtbot.wait(wait)
    # check that the reduction table was re-enabled after the function returned
    assert window_main.ui.reductionTable.isEnabled()

    # test first loading a run, then clearing the cell and pressing Enter to clear loaded data
    window_main.ui.reductionTable.setCurrentCell(0, column)
    window_main.ui.reductionTable.currentItem().setText("184975")
    window_main.ui.table_reduction_cell_enter_pressed()
    qtbot.wait(5000)
    # check that the data has been loaded
    assert window_main.big_table_data[0, column - 1] is not None
    # clear the cell and press Enter to clear the data
    window_main.ui.reductionTable.setCurrentCell(0, column)
    window_main.ui.reductionTable.currentItem().setText("")
    window_main.ui.table_reduction_cell_enter_pressed()
    qtbot.wait(wait)
    # check that the reduction table was re-enabled after the function returned
    assert window_main.ui.reductionTable.isEnabled()
    # check that the data has been cleared
    assert window_main.big_table_data[0, column - 1] is None
