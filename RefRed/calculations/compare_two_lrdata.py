class CompareTwoLRData(object):
    
    def __init__(self,
                 lrdata_1 = None,
                 lrdata_2 = None,
                 is_data_type_selected = True):
        
        self.lrdata_1 = lrdata_1
        self.lrdata_2 = lrdata_2
        self.result_comparison = 0
        
        compare1 = self.compare_lambda_requested()
        if compare1 != 0:
            self.result_comparison = compare1
            return
        
        # no need to check theta when working with norm runs
        if not is_data_type_selected:
            return
        
        compare2 = self.compare_theta()
        if compare2 != 0:
            self.result_comparison = compare2
            return
        
    def compare_lambda_requested(self):
        ''' sorting in descending order '''

        _lrdata_1 = self.lrdata_1
        _lrdata_2 = self.lrdata_2
        
        value_1 = _lrdata_1.lambda_requested
        value_2 = _lrdata_2.lambda_requested
        
        if value_1 < value_2:
            return -1
        elif value_1 > value_2:
            return 1
        else:
            return 0
        
    def compare_theta(self):
        ''' sorting in ascending order '''

        _lrdata_1 = self.lrdata_1
        _lrdata_2 = self.lrdata_2
        
        value_1 = _lrdata_1.theta
        value_2 = _lrdata_2.theta
        
        if value_1 < value_2:
            return -1
        elif value_1 > value_2:
            return 1
        else:
            return 0
        
        
        