from qtpy import QtGui
from qtpy.QtWidgets import QApplication

from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker
from RefRed.calculations.check_list_run_compatibility_and_display_thread import CheckListRunCompatibilityAndDisplayThread
import RefRed.colors
from RefRed.calculations.locate_list_run import LocateListRun


class UpdateReductionTable(object):

    raw_runs = None
    is_data_displayed = True

    def __init__(self, parent=None, row=0, col=1, runs=None):
        self.parent= parent
        self.row = row
        self.col = col

        item = self.parent.ui.reductionTable.item(row, col)
        if item.text() == '':
            self.clear_cell(row, col)
            self.parent.file_loaded_signal.emit()
            QApplication.processEvents()
            return

        data_type = 'data' if col == 1 else 'norm'
        self.is_data_displayed = True if (col == 1) else False

        self.raw_runs = str(runs)
        run_breaker = RunSequenceBreaker(run_sequence=self.raw_runs)
        list_run = run_breaker.final_list

        # check if nexus can be found
        list_run_object = LocateListRun(list_run=list_run)
        if list_run_object.list_run_not_found != []:
            str_list_run_not_found = [str(x) for x in list_run_object.list_run_not_found]
            runs_not_located = ', '.join(str_list_run_not_found)
            mess = "Can not locate %s run(s): %s" %(data_type, runs_not_located)
            self.parent.ui.reductionTable.item(row, 8).setText(mess)
            _color = QtGui.QColor(RefRed.colors.VALUE_BAD)
            self.parent.ui.reductionTable.item(row, 8).setBackground(_color)
        else:
            mess = "%s runs have been located!" % data_type
            self.parent.ui.reductionTable.item(row, 8).setText(mess)
            _color = QtGui.QColor(RefRed.colors.VALUE_OK)
            self.parent.ui.reductionTable.item(row, 8).setBackground(_color)

        list_run_found = list(list_run_object.list_run_found)

        if list_run_found == []:
            self.parent.ui.reductionTable.item(row, col).setText('')
            return
        str_list_run_found = [str(x) for x in list_run_found]
        final_list_run_found = ','.join(str_list_run_found)
        self.parent.ui.reductionTable.item(row, col).setText(final_list_run_found)

        list_nexus_found = list_run_object.list_nexus_found
        thread_index = ((self.col-1) + 2*self.row)
        self.parent.loading_nxs_thread[thread_index] = CheckListRunCompatibilityAndDisplayThread()
        self.parent.loading_nxs_thread[thread_index].setup(parent=self.parent,
                       list_run = list_run_found,
                       list_nexus = list_nexus_found,
                       row = row,
                       is_working_with_data_column = self.is_data_displayed,
                       is_display_requested = self.display_of_this_row_checked())
        self.parent.loading_nxs_thread[thread_index].start()

    def clear_cell(self, row, col):
        """
            Clear a reduction table cell, and clean up what is left behind.
            The main "big_table_data" array has three entries per row,
                0: Scattering data <class 'RefRed.calculations.lr_data.LRData'>
                1: Direct beam data <class 'RefRed.calculations.lr_data.LRData'>
                2: Reduction options <class 'RefRed.lconfigdataset.LConfigDataset'>
            If col==1, we are clearing the scattering data.
            If col==2, we are clearing the direct beam.
        """
        # Clear the data and configuration
        # Note: there is a Mantid process cleaning process elsewhere in the code
        # so we don't have to deal with it here.
        config = self.parent.big_table_data[self.row, 2]
        if col==1:
            self.parent.big_table_data[self.row, 0] = None
            config.clear_data()
        elif col==2:
            self.parent.big_table_data[self.row, 1] = None
            config.clear_normalization()

    def display_of_this_row_checked(self):
        _button_status = self.parent.ui.reductionTable.cellWidget(self.row, 0).checkState()
        if _button_status == 2:
            return True
        return False
