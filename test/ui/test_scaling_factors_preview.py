import os
from unittest.mock import patch as mock_patch

import pytest
from qtpy import QtCore

from RefRed.main import MainGui
from RefRed.sf_preview.sf_preview import SFPreview

SECOND = 1000  # 1000 miliseconds


def test_sf_preview(qtbot, data_server):
    window_main = MainGui()
    qtbot.addWidget(window_main)
    # Uncheck button "Use Scaling Factor Config."
    qtbot.mouseClick(window_main.ui.scalingFactorFlag, QtCore.Qt.LeftButton)
    assert window_main.ui.scalingFactorFlag.isChecked() is False
    assert window_main.ui.previewScalingFactorFile.isEnabled() is False  # Verify button "Preview ..." is disabled
    # re-enable the preview
    qtbot.mouseClick(window_main.ui.scalingFactorFlag, QtCore.Qt.LeftButton)
    assert window_main.ui.scalingFactorFlag.isChecked() is True
    assert window_main.ui.previewScalingFactorFile.isEnabled() is True  # Verify button "Preview ..." is disabled
    # Click in the "Browse.." button and load file sf_186529_Si_auto.cfg from the test/data directory

    file_name = "sf_186529_Si_auto.cfg"
    # this will set directory in the QFileDialog to the directory where file_name resides
    window_main.path_ascii = os.path.dirname(data_server.path_to(file_name))

    # mock entering the file the QFileDialog reading the scaling factors file
    def mock_open_file(*args, **kwargs):
        parent_dir = args[2]
        return os.path.join(parent_dir, "sf_186529_Si_auto.cfg"), ""

    with mock_patch(
        "RefRed.gui_handling.scaling_factor_widgets_handler.QFileDialog.getOpenFileName", new=mock_open_file
    ):
        qtbot.mouseClick(window_main.ui.sfBrowseButton, QtCore.Qt.LeftButton)  # open the QFileDialog

    assert window_main.ui.scalingFactorFile.text() == file_name
    assert window_main.ui.selectIncidentMediumList.currentText() == "Si"
    # open the preview widget
    qtbot.mouseClick(window_main.ui.previewScalingFactorFile, QtCore.Qt.LeftButton)
    sf_preview = window_main.findChild(SFPreview)
    qtbot.addWidget(sf_preview)  # qtbot will make sure to close this widget upon test completion
    assert sf_preview.ui.full_name_of_sf_file.text() == data_server.path_to(file_name)
    assert sf_preview.ui.table_widget.horizontalHeaderItem(4).data(0) == "S1W"
    assert sf_preview.ui.table_widget.item(4, 4).data(0) == "12.487"


if __name__ == "__main__":
    pytest.main([__file__])
