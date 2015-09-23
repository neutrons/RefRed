class IndividualReductionSettingsHandler(object):
    
    data = None
    norm = None
    output_workspace = ''
    
    def __init__(self, parent=None, row_index=-1):
        self.parent = parent
        self.row_index = row_index
        big_table_data = self.parent.big_table_data
        self.data = big_table_data[row_index, 0]
        self.norm = big_table_data[row_index, 1]
        self.retrieve()
        
    def retrieve(self):
        self._data_run_numbers = self.get_data_run_numbers()
        self._data_peak_range = self.get_data_peak_range()
        self._data_back_flag = self.get_data_back_flag()
        self._data_back_range = self.get_data_back_range()
        self._data_low_res_flag = self.get_data_low_res_flag()
        self._data_low_res_range = self.get_data_low_res_range()

        self._norm_flag = self.get_norm_flag()
        self._norm_run_numbers = self.get_norm_run_numbers()
        self._norm_peak_range = self.get_norm_peak_range()
        self._norm_back_flag = self.get_norm_back_flag()
        self._norm_back_range = self.get_norm_back_range()
        self._norm_low_res_flag = self.get_norm_low_res_flag()
        self._norm_low_res_range = self.get_norm_low_res_range()
        
        self._tof_range = self.get_tof_range()
        self._output_workspace_name = self.define_output_workspace_name(run_numbers = 
                                                                        self._data_run_numbers)
        
    def define_output_workspace_name(self, run_numbers = None):
        str_run_numbers = run_numbers
        return "reflectivity_%s" % str_run_numbers
        
    def get_tof_range(self):
        is_auto_tof_range_selected = self.is_auto_tof_range_selected()
        if is_auto_tof_range_selected:
            tof_range = self.get_auto_tof_range()
        else:
            tof_range = self.get_manual_tof_range()
        tof_range_micros = self.convert_tof_range_to_micros(tof_range = tof_range)
        return tof_range_micros
        
    def convert_tof_range_to_micros(self, tof_range = None):
        tof1 = float(tof_range[0])
        if tof1 < 100:
            tof1_micros = tof1 * 1000.
            tof2_micros = float(tof_range[1]) * 1000.
        else:
            tof1_micros = tof1
            tof2_micros = float(tof_range[1])
        return [tof1_micros, tof2_micros]
        
    def get_auto_tof_range(self):
        _data = self.data
        return _data.tof_range_auto
        
    def get_manual_tof_range(self):
        _data = self.data
        return _data.tof_range_manual

    def is_auto_tof_range_selected(self):
        _data = self.data
        return bool(_data.tof_range_auto_flag)
        
    def get_data_low_res_flag(self):
        _data = self.data
        return self.get_low_res_flag(data = _data)
        
    def get_norm_low_res_flag(self):
        _norm = self.norm
        return self.get_low_res_flag(data = _norm)
        
    def get_low_res_flag(self, data = None):
        return bool(data.low_res_flag)
        
    def get_data_low_res_range(self):
        _data = self.data
        return self.get_low_res_range(data = _data)
    
    def get_norm_low_res_range(self):
        _norm = self.norm
        return self.get_low_res_range(data = _norm)

    def get_low_res_range(self, data = None):
        low_res1 = int(data.low_res[0])
        low_res2 = int(data.low_res[1])
        low_res_min = min([low_res1, low_res2])
        low_res_max = max([low_res1, low_res2])
        return [low_res_min, low_res_max]
        
    def get_norm_flag(self):
        _norm = self.norm
        return _norm.use_it_flag
        
    def get_data_back_range(self):
        _data = self.data
        return self.get_back_range(data = _data)
    
    def get_norm_back_range(self):
        _norm = self.norm
        return self.get_back_range(data = _norm)
    
    def get_back_range(self, data = None):
        back1 = int(data.back[0])
        back2 = int(data.back[1])
        back_min = min([back1, back2])
        back_max = max([back1, back2])
        return [back_min, back_max]
    
    def get_data_back_flag(self):
        _data = self.data
        return self.get_back_flag(data = _data)
    
    def get_norm_back_flag(self):
        _norm = self.norm
        return self.get_back_flag(data = _norm)
    
    def get_back_flag(self, data = None):
        return bool(data.back_flag)
        
    def get_data_peak_range(self):
        _data = self.data
        return self.get_peak_range(data=_data)
    
    def get_norm_peak_range(self):
        _norm = self.norm
        return self.get_peak_range(data=_norm)
    
    def get_peak_range(self, data=None):
        peak1 = int(data.peak[0])
        peak2 = int(data.peak[1])
        peak_min = min([peak1, peak2])
        peak_max = max([peak1, peak2])
        return [peak_min, peak_max]
        
    def get_norm_run_numbers(self):
        return self.get_run_numbers(column_index = 2)
        
    def get_data_run_numbers(self):
        return self.get_run_numbers(column_index = 1)

    def get_run_numbers(self, column_index = 1):
        run_numbers = self.parent.ui.reductionTable.item(self.row_index, column_index).text()
        return str(run_numbers)
