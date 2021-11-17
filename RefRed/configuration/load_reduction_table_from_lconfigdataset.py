from qtpy import QtGui, QtWidgets
from RefRed.calculations.add_list_nexus import AddListNexus
from RefRed.calculations.lr_data import LRData
from RefRed.calculations.locate_list_run import LocateListRun
from RefRed.calculations.update_reduction_table_metadata import UpdateReductionTableMetadata
from RefRed.gui_handling.progressbar_handler import ProgressBarHandler
from RefRed.plot.display_plots import DisplayPlots
from RefRed.gui_handling.gui_utility import GuiUtility
import RefRed.colors


class LoadReductionTableFromLConfigDataSet(object):

    parent = None

    def __init__(self, parent=None):
        self.parent = parent

        nbr_lconfig = self.get_nbr_lconfig()
        big_table_data = self.parent.big_table_data
        o_load_config_progressbar_handler = ProgressBarHandler(parent=parent)
        o_load_config_progressbar_handler.setup(nbr_reduction=nbr_lconfig, label='Loading Config.')

        for index_row, lconfig in enumerate(big_table_data[:, 2]):
            if lconfig is None:
                o_load_config_progressbar_handler.end()
                break

            list_data_run = lconfig.data_sets
            o_list_data_nexus = LocateListRun(list_run=list_data_run)
            list_data_nexus = o_list_data_nexus.list_nexus_found
            #            list_data_nexus= o_list_data_nexus.list_run_found
            _add_data_nexus = AddListNexus(
                list_nexus=list_data_nexus,
                list_run=list_data_run,
                metadata_only=False,
                check_nexus_compatibility=False,
                prefix='data',
            )
            data_lrdata = LRData(_add_data_nexus.wks, lconfig=lconfig, is_data=True, parent=self.parent)
            self.update_lrdata(lrdata=data_lrdata, lconfig=lconfig, type='data', row=index_row)

            list_norm_run = lconfig.norm_sets
            o_list_norm_nexus = LocateListRun(list_run=list_norm_run)
            list_norm_nexus = o_list_norm_nexus.list_nexus_found
            if list_norm_nexus != []:
                _add_norm_nexus = AddListNexus(
                    list_nexus=list_norm_nexus,
                    list_run=list_norm_run,
                    metadata_only=False,
                    check_nexus_compatibility=False,
                    prefix='norm',
                )
                norm_lrdata = LRData(_add_norm_nexus.wks, is_data=False, parent=self.parent)
                self.update_lrdata(lrdata=norm_lrdata, lconfig=lconfig, type='norm', row=index_row)

            is_display_requested = self.display_of_this_row_checked(index_row)
            if is_display_requested:
                self.display_plots(row=index_row)

            o_load_config_progressbar_handler.next_step()

        big_table_data = self.parent.big_table_data

    def display_plots(self, row=0):
        o_gui_utility = GuiUtility(parent=self.parent)
        is_data = o_gui_utility.is_data_tab_selected()

        DisplayPlots(parent=self.parent, row=row, is_data=is_data)

    def display_of_this_row_checked(self, row):
        _button_status = self.parent.ui.reductionTable.cellWidget(row, 0).checkState()
        if _button_status == 2:
            return True
        return False

    def get_nbr_lconfig(self):
        big_table_data = self.parent.big_table_data
        nbr_row = 0
        for index_row, lconfig in enumerate(big_table_data[:, 2]):
            if lconfig is None:
                return nbr_row
            nbr_row += 1
        return nbr_row

    def update_lrdata(self, lrdata=None, lconfig=None, type='data', row=0):
        big_table_data = self.parent.big_table_data

        if type == 'data':
            peak1 = int(lconfig.data_peak[0])
            peak2 = int(lconfig.data_peak[1])
            back1 = int(lconfig.data_back[0])
            back2 = int(lconfig.data_back[1])
            back_flag = lconfig.data_back_flag
            low_res1 = int(lconfig.data_low_res[0])
            low_res2 = int(lconfig.data_low_res[1])
            low_res_flag = lconfig.data_low_res_flag
            full_file_name = lconfig.data_full_file_name

        else:
            peak1 = int(lconfig.norm_peak[0])
            peak2 = int(lconfig.norm_peak[1])
            back1 = int(lconfig.norm_back[0])
            back2 = int(lconfig.norm_back[1])
            back_flag = lconfig.norm_back_flag
            low_res1 = int(lconfig.norm_low_res[0])
            low_res2 = int(lconfig.norm_low_res[1])
            low_res_flag = lconfig.norm_low_res_flag
            full_file_name = lconfig.norm_full_file_name

        tof_auto_flag = lconfig.tof_auto_flag
        tof_range = lconfig.tof_range

        # using lconfig values
        lrdata.peak = [peak1, peak2]
        lrdata.back = [back1, back2]
        lrdata.back_flag = back_flag
        lrdata.low_res = [low_res1, low_res2]
        lrdata.low_res_flag = low_res_flag
        lrdata.tof_range = tof_range
        lrdata.tof_auto_flag = tof_auto_flag
        lrdata.full_file_name = full_file_name

        index_col = 0 if type == 'data' else 1
        reduction_table_index_col = index_col + 1
        big_table_data[row, index_col] = lrdata
        self.parent.big_table_data = big_table_data

        if type == 'data':
            UpdateReductionTableMetadata(parent=self.parent, lrdata=lrdata, row=row)
            QtWidgets.QApplication.processEvents()

        # change color of data/norm field to inform data have been loaded
        _color = QtGui.QColor(RefRed.colors.VALUE_OK)
        self.parent.ui.reductionTable.item(row, reduction_table_index_col).setForeground(_color)
