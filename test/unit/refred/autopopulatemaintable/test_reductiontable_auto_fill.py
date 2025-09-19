from unittest import mock

from refred.autopopulatemaintable.reductiontable_auto_fill import ReductionTableAutoFill
from refred.calculations.lr_data import LRData
from refred.gui_handling.data_norm_spinboxes import DataSpinbox
from refred.main import MainGui
from refred.reduction_table_handling.reduction_table_check_box import ReductionTableCheckBox


@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
def test_reduction_table_auto_fill_two_runs(mock_file_finder_find_runs, file_finder_find_runs, qtbot):
    """Test that the first run configuration is preserved when loading a second run"""
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)

    # load the first run and plot it
    run_str_1 = "188300"
    ReductionTableAutoFill(parent=window_main, list_of_run_from_input=run_str_1, data_type_selected="data")
    ReductionTableCheckBox(parent=window_main, row_selected=0)

    # modify the background position
    back_min, back_max = 120, 180
    DataSpinbox(parent=window_main, entry_type="back", value_min=back_min, value_max=back_max)

    # verify that the background position was updated
    run_data: LRData = window_main.big_table_data.reflectometry_data(0)
    assert run_data.run_number == run_str_1
    assert run_data.back == [back_min, back_max]

    # load the second run, which will bump the first run to the second row due to the sorting by lambda
    run_str_2 = "188299"
    ReductionTableAutoFill(parent=window_main, list_of_run_from_input=run_str_2, data_type_selected="data")

    # verify that the background position of the first run (now in the second row in the table) is the same
    run_data: LRData = window_main.big_table_data.reflectometry_data(1)
    assert run_data.run_number == run_str_1
    assert run_data.back == [back_min, back_max]
