from RefRed.main import MainGui
from qtpy import QtCore
import os
import pytest
from unittest import mock
import numpy as np

wait = 200


if os.environ.get("GITHUB_ACTIONS", False):  # run small set in GitHub actions
    test_cases = [
        {
            "conf": "REF_L_188299_to_188301_plus_norm_runs.xml",
            "ascii": "REF_L_188299_to_188301_plus_norm_runs.txt",
            "first reduced": "first_reduced_in_188299_188301_plus_norm_runs.txt",
            "stitch": "REFL_188299_to_188301_plus_norm_runs_auto_stitching.txt",
            "script": "REF_L_188299_to_188301_plus_norm_runs.py",
            "run set": [188299, 188300, 188301],
            "metadataRunNumber": "188299",
            "metadataProtonChargeValue": "1.06e+02",
            "metadataProtonChargeUnits": "mC",
            "metadataLambdaRequestedValue": "12.39",
            "metadataLambdaRequestedUnits": "A",
            "metadatathiValue": "-0.60",
            "metadatathiUnits": "degree",
            "metadatatthdValue": "-1.20",
            "metadatatthdUnits": "deg",
            "metadataS1WValue": "20.00",
            "metadataS2WValue": "20.00",
            "metadataS1HValue": "0.39",
            "metadataS2HValue.": "0.25",
        }
    ]
else:
    test_cases = [
        {
            "conf": "REF_L_188298_auto_template.xml",
            "ascii": "REFL_188298_reduced_data.txt",
            "first reduced": "first_reduced_in_188298_188304.txt",
            "stitch": "REFL_188298_reduced_data_auto_stitching.txt",
            "script": "REFL_188298_data_reduction_script.py",
            "run set": [188298, 188299, 188300, 188301, 188302, 188303, 188304],
            "metadataRunNumber": "188298",
            "metadataProtonChargeValue": "4.31e+02",
            "metadataProtonChargeUnits": "mC",
            "metadataLambdaRequestedValue": "15.00",
            "metadataLambdaRequestedUnits": "A",
            "metadatathiValue": "-0.60",
            "metadatathiUnits": "degree",
            "metadatatthdValue": "-1.20",
            "metadatatthdUnits": "deg",
            "metadataS1WValue": "20.00",
            "metadataS2WValue": "20.00",
            "metadataS1HValue": "0.39",
            "metadataS2HValue.": "0.25",
        }
    ]


@pytest.mark.parametrize("case", test_cases)
@mock.patch("qtpy.QtWidgets.QFileDialog")
def test_reduce_and_export_data(QFileDialog_mock, qtbot, tmp_path, data_server, case):
    # set mock return values for QFileDialog
    QFileDialog_mock().exec_.return_value = True
    QFileDialog_mock().selectedFiles.return_value = data_server.path_to(case["conf"])
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
    qtbot.mouseClick(window.ui.reductionTable.cellWidget(0, 0), QtCore.Qt.LeftButton, pos=QtCore.QPoint(10, 9))
    qtbot.wait(wait)

    # Metadata table
    for key, value in case.items():
        try:
            assert getattr(window.ui, key).text() == value
        except AttributeError:  # example, key=="conf"
            pass

    # Push Reduce button
    qtbot.mouseClick(window.ui.reduceButton, QtCore.Qt.LeftButton)
    qtbot.waitUntil(lambda: window.ui.statusbar.currentMessage() == "Done!")

    # check that we have moved to the "Data Stitching" tab
    assert window.ui.plotTab.currentIndex() == 1

    qtbot.wait(wait)

    # Export data and compare
    export_ascii(qtbot, window)

    # compare results to expected
    compare_results("output.txt", data_server.path_to(case["ascii"]), tmp_path)

    # Change from Absolute Normalization to Auto. Stitching.
    (tmp_path / "output.txt").unlink()
    qtbot.mouseClick(window.ui.auto_stitching_button, QtCore.Qt.LeftButton, pos=QtCore.QPoint(10, 9))
    qtbot.wait(wait)

    export_ascii(qtbot, window)

    # compare results to expected
    compare_results("output.txt", data_server.path_to(case["stitch"]), tmp_path)

    # export the reduction script
    (tmp_path / "output.txt").unlink()

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
    expected_script = open(data_server.path_to(case["script"])).readlines()

    for value, expected in zip(reduction_script, expected_script):
        if value.startswith('#') or value.startswith('reduction_pars'):
            continue
        assert value.strip() == expected.strip()


def compare_results(results_file, expected_results_file, tmp_path):
    print("Compare: %s %s" % (expected_results_file, results_file))
    results = open(tmp_path / results_file).readlines()
    expected_results = open(expected_results_file).readlines()

    for value, expected in zip(results, expected_results):
        if (
            value.startswith("# Reduction time")
            or value.startswith("# Mantid version")
            or "# Date" in value
            or "# Reduction"
        ):
            continue

        if value.startswith('# # 188'):
            value_arr = value.replace('#', '').strip().split()
            expected_arr = expected.replace('#', '').strip().split()
            for i in range(2):  # DataRun and NormRun
                assert value_arr[i] == expected_arr[i]
            np.testing.assert_allclose(np.array(value_arr[2:], dtype=float), np.array(expected_arr[2:], dtype=float))
        elif value.startswith('#'):
            assert value.strip() == expected.strip()
        else:
            np.testing.assert_allclose(np.array(value.split(), dtype=float), np.array(expected.split(), dtype=float))
    print("   -- passed")


def export_ascii(qtbot, window):
    # press "Export the plot into ASCII file"
    export_action = window.ui.data_stitching_plot.toolbar.actions()[9]
    export_button_widget = window.ui.data_stitching_plot.toolbar.widgetForAction(export_action)
    qtbot.mouseClick(export_button_widget, QtCore.Qt.LeftButton)
    qtbot.wait(wait)


if __name__ == '__main__':
    pytest.main([__file__])
