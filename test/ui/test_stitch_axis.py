import os
import pytest
from RefRed.main import MainGui
from qtpy import QtCore, QtWidgets


wait = 100


def test_stitch_plot(qtbot, data_server):
    """Test the axis adjustment in stitching plot"""
    # Create the main window.
    main = MainGui()
    qtbot.addWidget(main)
    main.show()  # Only for human inspection. This line should be commented once the test passes.

    # Load data via xml file
    xml_file = data_server.path_to("REF_L_188299_to_188301.xml")
    main.path_config = os.path.dirname(xml_file)

    def qfiledialog_handler():
        def handler():
            dialog = main.findChild(QtWidgets.QFileDialog)
            line_edit = dialog.findChild(QtWidgets.QLineEdit)
            qtbot.keyClicks(line_edit, os.path.basename(xml_file))
            qtbot.wait(wait)
            qtbot.keyClick(line_edit, QtCore.Qt.Key_Enter)

        QtCore.QTimer.singleShot(5 * wait, handler)  # wait for `lapse` time, then execute `handler`

    qfiledialog_handler()
    main.load_configuration()
    qtbot.wait(wait)

    # Run reduce
    main.run_reduction_button()
    qtbot.wait(wait)
    data_stitching_Tab = main.findChild(QtWidgets.QWidget, "data_stitching_Tab")
    qtbot.mouseClick(data_stitching_Tab, QtCore.Qt.LeftButton)
    qtbot.wait(wait)

    #
    stitch_plot = main.findChild(QtWidgets.QWidget, "data_stitching_plot")
    # mimic right click on the x-axis
    stitch_plot._singleClick(True, True, 0, 0)
    qtbot.wait(wait)
    popup = main.findChild(QtWidgets.QMainWindow, "ManualXAxisControl")
    # - adjust xmin
    xmin_line_edit = popup.findChild(QtWidgets.QLineEdit, "x_min_value")
    xmin_line_edit.setText("0.01")
    popup.x_min_event()
    qtbot.wait(wait)
    # - adjust xmax
    xmax_line_edit = popup.findChild(QtWidgets.QLineEdit, "x_max_value")
    xmax_line_edit.setText("0.03")
    popup.x_max_event()
    qtbot.wait(wait)
    # - toggle back to auto scale
    popup.x_auto_rescale_event()
    qtbot.wait(wait)
    popup.close()
    qtbot.wait(wait)
    # mimic right click on the y-axis
    stitch_plot._singleClick(True, False, 0, 0)
    qtbot.wait(wait)
    popup = main.findChild(QtWidgets.QMainWindow, "ManualYAxisControl")
    assert popup
    # - adjust ymin
    popup.ui.y_min_value.setText("0.3")
    popup.y_min_event()
    qtbot.wait(wait)
    # - adjust ymax
    popup.ui.y_max_value.setText("14.0")
    popup.y_max_event()
    qtbot.wait(wait)
    # - toggle back to auto scale
    popup.y_auto_rescale_event()
    qtbot.wait(wait)
    popup.close()
    qtbot.wait(wait)


if __name__ == '__main__':
    pytest.main([__file__])
