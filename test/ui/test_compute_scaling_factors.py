import os
import random
import string
from unittest.mock import patch as mock_patch

import pytest
from qtpy import QtCore

from refred.main import MainGui

SECOND = 1000  # 1000 miliseconds


# The run-set "184975-184989" overflows the RAM of the GitHub Actions runners
test_cases = [("184977-184980", 4, "sf_export_script_184977_184980.py")]
if not os.environ.get("GITHUB_ACTIONS", False):
    test_cases.append(("184975-184989", 15, "sf_export_script_184975_184989.py"))


@pytest.mark.parametrize("run_set, run_count, script_file", test_cases)
def test_sf_calculator(qtbot, data_server, run_set, run_count, script_file):
    window_main = MainGui()
    qtbot.addWidget(window_main)
    window_main.launch_sf_calculator()
    sfc = window_main.sf_calculator
    qtbot.addWidget(sfc)
    #
    # Load the event files
    #
    q_rectangle = sfc.runSequenceLineEdit.geometry()
    qtbot.mouseClick(sfc.runSequenceLineEdit, QtCore.Qt.LeftButton, pos=q_rectangle.center())
    # enter run numbers
    qtbot.keyClicks(sfc.runSequenceLineEdit, run_set)
    qtbot.keyClick(sfc.runSequenceLineEdit, QtCore.Qt.Key_Enter)
    assert sfc.tableWidget.rowCount() == run_count

    #
    # Generate the structure factors
    #
    sfc._save_directory = "/tmp"  # force the location of saving directory
    file_name = "".join([random.choice(string.ascii_letters) for i in range(10)]) + ".cfg"
    with mock_patch("refred.sf_calculator.sf_calculator.QFileDialog.getSaveFileName") as mock_getSaveFileName:
        mock_getSaveFileName.return_value = os.path.join(sfc._save_directory, file_name), ""
        qtbot.mouseClick(sfc.sfFileNameBrowseButton, QtCore.Qt.LeftButton)

    with qtbot.waitSignal(sfc.sfFileNamePreview.textChanged, timeout=10 * SECOND):
        qtbot.mouseClick(sfc.generateSFfileButton, QtCore.Qt.LeftButton)

    qtbot.mouseClick(sfc.generateSFfileButton, QtCore.Qt.LeftButton)
    # Compare the contents of the file preview and the actual saved file
    cfg_file = os.path.join(sfc._save_directory, file_name)
    cfg = sfc.sfFileNamePreview.toPlainText()
    contents = open(cfg_file, "r").read()
    assert cfg == contents
    os.remove(cfg_file)

    #
    # Export Python Script
    #
    file_name = "".join([random.choice(string.ascii_letters) for i in range(10)]) + ".py"
    with mock_patch("refred.sf_calculator.reduction_sf_calculator.QFileDialog.getSaveFileName") as mock_getSaveFileName:
        mock_getSaveFileName.return_value = os.path.join(sfc._save_directory, file_name), ""
        qtbot.mouseClick(sfc.exportButton, QtCore.Qt.LeftButton)

    qtbot.wait(3 * SECOND)  # it takes time for the script exporter to complete

    # compare the contents of the script
    def to_compare(filename):
        # Load the script and compare lines that are not expected to change.
        content = "\n".join(open(filename, "r").read().split("\n")[8:16])
        return content

    cfg_file = os.path.join(sfc._save_directory, file_name)
    assert to_compare(cfg_file) == to_compare(data_server.path_to(script_file))
    os.remove(cfg_file)


if __name__ == "__main__":
    pytest.main([__file__])
