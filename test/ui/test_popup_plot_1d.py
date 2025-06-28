from unittest.mock import patch as mock_patch

import pytest
from qtpy import QtCore

from refred.main import MainGui
from refred.plot.popup_plot_1d import PopupPlot1d


def test_popup_plot_1d(qtbot, data_server):
    window_main = MainGui()
    qtbot.addWidget(window_main)
    # window_main.show()  # Only for human inspection. This line should be commented once the test passes.

    def mock_file_dialog_opens(self):  # `self` is just one input argument, emphasizing we're mocking one class method
        r"""mock opening QFileDialog and selecting one file for reading"""
        return True

    def mock_file_dialog_returns(self):
        r"""mock returning the path to the file that's been opened for reading"""
        return data_server.path_to("REF_L_188299_configuration.xml")

    with mock_patch("refred.configuration.loading_configuration.QFileDialog.exec_", new=mock_file_dialog_opens):
        with mock_patch(
            "refred.configuration.loading_configuration.QFileDialog.selectedFiles", new=mock_file_dialog_returns
        ):
            window_main.load_configuration()  # load one data set, populates the first row in the reduction table

    window_main.reduction_table_visibility_changed_test(state=1, row=0)  # click the first row in reduction-table
    window_main.single_click_data_yi_plot(True)
    window_main.single_click_data_yi_plot(True)  # two single clicks emulate a double-click, instantiates a PopupPlot1d
    popup = PopupPlot1d._open_instances[-1]  # reference to the recently instantiated PopupPlot1d object
    figure = popup.ui.plot_counts_vs_pixel  # an instance of MPLWidget

    def pixel(boundary: str):
        r"""pixel coordinate for one of the vertical lines
        :boundary: the vertical line signaling peak or background boundary"""
        # dictionary translating the boundary to a Line2D index
        index = {
            "peak left boundary": 1,
            "peak right boundary": 2,
            "background left boundary": 3,
            "background right boundary": 4,
        }
        return figure.canvas.ax.lines[index[boundary]].get_data()[0][0]

    def assert_boundary(boundary, spinbox, value, old_value=None):
        r"""Check that the vertical line drawn in the matplotlib widget is actualized with
        the value passed on
        :boundary str: the vertical line signaling peak or background boundary
        :spinbox QSpingBox: the spin box widget controling the position of the vertical line
        :value int: the new pixel coordinate for the vertical line
        :old_value int: the current pixel coordinate for the vertical line
        """
        if old_value:
            assert pixel(boundary) == pytest.approx(old_value)
        spinbox.setValue(value)
        # Clicking "Enter" causes QSpinBox.editingFinished() signal to be emitted,
        # which in turn causes the associated vertical line to change pixel coordinate
        qtbot.keyClick(spinbox, QtCore.Qt.Key_Enter)
        assert pixel(boundary) == pytest.approx(value)

    # test changing the peak boundaries
    assert_boundary("peak left boundary", popup.ui.plotPeakFromSpinBox, 130, old_value=129)
    assert_boundary("peak right boundary", popup.ui.plotPeakToSpinBox, 142, old_value=141)

    # test changing the background boundaries
    assert_boundary("background left boundary", popup.ui.plotBackFromSpinBox, 127, old_value=126)
    assert_boundary("background right boundary", popup.ui.plotBackToSpinBox, 145, old_value=144)


if __name__ == "__main__":
    pytest.main([__file__])
