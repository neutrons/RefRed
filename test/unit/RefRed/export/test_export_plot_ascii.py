# package imports
import RefRed
from RefRed.export import export_plot_ascii

# 3rd party imports
import pytest
import unittest.mock as mock
import tempfile
import numpy as np
from pathlib import Path


class TestExportPlotAscii:
    def setup_class(self):
        # make a fake parent
        self.fp = mock.Mock()
        self.fp.path_ascii = tempfile.gettempdir()
        # make fake active data
        self.fad = mock.Mock()
        self.fad.run_number = 1
        self.fad.countstofdata = np.array([1.0, 2.0])
        self.fad.tof_axis_auto_with_margin = np.array([1.0, 2.0, 3.0])
        self.fad.countsxdata = np.array([1.0, 2.0])
        self.fad.ycountsdata = np.array([1.0, 2.0])
        # instantiate the exporter
        self.epa = export_plot_ascii.ExportPlotAscii(parent=self.fp)

    def teardown_class(self):
        print(f"Test tear down for {self}")

    @pytest.mark.parametrize(
        "datatype,filename",
        [
            ("yt", "REFL_1_2dPxVsTof.txt"),
            ("ix", "REFL_1_ix.txt"),
            ("it", "REFL_1_yt.txt"),
            ("yi", "REFL_1_rpx.txt"),
        ],
    )
    def test_get_default_filename(self, datatype: str, filename: str):
        default_filename = self.epa.get_default_filename(1, datatype)
        assert default_filename == str(Path(tempfile.gettempdir()) / filename)

    def test_get_counts_vs_tof_datastr(self):
        outstrlist = self.epa.get_counts_vs_tof_datastr(self.fad)
        reference = [
            "#Counts vs  TOF",
            "#TOF(ms) - Counts",
            "1.0 1.0",
            "2.0 2.0",
            "3.0",
        ]
        for me, ne in zip(outstrlist, reference):
            assert me == ne

    def test_get_counts_vs_pixel_datastr(self):
        outstrlist = self.epa.get_counts_vs_pixel_datastr(self.fad)
        reference = [
            "#Counts vs Pixels (low resolution range)",
            "#Pixel - Counts",
            "0 1.0",
            "1 2.0",
        ]
        for me, ne in zip(outstrlist, reference):
            assert me == ne

    def test_get_ycounts_vs_pixel_datastr(self):
        outstrlist = self.epa.get_ycounts_vs_pixel_datastr(self.fad)
        reference = ["#Counts vs Pixels", "#Pixel - Counts", "0 1.0", "1 2.0"]
        for me, ne in zip(outstrlist, reference):
            assert me == ne

    @mock.patch("RefRed.utilities.write_ascii_file", mock.MagicMock())
    @mock.patch("RefRed.utilities.output_2d_ascii_file", mock.MagicMock())
    def test_export(self):
        # we need a new one as pytest might run out of order
        epa = export_plot_ascii.ExportPlotAscii(parent=self.fp)
        # overwrite external caller
        epa.get_save_filename = mock.MagicMock(return_value=("/tmp/t.txt", ""))
        epa.export_stitched = mock.MagicMock()
        epa.get_active_data = mock.MagicMock(return_value=self.fad)
        # overwrite tested func
        epa.get_default_filename = mock.MagicMock(return_value=("/tmp/t.txt", ""))
        epa.get_counts_vs_pixel_datastr = mock.MagicMock(return_value=[""])
        epa.get_counts_vs_tof_datastr = mock.MagicMock(return_value=[""])
        epa.get_ycounts_vs_pixel_datastr = mock.MagicMock(return_value=[""])

        # go through valid options
        for dt in ("yt", "ix", "it", "yi"):
            epa.data_type = dt
            epa.export()

        assert RefRed.utilities.output_2d_ascii_file.call_count == 1
        assert RefRed.utilities.write_ascii_file.call_count == 3


if __name__ == "__main__":
    pytest.main([__file__])
