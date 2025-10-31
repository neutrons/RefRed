from unittest import mock

from refred.main import MainGui
from refred.reduction.live_reduction_handler import LiveReductionHandler
from test.utilities import load_run_from_reduction_table


class TestLiveReductionHandler:
    @mock.patch("refred.calculations.locate_list_run.FileFinder.findRuns")
    def test_run(self, mock_file_finder_find_runs, qtbot, file_finder_find_runs):
        mock_file_finder_find_runs.side_effect = file_finder_find_runs

        main_window = MainGui()
        qtbot.addWidget(main_window)
        main_window.ui.useNormalizationFlag.setChecked(False)
        # load one run
        row = 0
        load_run_from_reduction_table(main_window, row=row, col=1, run="188300")
        qtbot.wait(2000)
        # run reduction
        handler = LiveReductionHandler(main_window)
        assert len(handler.big_table_data[row][2].reduce_q_axis) == 0
        assert len(handler.big_table_data[row][2].reduce_y_axis) == 0
        handler.run()
        assert len(handler.big_table_data[row][2].reduce_q_axis) == 72
        assert len(handler.big_table_data[row][2].reduce_y_axis) == 72
