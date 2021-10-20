# local imports
from RefRed.reduction.live_reduction_handler import LiveReductionHandler

# third party packages
import pytest


class TestLiveReductionHandler:
    def test_init(self):
        o_live_reduction = LiveReductionHandler(parent=None)

    def test_calculate_nbr_reduction_process(self):
        pass

    def test_cleanup(self):
        pass

    def test_export(self):
        pass

    def test_launch_reduction(self):
        pass

    def test_print_message(self):
        pass

    def test_recalculate(self):
        pass

    def test_remove_tmp_workspaces(self):
        pass

    def test_run(self):
        pass

    def test_save_reduced_for_ascii_loaded(self):
        pass

    def test_save_reduction(self):
        pass

    def test_save_stitching_plot_view(self):
        pass


if __name__ == '__main__':
    pytest.main([__file__])
