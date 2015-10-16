from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication


class ReducedAsciiTableHandler(object):
    
    list_filename_to_remove = []
    total_number_of_rows_in_table = -1
    
    def __init__(self, parent=None):
        self.parent = parent
        self.total_number_of_rows_in_table = self.parent.ui.reducedAsciiDataSetTable.rowCount()
    
    def remove_rows(self):
        self.__get_range_row_selected()
        self.__clear_o_stitching_ascii_widget()
        self.__clear_table_rows()
    
    def clear_table(self):
        pass
    
    def __clear_table_rows(self):
        if self.list_filename_to_remove == []:
            return
        
        index_row_to_remove = 0
        for row in range(self.total_number_of_rows_in_table):
            if self.parent.ui.reducedAsciiDataSetTable.item(row, 0) is None:
                break
            _row_file_name = str(self.parent.ui.reducedAsciiDataSetTable.item(row, 0).text())
            if _row_file_name in self.list_filename_to_remove:
                self.parent.ui.reducedAsciiDataSetTable.removeRow(index_row_to_remove)
                #self.parent.ui.reducedAsciiDataSetTable.item(row, 0).setText("")
                #self.parent.ui.reducedAsciiDataSetTable.cellWidget(row, 1).setCheckState(Qt.Unchecked)
            else:
                index_row_to_remove += 1
    
    def __get_range_row_selected(self):
        selected_range = self.parent.ui.reducedAsciiDataSetTable.selectedRanges()
        _to_row = selected_range[0].bottomRow()
        _from_row = selected_range[0].topRow()
        
        # user can not remove row of live reduced data
        list_filename_to_remove = []
        for row in range(_from_row, _to_row+1):
            file_name = str(self.parent.ui.reducedAsciiDataSetTable.item(row,0).text())
            if file_name != 'LAST REDUCED SET':
                list_filename_to_remove.append(file_name)
        self.list_filename_to_remove = list_filename_to_remove

    def __clear_o_stitching_ascii_widget(self):
        o_stitching_ascii_widget = self.parent.o_stitching_ascii_widget

        print('before')
        print(o_stitching_ascii_widget.loaded_ascii_array)

        o_stitching_ascii_widget.remove_data(list_file_to_remove = 
                                             self.list_filename_to_remove)
        self.parent.o_stitching_ascii_widget = o_stitching_ascii_widget

        print('after')
        print(o_stitching_ascii_widget.loaded_ascii_array)

