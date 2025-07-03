import functools

import pytest
from qtpy import QtCore, QtWidgets

from refred.main import MainGui

wait = 200


def test_startup(qtbot):
    pytest.importorskip("mantid")

    window = MainGui()
    qtbot.addWidget(window)
    window.show()
    assert window.windowTitle().startswith("Liquids Reflectometer Reduction -")
    assert window.ui.plotTab.tabText(0) == "Overview"
    assert window.ui.plotTab.tabText(1) == "Data Stitching"

    # This is the handle modal dialogs
    def handle_dialog_close(expected_title):
        # get a reference to the dialog and handle it here
        dialog = window.findChild(QtWidgets.QFileDialog)
        # Type in file to load and press enter
        qtbot.keyClick(dialog, QtCore.Qt.Key_Escape)
        assert dialog.windowTitle() == expected_title

    qtbot.wait(wait)

    # Metadata table
    assert window.ui.metadataRunNumber.text() == "N/A"
    assert window.ui.metadataProtonChargeValue.text() == "N/A"
    assert window.ui.metadataProtonChargeUnits.text() == "units"
    assert window.ui.metadataLambdaRequestedValue.text() == "N/A"
    assert window.ui.metadataLambdaRequestedUnits.text() == "units"
    assert window.ui.metadatathiValue.text() == "N/A"
    assert window.ui.metadatathiUnits.text() == "rad"
    assert window.ui.metadatatthdValue.text() == "N/A"
    assert window.ui.metadatatthdUnits.text() == "rad"
    assert window.ui.metadataS1WValue.text() == "N/A"
    assert window.ui.metadataS2WValue.text() == "N/A"
    assert window.ui.metadataS1HValue.text() == "N/A"
    assert window.ui.metadataS2HValue.text() == "N/A"

    # Open file menu, move down two and select Load, then just close the dialog
    action_rect = window.ui.menubar.actionGeometry(window.ui.menuFile.menuAction())
    qtbot.mouseClick(window.ui.menubar, QtCore.Qt.LeftButton, pos=action_rect.center())
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    QtCore.QTimer.singleShot(500, functools.partial(handle_dialog_close, "Open Configuration File"))
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Enter)
    qtbot.wait(wait)

    # Open and close SF Preview
    qtbot.mouseClick(window.ui.previewScalingFactorFile, QtCore.Qt.LeftButton)
    sf_preview_window = window.findChild(QtWidgets.QMainWindow)
    assert sf_preview_window.windowTitle() == "Scaling Factor File Preview"
    qtbot.wait(wait)
    assert sf_preview_window.close()

    # Change to Data\ Stitching tab
    assert window.ui.plotTab.currentIndex() == 0
    qtbot.wait(wait)

    window.ui.plotTab.setCurrentIndex(1)  # need to work out how to do this with qtbot
    qtbot.wait(wait)

    assert window.ui.plotTab.currentIndex() == 1

    # Open and close SF Calculator
    action_rect = window.ui.menubar.actionGeometry(window.ui.menuAdvanced.menuAction())
    qtbot.mouseClick(window.ui.menubar, QtCore.Qt.LeftButton, pos=action_rect.center())
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuAdvanced, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuAdvanced, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuAdvanced, QtCore.Qt.Key_Enter)
    qtbot.wait(wait)
    assert window.sf_calculator.windowTitle().startswith("SF Calculator - ")
    window.sf_calculator.close()
    qtbot.wait(wait)

    # Open About Dialog
    action_rect = window.ui.menubar.actionGeometry(window.ui.menuHelp.menuAction())
    qtbot.mouseClick(window.ui.menubar, QtCore.Qt.LeftButton, pos=action_rect.center())
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuHelp, QtCore.Qt.Key_Down)
    qtbot.wait(wait)

    def handle_message_box(expected_text):
        dialog = window.findChild(QtWidgets.QMessageBox)
        assert dialog.text().startswith(expected_text)
        qtbot.keyClick(dialog, QtCore.Qt.Key_Enter)

    QtCore.QTimer.singleShot(
        500, functools.partial(handle_message_box, "refred - Liquids Reflectrometry Reduction program")
    )
    qtbot.keyClick(window.ui.menuHelp, QtCore.Qt.Key_Enter)
