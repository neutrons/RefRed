from RefRed.main import MainGui
from qtpy import QtCore, QtWidgets

# import functools
# import pytest

wait = 200


def test_plot2d_dialog(qtbot, data_server):
    """Test the plot2d dialog."""
    # Create the main window
    window = MainGui()
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(wait)

    # Load the data
    xmlfilename = data_server.path_to("REF_L_188298_tiny_template.xml")
    action_rect = window.ui.menubar.actionGeometry(window.ui.menuFile.menuAction())
    qtbot.mouseClick(window.ui.menubar, QtCore.Qt.LeftButton, pos=action_rect.center())
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Enter)
    qtbot.wait(wait)
    # def handler():
    dialog = window.ui.findChild(QtWidgets.QFileDialog)
    qtbot.wait(wait)
    print(dialog)
    line_edit = dialog.findChild(QtWidgets.QLineEdit)
    qtbot.keyClicks(line_edit, xmlfilename)
    qtbot.wait(wait)
    qtbot.keyClick(line_edit, QtCore.Qt.Key_Enter)
    # QtCore.QTimer.singleShot(wait*3, handler)

    # Trigger the plot2d dialog

    # Check the plot2d dialog has correct settings

    # Click a few buttons

    # Done
