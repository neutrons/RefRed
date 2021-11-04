from RefRed.main import MainGui
from qtpy import QtCore, QtWidgets
import os
from unittest import mock
import numpy as np

wait = 200


@mock.patch("qtpy.QtWidgets.QFileDialog")
def test_reduce_and_export_data(QFileDialog_mock, qtbot, tmp_path, data_server):
    # set mock return values for QFileDialog
    QFileDialog_mock().exec_.return_value = True
    QFileDialog_mock().selectedFiles.return_value = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                 "../data/REF_L_188298_auto_template.xml")
    QFileDialog_mock.getSaveFileName.return_value = (str(tmp_path / "output.txt"), "")
    QFileDialog_mock.getExistingDirectory.return_value = str(tmp_path)

    window = MainGui()
    qtbot.addWidget(window)
    window.show()

    # Open file menu, move down two and select Load
    action_rect = window.ui.menubar.actionGeometry(window.ui.menuFile.menuAction())
    qtbot.mouseClick(window.ui.menubar, QtCore.Qt.LeftButton, pos=action_rect.center())
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuFile, QtCore.Qt.Key_Enter)
    qtbot.waitUntil(lambda: window.ui.statusbar.currentMessage() == "Done!")
    qtbot.wait(wait)

    # Press button to plot first row of data
    qtbot.mouseClick(window.ui.reductionTable.cellWidget(0, 0),
                     QtCore.Qt.LeftButton,
                     pos=QtCore.QPoint(10, 9))
    qtbot.wait(wait)

    # Metadata table
    assert window.ui.metadataRunNumber.text() == "188298"
    assert window.ui.metadataProtonChargeValue.text() == "4.31e+02"
    assert window.ui.metadataProtonChargeUnits.text() == "mC"
    assert window.ui.metadataLambdaRequestedValue.text() == "15.00"
    assert window.ui.metadataLambdaRequestedUnits.text() == "A"
    assert window.ui.metadatathiValue.text() == "-0.60"
    assert window.ui.metadatathiUnits.text() == "degree"
    assert window.ui.metadatatthdValue.text() == "-1.20"
    assert window.ui.metadatatthdUnits.text() == "deg"
    assert window.ui.metadataS1WValue.text() == "20.00"
    assert window.ui.metadataS2WValue.text() == "20.00"
    assert window.ui.metadataS1HValue.text() == "0.39"
    assert window.ui.metadataS2HValue.text() == "0.25"

    # Push Reduce button

    qtbot.mouseClick(window.ui.reduceButton, QtCore.Qt.LeftButton)
    qtbot.waitUntil(lambda: window.ui.statusbar.currentMessage() == "Done!")

    # check that we have moved to the "Data Stitching" tab
    assert window.ui.plotTab.currentIndex() == 1

    qtbot.wait(wait)

    # Export data and compare
    export_ascii(qtbot, window)

    # compare results to expected
    compare_results("output.txt", "REFL_188298_reduced_data.txt", tmp_path)

    # Export data again but this time into multiple files
    export_ascii(qtbot, window, multiple=True)

    for run in range(188299, 188305):
        assert os.path.exists(tmp_path / f"REF_L_{run}_reduced_data.txt")

    # compare just the first file
    compare_results("REF_L_188298_reduced_data.txt", "REF_L_188298_reduced_data.txt", tmp_path)

    # Change from Absolute Normalization to Auto. Stitching.
    (tmp_path / "output.txt").unlink()
    qtbot.mouseClick(window.ui.auto_stitching_button, QtCore.Qt.LeftButton,
                     pos=QtCore.QPoint(10, 9))
    qtbot.wait(wait)

    export_ascii(qtbot, window)

    # compare results to expected
    compare_results("output.txt", "REFL_188298_reduced_data_auto_stitching.txt", tmp_path)

    # export the reduction script
    (tmp_path / "output.txt").unlink()
    # open reduction  menu, move down two and select
    action_rect = window.ui.menubar.actionGeometry(window.ui.menuReduction.menuAction())
    qtbot.mouseClick(window.ui.menubar, QtCore.Qt.LeftButton, pos=action_rect.center())
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuReduction, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuReduction, QtCore.Qt.Key_Down)
    qtbot.wait(wait)
    qtbot.keyClick(window.ui.menuReduction, QtCore.Qt.Key_Enter)
    qtbot.wait(wait)

    reduction_script = open(tmp_path / "output.txt").readlines()
    expected_script = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "../data/REFL_188298_data_reduction_script.py")).readlines()

    for value, expected in zip(reduction_script, expected_script):
        if value.startswith('#'):
            continue
        assert value.strip() == expected.strip()


def compare_results(results_file, expected_results_file, tmp_path):
    results = open(tmp_path / results_file).readlines()
    expected_results = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         f'../data/{expected_results_file}')).readlines()

    for value, expected in zip(results, expected_results):
        if value.startswith("# Reduction time") or value.startswith("# Mantid version") or "# Date" in value:
            continue

        if value.startswith('#'):
            assert value.strip() == expected.strip()
        else:
            np.testing.assert_allclose(np.array(value.split(), dtype=float),
                                       np.array(expected.split(), dtype=float))


def export_ascii(qtbot, window, multiple=False):
    # press "Export the plot into ASCII file"
    export_action = window.ui.data_stitching_plot.toolbar.actions()[9]
    export_button_widget = window.ui.data_stitching_plot.toolbar.widgetForAction(export_action)
    qtbot.mouseClick(export_button_widget, QtCore.Qt.LeftButton)
    qtbot.wait(wait)

    outputReducedDataDialog = window.findChildren(QtWidgets.QDialog)[-1]

    if multiple:
        # select 'n Ascii Files'
        qtbot.mouseClick(outputReducedDataDialog.ui.n_ascii_format, QtCore.Qt.LeftButton)
        qtbot.wait(wait)

    # press "Create Ascii File ..."
    qtbot.mouseClick(outputReducedDataDialog.ui.createAsciiButton, QtCore.Qt.LeftButton)
    qtbot.wait(wait)
