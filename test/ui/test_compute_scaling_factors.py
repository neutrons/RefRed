# package imports
from RefRed.main import MainGui

# third party imports
from qtpy import QtCore, QtWidgets
import pytest

# standard imports
import random
import os
import string


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
    def qfiledialog_handler(filename, lapse=500):
        def handler():
            dialog = sfc.findChild(QtWidgets.QFileDialog)
            line_edit = dialog.findChild(QtWidgets.QLineEdit)
            qtbot.keyClicks(line_edit, filename)
            qtbot.wait(200)
            qtbot.keyClick(line_edit, QtCore.Qt.Key_Enter)

        QtCore.QTimer.singleShot(lapse, handler)

    sfc._save_directory = "/tmp"  # force the location of saving directory
    # do not use mkstemp since we don't want to actually create an empty file. Creating an empty file
    # would result in the QFileDialog poping the question if we want to replace the file.
    file_name = ''.join([random.choice(string.ascii_letters) for i in range(10)]) + ".cfg"

    qfiledialog_handler(file_name, lapse=0.5 * SECOND)
    qtbot.mouseClick(sfc.sfFileNameBrowseButton, QtCore.Qt.LeftButton)
    with qtbot.waitSignal(sfc.sfFileNamePreview.textChanged, timeout=10 * SECOND):
        qtbot.mouseClick(sfc.generateSFfileButton, QtCore.Qt.LeftButton)

    # Compare the contents of the file preview and the actual saved file
    cfg_file = os.path.join(sfc._save_directory, file_name)
    cfg = sfc.sfFileNamePreview.toPlainText()
    contents = open(cfg_file, 'r').read()
    assert cfg == contents
    os.remove(cfg_file)

    #
    # Export Python Script
    #
    file_name = ''.join([random.choice(string.ascii_letters) for i in range(10)]) + ".py"
    qfiledialog_handler(file_name, lapse=0.5 * SECOND)
    qtbot.mouseClick(sfc.exportButton, QtCore.Qt.LeftButton)
    qtbot.wait(3 * SECOND)  # it takes time for the script exporter to complete

    # compare the contents of the script
    def to_compare(filename):
        r"""Load the script, retain only the call to LRScalingFactors, and drop the value of option ScalingFactorFile.
        This value depends on the path of the directory where the test is executed"""
        all = open(filename, "r").read().split('\n')[-1]
        return all.split('ScalingFactorFile')[0]

    cfg_file = os.path.join(sfc._save_directory, file_name)
    assert to_compare(cfg_file) == to_compare(data_server.path_to(script_file))
    os.remove(cfg_file)


if __name__ == '__main__':
    pytest.main([__file__])
