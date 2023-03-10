# third party packages
import pytest

# standard packages
from pathlib import Path


def test_data_server(data_server):
    assert Path(data_server.path_to('easy_data_set.csv')).exists()


def test_main_gui(main_gui):
    main_gui()
    # checkbox = main_window.ui.reductionTable.cellWidget(0, 0)
    # assert checkbox.isChecked() is True


if __name__ == '__main__':
    pytest.main([__file__])
