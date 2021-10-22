import os
from pathlib import Path
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

    def get_default_filename(self, run_number: int, datatype: str) -> str:
        """Return a default filename based on run number and data/plot type"""
        # NOTE:
        # figure layout as of 10-22-2021
        # ------------  main window ------------|
        # |     yt_plot      |     yi_plot      |
        # |------------------|------------------|
        # |     it_plot      |     ix_plot      |
        # |-------------------------------------|
        # |                table                |
        # |-------------------------------------|
        basepath = Path(self.parent.path_ascii)
        suffix = {
            "yt": "2dPxVsTof",
            "ix": "ix",
            "it": "yt",
            "yi": "rpx",
        }[datatype]
        filename = f"REFL_{run_number}_{suffix}.txt"
        return str(basepath / filename)

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
        # grab the active data
        active_data = self.get_active_data()
        # generate default filename for user
        default_filename = self.get_default_filename(
            active_data.run_number,
            self.data_type,
        )
        # ask user
        caption = "Create 2D Pixel VS TOF"
        filename, _ = getSaveFileName(self.parent, caption, default_filename)
        # save data ONLY when filename is valid
        if filename.strip():
            # update cached dir
            self.parent.path_ascii = os.path.dirname(filename)
            # sanity check on extension
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            # get data to save
            data_to_save = active_data.ytofdata
            # save to file
            RefRed.utilities.output_2d_ascii_file(filename, data_to_save)

    def export_ix(self):
        # grab the activate data
        active_data = self.get_active_data()
        # generate the default filename for user
        default_filename = self.get_default_filename(
            active_data.run_number,
            self.data_type,
        )
        # ask user input
        caption = "Create Counts vs Pixel (low resolution range) ASCII File"
        filename, _ = getSaveFileName(self.parent, caption, default_filename)
        # save ONLY when given filename is valid
        if filename.strip():
            # update parent cached dir
            self.parent.path_ascii = os.path.dirname(filename)
            # sanitizing filename extension
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            # get data/str to save
            countsx = active_data.countsxdata
            pixelaxis = list(range(len(countsx)))
            text = ["#Counts vs Pixels (low resolution range)", "#Pixel - Counts"]
            text += [f"{p} {c}" for p, c in zip(pixelaxis, countsx)]
            # save to file
            RefRed.utilities.write_ascii_file(filename, text)

    def export_it(self):
        # grab the active data
        active_data = self.get_active_data()
        # generate the default filename for user
        default_filename = self.get_default_filename(
            active_data.run_number,
            self.data_type,
        )
        # ask user for input
        caption = "Create Counts vs TOF ASCII File"
        filename, _ = getSaveFileName(self.parent, caption, default_filename)
        # save ONLY when given filename is valid
        if filename.strip():
            # update parent cached dir
            self.parent.path_ascii = os.path.dirname(filename)
            # sanitizing filename extension
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            # get data/str to save
            countstof = active_data.countstofdata
            tof = active_data.tof_axis_auto_with_margin
            scale = 1000.0 if tof[-1] > 1000 else 1.0
            tof /= scale
            text = ["#Counts vs  TOF", "#TOF(ms) - Counts"]
            text += [f"{t} {c}" for t, c in zip(tof[:-1], countstof)]
            text.append(str(tof[-1]))
            # save to file
            RefRed.utilities.write_ascii_file(filename, text)

    def export_yi(self):
        # grab the active data
        active_data = self.get_active_data()
        # generate the default filename for user
        default_filename = self.get_default_filename(
            active_data.run_number,
            self.data_type,
        )
        # ask user for input
        caption = "Create Counts vs Pixel ASCII File"
        filename, _ = getSaveFileName(self.parent, caption, default_filename)
        # save ONLY when given filename is valid
        if filename.strip():
            # update parent cached dir
            self.parent.path_ascii = os.path.dirname(filename)
            # sanitizing filename extension
            filename = makeSureFileHasExtension(filename, default_ext=".txt")
            # get data/str to save
            ycounts = active_data.ycountsdata
            pixelaxis = list(range(len(ycounts)))
            text = ["#Counts vs Pixels", "#Pixel - Counts"]
            text += [f"{p} {c}" for p, c in zip(pixelaxis, ycounts)]
            # save to file
            RefRed.utilities.write_ascii_file(filename, text)

    # -------------------------------------------------------------------- #
    # NOTE:                                                                #
    # this module cannot ensure that the following functions will always   #
    # behave exactly as they were intended due to the external dependency  #
    # nature.                                                              #
    # -------------------------------------------------------------------- #
    def export_stitched(self):
        _tmp = OutputReducedData(parent=self.parent)
        _tmp.show()

    def get_active_data(self):
        """Find the active/selected data from GUI"""
        o_gui_utility = GuiUtility(parent=self.parent)
        row = o_gui_utility.get_current_table_reduction_check_box_checked()
        col = o_gui_utility.get_data_norm_tab_selected()
        return self.parent.big_table_data[row, col]
