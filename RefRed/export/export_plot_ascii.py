import os
from typing import List
from pathlib import Path
import RefRed.utilities
from RefRed.export.output_reduced_data import OutputReducedData
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.utilities import makeSureFileHasExtension
from RefRed.widgets import getSaveFileName


class ExportPlotAscii:

    # NOTE:
    # figure layout as of 10-22-2021
    # ------------  main window ------------|
    # |     yt_plot      |     yi_plot      |
    # |------------------|------------------|
    # |     it_plot      |     ix_plot      |
    # |-------------------------------------|
    # |                table                |
    # |-------------------------------------|
    default_suffix = {
        "yt": "2dPxVsTof",
        "ix": "ix",
        "it": "yt",
        "yi": "rpx",
    }
    default_caption = {
        "yt": "Create 2D Pixel VS TOF",
        "ix": "Create Counts vs Pixel (low resolution range) ASCII File",
        "it": "Create Counts vs TOF ASCII File",
        "yi": "Create Counts vs Pixel ASCII File",
    }

    def __init__(self, parent, data_type: str = "yt"):
        self.parent = parent
        self.data_type = data_type

    def get_default_filename(self, run_number: int, datatype: str) -> str:
        """Return a default filename based on run number and data/plot type"""
        basepath = Path(self.parent.path_ascii)
        suffix = self.default_suffix[datatype]
        filename = f"REFL_{run_number}_{suffix}.txt"
        return str(basepath / filename)

    def get_counts_vs_tof_datastr(self, active_data) -> List[str]:
        """Generate a list of string used to export the it plot"""
        countstof = active_data.countstofdata
        tof = active_data.tof_axis_auto_with_margin
        scale = 1000.0 if tof[-1] > 1000.0 else 1.0
        tof = tof / scale
        text = ["#Counts vs  TOF", "#TOF(ms) - Counts"]
        text += [f"{t} {c}" for t, c in zip(tof[:-1], countstof)]
        text.append(str(tof[-1]))
        return text

    def get_counts_vs_pixel_datastr(self, active_data) -> List[str]:
        """Generate a list of string used to export the ix plot"""
        countsx = active_data.countsxdata
        pixelaxis = list(range(len(countsx)))
        text = ["#Counts vs Pixels (low resolution range)", "#Pixel - Counts"]
        text += [f"{p} {c}" for p, c in zip(pixelaxis, countsx)]
        return text

    def get_ycounts_vs_pixel_datastr(self, active_data) -> List[str]:
        """Generate a list of string used to export the yi plot"""
        ycounts = active_data.ycountsdata
        pixelaxis = list(range(len(ycounts)))
        text = ["#Counts vs Pixels", "#Pixel - Counts"]
        text += [f"{p} {c}" for p, c in zip(pixelaxis, ycounts)]
        return text

    # --------------- #
    # actual callback #
    # --------------- #
    def export(self):
        # sanity check
        if self.data_type == "stitched":
            self.export_stitched()  # out-source to external lib
        elif self.data_type in ("yt", "ix", "it", "yi"):
            # grab the active data
            active_data = self.get_active_data()
            # generate default filename for user
            default_filename = self.get_default_filename(
                active_data.run_number,
                self.data_type,
            )
            # ask user
            caption = self.default_caption[self.data_type]
            filename, _ = self.get_save_filename(caption, default_filename)
            # save data ONLY when filename is valid
            if filename.strip():
                # update cached dir
                self.parent.path_ascii = os.path.dirname(filename)
                # sanity check on extension
                filename = makeSureFileHasExtension(filename, default_ext=".txt")
                # get the data and save
                if self.data_type == "yt":
                    data_to_save = active_data.ytofdata
                    RefRed.utilities.output_2d_ascii_file(filename, data_to_save)
                else:
                    # get data string list
                    if self.data_type == "ix":
                        outstrlist = self.get_counts_vs_pixel_datastr(active_data)
                    elif self.data_type == "it":
                        outstrlist = self.get_counts_vs_tof_datastr(active_data)
                    elif self.data_type == "yi":
                        outstrlist = self.get_ycounts_vs_pixel_datastr(active_data)
                    # save to ASCII
                    RefRed.utilities.write_ascii_file(filename, outstrlist)
        else:
            raise ValueError(f"data type {self.data_type} not supported.")

    # -------------------------------------------------------------------- #
    # NOTE:                                                                #
    # this module cannot ensure that the following functions will always   #
    # behave exactly as they were intended due to the external dependency  #
    # nature.                                                              #
    # -------------------------------------------------------------------- #
    def get_save_filename(self, caption, default_filename):
        """wrapper around external getSaveFileName"""
        # NOTE:
        # current test framework cannot patch getSaveFileName, we have to shadow
        # it for testing purpose.
        return getSaveFileName(self.parent, caption, default_filename)

    def export_stitched(self):
        _tmp = OutputReducedData(parent=self.parent)
        _tmp.show()

    def get_active_data(self):
        """Find the active/selected data from GUI"""
        o_gui_utility = GuiUtility(parent=self.parent)
        row = o_gui_utility.get_current_table_reduction_check_box_checked()
        col = o_gui_utility.get_data_norm_tab_selected()
        return self.parent.big_table_data[row, col]
