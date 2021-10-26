# local imports
from RefRed.main import MainGui

# third party packages
import pytest


class TestMainGui:
    def test_init(self, qtbot):
        window_main = MainGui()
        qtbot.addWidget(window_main)
        assert "Liquids Reflectometer Reduction" in window_main.windowTitle()

    def test_run_reduction_button(self, qtbot):
        window_main = MainGui()
        qtbot.addWidget(window_main)
        assert window_main.run_reduction_button() is None


if __name__ == '__main__':
    pytest.main([__file__])
