import pytest

# third party packages
from qtpy.QtCore import Qt
import unittest.mock as mock

from RefRed.main import MainGui
from RefRed.reduction_table_handling.update_reduction_table import UpdateReductionTable

wait = 5000


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


@mock.patch(
    "RefRed.calculations.check_list_run_compatibility_thread.CheckListRunCompatibilityThread.updating_reductionTable_metadata")
@mock.patch("RefRed.calculations.check_list_run_compatibility_thread.CheckListRunCompatibilityThread.loading_lr_data")
@mock.patch(
    "RefRed.calculations.check_list_run_compatibility_thread.CheckListRunCompatibilityThread.update_lconfigdataset")
@mock.patch("RefRed.calculations.check_list_run_compatibility_thread.AddListNexus")
@mock.patch("RefRed.reduction_table_handling.update_reduction_table.DisplayPlots")
@mock.patch("RefRed.reduction_table_handling.update_reduction_table.LocateListRun")
def test_update_reduction_table_thread(mock_locate_list_run, mock_display_plots, mock_add_list_nexus,
                                       mock_update_lconfigdataset, mock_loading_lr_data,
                                       mock_updating_reductionTable_metadata, qtbot):
    """Test of the signalling between the main thread and CheckListRunCompatibilityThread"""
    mock_locate_list_run.return_value = MockLocateListRun()
    mock_add_list_nexus.return_value = mock.Mock(ws=True)

    window_main = MainGui()
    qtbot.addWidget(window_main)
    window_main.ui.reductionTable.setCurrentCell(0, 1)
    window_main.ui.reductionTable.currentItem().setText("184975")

    # press Enter in run number cell to trigger update_reduction_table
    window_main.ui.reductionTable.keyPressEvent(Event(Qt.Key_Return))
    qtbot.wait(wait)

    # check mocked functions in the spawned thread
    mock_update_lconfigdataset.assert_called_once()
    mock_loading_lr_data.assert_called_once()
    mock_updating_reductionTable_metadata.assert_called_once()

    # check mocked function in the main thread
    mock_display_plots.assert_called_once()

    # check that the reduction table was re-enabled after the thread returned
    assert window_main.ui.reductionTable.isEnabled()
