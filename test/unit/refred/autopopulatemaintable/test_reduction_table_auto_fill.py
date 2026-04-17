from unittest import mock

import pytest

from refred.autopopulatemaintable.reduction_table_auto_fill import ReductionTableAutoFill
from refred.calculations.lr_data import LRData
from refred.gui_handling.data_norm_spinboxes import DataSpinbox, NormSpinbox
from refred.main import MainGui
from refred.reduction_table_handling.reduction_table_check_box import ReductionTableCheckBox

wait = 2000


def _run_manual_sequence_event(window_main, data_type, run_input):
    if data_type == "data":
        line_edit = window_main.ui.data_sequence_lineEdit
        event = window_main.data_sequence_event
    else:
        line_edit = window_main.ui.norm_sequence_lineEdit
        event = window_main.norm_sequence_event

    line_edit.setText(run_input)
    event()
    return line_edit


def _prepare_norm_loading(window_main):
    ReductionTableAutoFill(parent=window_main, list_of_run_from_input="188299", data_type_selected="data")


@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
def test_reduction_table_auto_fill_two_runs(mock_file_finder_find_runs, file_finder_find_runs, qtbot):
    """Test that the first run configuration is preserved when loading a second run"""
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)

    # load the first data run + normalization run and plot
    run_str_1 = "188299"
    norm_str_1 = "188231"
    ReductionTableAutoFill(parent=window_main, list_of_run_from_input=run_str_1, data_type_selected="data")
    ReductionTableAutoFill(parent=window_main, list_of_run_from_input=norm_str_1, data_type_selected="norm")
    ReductionTableCheckBox(parent=window_main, row_selected=0)

    # modify the background position for the data run and normalization run
    back_min, back_max = 120, 180
    DataSpinbox(parent=window_main, entry_type="back", value_min=back_min, value_max=back_max)
    NormSpinbox(parent=window_main, entry_type="back", value_min=back_min, value_max=back_max)

    # verify that the background position was updated
    run_data: LRData = window_main.big_table_data.reflectometry_data(0)
    assert run_data.run_number == run_str_1
    assert run_data.back == [back_min, back_max]
    norm_data: LRData = window_main.big_table_data.normalization_data(0)
    assert norm_data.run_number == norm_str_1
    assert norm_data.back == [back_min, back_max]

    # load the second run, which will bump the first run to the second row due to the sorting by lambda
    run_str_2 = "188300"
    ReductionTableAutoFill(parent=window_main, list_of_run_from_input=run_str_2, data_type_selected="data")
    window_main.norm_sequence_event()

    # verify that the background position of the first run (now in the second row in the table) is the same
    run_data = window_main.big_table_data.reflectometry_data(0)
    assert run_data.run_number == run_str_1
    assert run_data.back == [back_min, back_max]
    norm_data = window_main.big_table_data.normalization_data(0)
    assert norm_data.run_number == norm_str_1
    assert norm_data.back == [back_min, back_max]


@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
@pytest.mark.parametrize(
    ("data_type", "valid_run", "expected_message"),
    [
        ("data", "188299", "Cannot locate data run(s): 999999."),
        ("norm", "188231", "Cannot locate norm run(s): 999999."),
    ],
)
def test_manual_sequence_event_mixed_valid_invalid_runs(
    mock_file_finder_find_runs, data_type, valid_run, expected_message, file_finder_find_runs, qtbot
):
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)
    if data_type == "norm":
        _prepare_norm_loading(window_main)

    line_edit = _run_manual_sequence_event(window_main, data_type, f"{valid_run},999999")
    qtbot.wait(wait)

    if data_type == "data":
        loaded_data = window_main.big_table_data.reflectometry_data(0)
    else:
        loaded_data = window_main.big_table_data.normalization_data(0)
    assert loaded_data is not None
    assert loaded_data.run_number == valid_run
    assert line_edit.text() == expected_message
    assert "red" in line_edit.styleSheet()


@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
@pytest.mark.parametrize(
    ("data_type", "valid_run"),
    [
        ("data", "188299"),
        ("norm", "188231"),
    ],
)
def test_manual_sequence_event_all_valid_runs_clear_line_edit(
    mock_file_finder_find_runs, data_type, valid_run, file_finder_find_runs, qtbot
):
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)
    if data_type == "norm":
        _prepare_norm_loading(window_main)

    line_edit = _run_manual_sequence_event(window_main, data_type, valid_run)
    qtbot.wait(wait)

    assert line_edit.text() == ""
    assert line_edit.styleSheet() == ""


@mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
@pytest.mark.parametrize(
    ("data_type", "expected_message"),
    [
        ("data", "Cannot locate data run(s): 999999."),
        ("norm", "Cannot locate norm run(s): 999999."),
    ],
)
def test_manual_sequence_event_all_invalid_runs_show_error(
    mock_file_finder_find_runs, data_type, expected_message, file_finder_find_runs, qtbot
):
    mock_file_finder_find_runs.side_effect = file_finder_find_runs

    window_main = MainGui()
    qtbot.addWidget(window_main)
    if data_type == "norm":
        _prepare_norm_loading(window_main)

    line_edit = _run_manual_sequence_event(window_main, data_type, "999999")
    qtbot.wait(wait)

    if data_type == "data":
        loaded_data = window_main.big_table_data.reflectometry_data(0)
    else:
        loaded_data = window_main.big_table_data.normalization_data(0)
    assert loaded_data is None
    assert line_edit.text() == expected_message
    assert "red" in line_edit.styleSheet()
