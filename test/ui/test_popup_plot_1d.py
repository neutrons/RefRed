# package imports
from RefRed.plot.popup_plot_1d import PopupPlot1d

# third party imports
import pytest
from qtpy import QtCore


def skip_test_popup_plot_1d(qtbot, main_gui):
    window_main = main_gui(show=True)

    # Using qtbot.mouseClick twice to emulate a double bring is not instantiating up the popup
    # q_rectangle = yi_plot.contentsRect()
    # qtbot.mouseClick(yi_plot, QtCore.Qt.LeftButton, pos=q_rectangle.center())
    # qtbot.mouseClick(yi_plot, QtCore.Qt.LeftButton, pos=q_rectangle.center())

    # resort to manually invoking the callback
    window_main.single_click_data_yi_plot(True)
    window_main.single_click_data_yi_plot(True)  # two single clicks emulating a double-click
    popup = window_main.findChild(PopupPlot1d)
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
    assert_boundary("peak left boundary", popup.ui.plot_peak1, 130, old_value=129)
    assert_boundary("peak right boundary", popup.ui.plot_peak2, 142, old_value=141)

    # test changing the background boundaries
    assert_boundary("background left boundary", popup.ui.plot_back1, 127, old_value=126)
    assert_boundary("background right boundary", popup.ui.plot_back2, 145, old_value=144)

    # disable/enable background options. Assumed popup.ui.plot_back_flag is initially checked
    for status in [False, True]:
        qtbot.mouseClick(popup.ui.plot_back_flag, QtCore.Qt.LeftButton)
        assert popup.ui.plot_back1.isEnabled() is status
        assert popup.ui.plot_back2.isEnabled() is status


if __name__ == '__main__':
    pytest.main([__file__])
