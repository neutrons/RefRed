from unittest.mock import patch as mock_patch

import pytest
from qtpy import QtCore, QtWidgets

from refred.main import MainGui
from refred.plot.popup_plot_2d import PopupPlot2d

wait = 100


def test_plot2d_dialog(qtbot, data_server):
    """Test the plot2d dialog."""
    # Create the main window
    window_main = MainGui()
    qtbot.addWidget(window_main)
    # window.show()  # Only for human inspection. This line should be commented once the test passes.

    def mock_file_dialog_opens(self):  # `self` is just one input argument, emphasizing we're mocking one class method
        r"""mock opening QFileDialog and selecting one file for reading"""
        return True

    def mock_file_dialog_returns(self):
        r"""mock returning the path to the file that's been opened for reading"""
        return data_server.path_to("REF_L_188298_tiny_template.xml")

    with mock_patch("refred.configuration.loading_configuration.QFileDialog.exec_", new=mock_file_dialog_opens):
        with mock_patch(
            "refred.configuration.loading_configuration.QFileDialog.selectedFiles", new=mock_file_dialog_returns
        ):
            window_main.load_configuration()  # load one data set, populates the first row in the reduction table

    # Toggle the plot up
    window_main.reduction_table_visibility_changed_test(state=1, row=0)

    # Trigger the plot2d dialog
    # NOTE: somehow refred is not utilizing the built-in double
    #       click from Qt, so we need to trigger the single click
    #       twice within a short period
    window_main.single_click_data_yt_plot(True)
    window_main.single_click_data_yt_plot(True)  # two single clicks emulate a double-click, instantiates a PopupPlot2d

    # Check the plot2d dialog has correct settings
    plot2d = PopupPlot2d._open_instances[-1]  # reference to the recently instantiated PopupPlot2d object
    assert plot2d
    assert plot2d.data_type == "data"
    # --------- pixel_vs_tof_tab ---------- #
    # 1. switch to manual
    manual_button = plot2d.findChild(QtWidgets.QRadioButton, "tof_manual_flag")
    qtbot.mouseClick(manual_button, QtCore.Qt.LeftButton)
    # 2. tof range
    tof_from = plot2d.findChild(QtWidgets.QLineEdit, "tof_from")
    assert tof_from
    tof_from.setText("41")
    tof_to = plot2d.findChild(QtWidgets.QLineEdit, "tof_to")
    assert tof_to
    tof_to.setText("55")
    plot2d.manual_input_of_tof_field()
    # 3. peak range
    plot2d.ui.plot2dPeakFromSpinBox.setValue(130)
    plot2d.manual_input_peak1()
    plot2d.ui.plot2dPeakToSpinBox.setValue(140)
    plot2d.manual_input_peak2()
    # 4. background range
    plot2d.activate_or_not_back_widgets()
    plot2d.ui.plot2dBackFromValue.setValue(125)
    plot2d.manual_input_background()
    plot2d.ui.plot2dBackToValue.setValue(145)
    plot2d.manual_input_background()
    plot2d.update_plots()
    qtbot.wait(wait)
    # 5. back to auto
    auto_button = plot2d.findChild(QtWidgets.QRadioButton, "tof_auto_flag")
    qtbot.mouseClick(auto_button, QtCore.Qt.LeftButton)
    qtbot.wait(wait)
    # --------- detector_tab --------- #
    det_tab = plot2d.findChild(QtWidgets.QWidget, "tab_2")
    qtbot.mouseClick(det_tab, QtCore.Qt.LeftButton)
    plot2d.update_detector_tab_plot()
    qtbot.wait(wait)
    # switch back
    plt_tab = plot2d.findChild(QtWidgets.QWidget, "tab")
    qtbot.mouseClick(plt_tab, QtCore.Qt.LeftButton)
    qtbot.wait(wait)


if __name__ == "__main__":
    pytest.main([__file__])
