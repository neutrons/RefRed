# package imports
from RefRed.export import export_plot_ascii

# 3rd party imports
import pytest
import unittest.mock as mock

class TestExportPlotAscii:

    def setup_class(cls):
        epa = export_plot_ascii.ExportPlotAscii()
        print(f"Test setup for {cls}")

    def teardown_class(cls):
        print(f"Test tear down for {cls}")

    def test_export_yt(self):
        pass

    def test_export_ix(self):
        pass

    def test_export_it(self):
        pass

    def test_export_yi(self):
        pass


if __name__ == '__main__':
    pytest.main([__file__])
