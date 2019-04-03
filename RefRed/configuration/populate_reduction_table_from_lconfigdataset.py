class PopulateReductionTableFromLConfigDataSet(object):

    parent = None

    def __init__(self, parent=None):
        self.parent = parent
        
        big_table_data = self.parent.big_table_data
        
        for row_index, lconfig in enumerate(big_table_data[:,2]):
            if lconfig is None:
                return
            data_sets = ",".join(lconfig.data_sets)
            self.parent.ui.reductionTable.item(row_index, 1).setText(data_sets)
            norm_sets = ",".join(lconfig.norm_sets)
            self.parent.ui.reductionTable.item(row_index, 2).setText(norm_sets)
