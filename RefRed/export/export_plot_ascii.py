import os
from typing import List, Tuple
from pathlib import Path
from qtpy import QtWidgets
import RefRed.utilities
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.utilities import makeSureFileHasExtension
from RefRed.reduction.reduced_data_handler import ReducedDataHandler

from lr_reduction import output as lr_output


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
        """
        Description
        -----------
        Return a default filename based on run number and data/plot type

        Parameters
        ----------
        run_number : int
            run number (IPTS run number)
        data_type : str
            data type, one of "yt", "ix", "it", "yi"

        Returns
        -------
        filename : str
        """
        basepath = Path(self.parent.path_ascii)
        suffix = self.default_suffix[datatype]
        filename = f"REFL_{run_number}_{suffix}.txt"
        return str(basepath / filename)

    def get_counts_vs_tof_datastr(self, active_data) -> List[str]:
        """
        Description
        -----------
        Generate a list of string used to export the it plot

        Parameters
        ----------
        active_data : Unknown
            active data object selected from the table by user

        Returns
        -------
        outstrlist : List[str]
        """
        countstof = active_data.countstofdata
        tof = active_data.tof_axis_auto_with_margin
        scale = 1000.0 if tof[-1] > 1000.0 else 1.0
        tof = tof / scale
        text = ["#Counts vs  TOF", "#TOF(ms) - Counts"]
        text += [f"{t} {c}" for t, c in zip(tof[:-1], countstof)]
        text.append(str(tof[-1]))
        return text

    def get_counts_vs_pixel_datastr(self, active_data) -> List[str]:
        """
        Description
        -----------
        Generate a list of string used to export the ix plot

        Parameters
        ----------
        active_data : Unknown
            active data object selected from the table by user

        Returns
        -------
        outstrlist : List[str]
        """
        countsx = active_data.countsxdata
        pixelaxis = list(range(len(countsx)))
        text = ["#Counts vs Pixels (low resolution range)", "#Pixel - Counts"]
        text += [f"{p} {c}" for p, c in zip(pixelaxis, countsx)]
        return text

    def get_ycounts_vs_pixel_datastr(self, active_data) -> List[str]:
        """
        Description
        -----------
        Generate a list of string used to export the yi plot

        Parameters
        ----------
        active_data : Unknown
            active data object selected from the table by user

        Returns
        -------
        outstrlist : List[str]
        """
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
    def get_save_filename(
        self,
        caption: str,
        default_filename: str,
    ) -> Tuple[str, str]:
        """wrapper around external getSaveFileName"""
        # NOTE:
        # current test framework cannot patch getSaveFileName, we have to shadow
        # it for testing purpose.
        return QtWidgets.QFileDialog.getSaveFileName(
            self.parent,
            caption,
            default_filename,
        )

    def export_stitched(self):
        """
        Pop up a dialog to ask the user where the save the output file,
        then proceed.
        """
        run_number = self.parent.ui.reductionTable.item(0, 1).text()
        default_filename = "REFL_%s_reduced_data.txt" % run_number
        path = Path(self.parent.path_ascii)
        default_filename = path / default_filename
        caption = "Select Location and Name"
        filter = "Reduced Ascii (*.txt);; All (*.*)"
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(
            self.parent,
            caption,
            str(default_filename),
            filter,
        )

        if filename.strip():
            # valid filename, save now
            folder = os.path.dirname(filename)
            if not os.access(folder, os.W_OK):
                self.ui.folder_error.setVisible(True)
                return

            self.filename = filename
            self.parent.path_ascii = os.path.dirname(filename)
            self.write_output_file(self.filename)

    def write_output_file(self, file_path):
        """
        Collect all the reduced data and create an output file.
        """
        # Gather data
        o_gui_utility = GuiUtility(parent=self.parent)
        nbr_row = o_gui_utility.reductionTable_nbr_row()
        o_reduced_data_hanlder = ReducedDataHandler(parent=self.parent)

        # Check wheter we want to export each individual run
        export_all = self.parent.ui.export_individual_checkbox.isChecked()
        _root, _ext = os.path.splitext(file_path)

        coll = lr_output.RunCollection()
        for row in range(nbr_row):
            _data = self.parent.big_table_data[row, 2]

            # Get the scaling factor, which may change in the UI
            sf = o_reduced_data_hanlder.generate_selected_sf(lconfig=_data)

            # Get the reduced data
            qz_mid = _data.reduce_q_axis
            refl = sf * _data.reduce_y_axis
            d_refl = sf * _data.reduce_e_axis

            _data.meta_data['scaling_factors']['a'] = sf * _data.meta_data['scaling_factors']['a']
            _data.meta_data['scaling_factors']['err_a'] = sf * _data.meta_data['scaling_factors']['err_a']
            _data.meta_data['scaling_factors']['b'] = sf * _data.meta_data['scaling_factors']['b']
            _data.meta_data['scaling_factors']['err_b'] = sf * _data.meta_data['scaling_factors']['err_b']

            npts = len(qz_mid)
            coll.add(qz_mid, refl, d_refl, meta_data=_data.meta_data)

            # At the user's request, save each individual run
            if export_all:
                run_file_path = "%s-%d%s" % (_root, row, _ext)
                coll_run = lr_output.RunCollection()
                coll_run.add(qz_mid, refl, d_refl, meta_data=_data.meta_data)
                coll_run.save_ascii(run_file_path)

        coll.save_ascii(file_path)

    def get_active_data(self):
        """Find the active/selected data from GUI"""
        o_gui_utility = GuiUtility(parent=self.parent)
        row = o_gui_utility.get_current_table_reduction_check_box_checked()
        col = o_gui_utility.get_data_norm_tab_selected()
        return self.parent.big_table_data[row, col]
