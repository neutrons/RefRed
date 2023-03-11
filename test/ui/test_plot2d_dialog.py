import os
import pytest
from RefRed.main import MainGui
from qtpy import QtCore, QtWidgets


wait = 100


def test_plot2d_dialog(qtbot, data_server):
    """Test the plot2d dialog."""
    # Create the main window
    window = MainGui()
    qtbot.addWidget(window)

    # window.show()  # Only for human inspection. This line should be commented once the test passes.

    # Load data
    xmlfilename = data_server.path_to("REF_L_188298_tiny_template.xml")
    window.path_config = os.path.dirname(xmlfilename)

    def qfiledialog_handler():
        def handler():
            dialog = window.findChild(QtWidgets.QFileDialog)
            line_edit = dialog.findChild(QtWidgets.QLineEdit)
            qtbot.keyClicks(line_edit, os.path.basename(xmlfilename))
            qtbot.wait(wait)
            qtbot.keyClick(line_edit, QtCore.Qt.Key_Enter)

        QtCore.QTimer.singleShot(5 * wait, handler)  # wait for `lapse` time, then execute `handler`

    qfiledialog_handler()
    window.load_configuration()
    qtbot.wait(wait)

    # Toggle the plot up
    window.reduction_table_visibility_changed_test(1, 0)
    qtbot.wait(wait)

    # Trigger the plot2d dialog
    # NOTE: somehow RefRed is not utilizing the built-in double
    #       click from Qt, so we need to trigger the single click
    #       twice within a short period
    window.single_click_data_yt_plot(True)
    qtbot.wait(0.1 * wait)
    window.single_click_data_yt_plot(True)
    qtbot.wait(wait)

    # Check the plot2d dialog has correct settings
    plot2d = window.findChild(QtWidgets.QDialog)
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
    plot2d.ui.peak1.setValue(130)
    plot2d.manual_input_peak1()
    plot2d.ui.peak2.setValue(140)
    plot2d.manual_input_peak2()
    # 4. background range
    plot2d.activate_or_not_back_widgets(True)
    plot2d.ui.back1.setValue(125)
    plot2d.manual_input_back1()
    plot2d.ui.back2.setValue(145)
    plot2d.manual_input_back2()
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


if __name__ == '__main__':
    pytest.main([__file__])
