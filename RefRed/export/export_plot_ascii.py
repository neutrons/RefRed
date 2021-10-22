import os
from pathlib import Path
from typing import List
import RefRed.utilities
from RefRed.export.output_reduced_data import OutputReducedData
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.utilities import makeSureFileHasExtension
from RefRed.widgets import getSaveFileName


class ExportPlotAscii:

    parent = None
    data_type = "yt"

    def __init__(self, parent=None, data_type: str = "yt"):
        self.parent = parent
        self.data_type = data_type

    def export(self):
        _data_type = self.data_type
        if _data_type == "yt":
            self.export_yt()
        elif _data_type == "ix":
            self.export_ix()
        elif _data_type == "it":
            self.export_it()
        elif _data_type == "yi":
            self.export_yi()
        elif _data_type == "stitched":
            self.export_stitched()
        else:
            raise ValueError(f"data type {_data_type} not supported.")

    def export_yt(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row, col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        default_filename = f"REFL_{_data.run_number}_2dPxVsTof.txt"
        path = Path(parent.path_ascii)
        default_filename = path / default_filename
        caption = "Create 2D Pixel VS TOF"
        filename, _ = getSaveFileName(parent, caption, str(default_filename))

        if filename.strip():
            # valid filename, save the data
            parent.path_ascii = os.path.dirname(filename)
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            image = _data.ytofdata
            RefRed.utilities.output_2d_ascii_file(filename, image)

    def export_ix(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row, col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        default_filename = f"REFL_{_data.run_number}_ix.txt"
        path = Path(parent.path_ascii)
        default_filename = path / default_filename
        caption = "Create Counts vs Pixel (low resolution range) ASCII File"
        filename, _ = getSaveFileName(parent, caption, str(default_filename))

        if filename.strip():
            # filename valid, save the data
            parent.path_ascii = os.path.dirname(filename)
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            countsxdata = _data.countsxdata
            pixelaxis = list(range(len(countsxdata)))

            text = ["#Counts vs Pixels (low resolution range)", "#Pixel - Counts"]
            text += [f"{p} {c}" for p, c in zip(pixelaxis, countsxdata)]

            RefRed.utilities.write_ascii_file(filename, text)

    def export_it(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row, col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        default_filename = f"REFL_{_data.run_number}_yt.txt"
        path = Path(parent.path_ascii)
        default_filename = path / default_filename
        caption = "Create Counts vs TOF ASCII File"
        filename, _ = getSaveFileName(parent, caption, str(default_filename))

        if filename.strip():
            # valid filename, save now
            parent.path_ascii = os.path.dirname(filename)
            countstofdata = _data.countstofdata
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            tof = _data.tof_axis_auto_with_margin
            if tof[-1] > 1000:
                tof /= 1000.0

            text = ["#Counts vs  TOF", "#TOF(ms) - Counts"]
            text += [f"{t} {c}" for t, c in zip(tof[:-1], countstofdata)]
            text.append(str(tof[-1]))
            RefRed.utilities.write_ascii_file(filename, text)

    def export_yi(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row, col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        default_filename = f"REFL_{_data.run_number}_rpx.txt"
        path = Path(parent.path_ascii)
        default_filename = path / default_filename
        caption = "Create Counts vs Pixel ASCII File"
        filename, _ = getSaveFileName(parent, caption, str(default_filename))

        if filename.strip():
            # valid filename, save now
            parent.path_ascii = os.path.dirname(filename)
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            ycountsdata = _data.ycountsdata
            pixelaxis = list(range(len(ycountsdata)))

            text = ["#Counts vs Pixels", "#Pixel - Counts"]
            text += [f"{p} {c}" for p, c in zip(pixelaxis, ycountsdata)]

            RefRed.utilities.write_ascii_file(filename, text)

    def export_stitched(self):
        _tmp = OutputReducedData(parent=self.parent)
        _tmp.show()

    def get_current_row_col_displayed(self) -> List[int]:
        o_gui_utility = GuiUtility(parent=self.parent)
        row = o_gui_utility.get_current_table_reduction_check_box_checked()
        col = o_gui_utility.get_data_norm_tab_selected()
        return [row, col]
