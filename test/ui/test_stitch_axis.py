import pytest
import numpy as np
from qtpy import QtCore, QtWidgets


wait = 100


def skipt_test_stitch_plot(qtbot, main_gui, data_server):
    """Test the axis adjustment in stitching plot"""
    main_window = main_gui(
        configuration=data_server.path_to("REF_L_188299_to_188301.xml"),
        show=True,
    )

    # Run reduce
    main_window.run_reduction_button()
    qtbot.wait(wait)
    data_stitching_Tab = main_window.findChild(QtWidgets.QWidget, "data_stitching_Tab")
    qtbot.mouseClick(data_stitching_Tab, QtCore.Qt.LeftButton)
    qtbot.wait(wait)

    #
    stitch_plot = main_window.findChild(QtWidgets.QWidget, "data_stitching_plot")
    ax = stitch_plot.canvas.ax
    # mimic right click on the x-axis
    stitch_plot._singleClick(True, True, 0, 0)
    qtbot.wait(wait)
    popup = main_window.findChild(QtWidgets.QMainWindow, "ManualXAxisControl")
    # - adjust xmin
    xmin_line_edit = popup.findChild(QtWidgets.QLineEdit, "x_min_value")
    xmin_line_edit.setText("0.01")
    popup.x_min_event()
    qtbot.wait(wait)
    np.testing.assert_equal(0.01, ax.get_xlim()[0])
    # - adjust xmax
    xmax_line_edit = popup.findChild(QtWidgets.QLineEdit, "x_max_value")
    xmax_line_edit.setText("0.03")
    popup.x_max_event()
    qtbot.wait(wait)
    np.testing.assert_equal(0.03, ax.get_xlim()[1])
    # - toggle back to auto scale
    popup.x_auto_rescale_event()
    qtbot.wait(wait)
    popup.close()
    qtbot.wait(wait)
    # mimic right click on the y-axis
    stitch_plot._singleClick(True, False, 0, 0)
    qtbot.wait(wait)
    popup = main_window.findChild(QtWidgets.QMainWindow, "ManualYAxisControl")
    assert popup
    # - adjust ymin
    popup.ui.y_min_value.setText("0.3")
    popup.y_min_event()
    qtbot.wait(wait)
    np.testing.assert_equal(0.3, ax.get_ylim()[0])
    # - adjust ymax
    popup.ui.y_max_value.setText("14.0")
    popup.y_max_event()
    qtbot.wait(wait)
    np.testing.assert_equal(14.0, ax.get_ylim()[1])
    # - toggle back to auto scale
    popup.y_auto_rescale_event()
    qtbot.wait(wait)
    popup.close()
    qtbot.wait(wait)


if __name__ == '__main__':
    pytest.main([__file__])
