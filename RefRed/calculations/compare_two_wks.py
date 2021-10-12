from mantid.api import mtd


class CompareTwoWks(object):
    '''
    will return -1, 0 or 1 according to the position of the wksToPosition in relation to the
    wksToCompareWith based on the following criteria
    '''

    wks_to_compare_with_run = None
    wks_to_position_run = None
    result_comparison = 0

    def __init__(self, wks_to_compare_with=None, wks_to_position=None, criteria1=None, criteria2=None):

        self.wks_to_compare_with_run = wks_to_compare_with
        self.wks_to_position_run = wks_to_position

        compare1 = self.compare_parameter(criteria1[0], criteria1[1])
        if compare1 != 0:
            self.result_comparison = compare1
            return

        compare2 = self.compare_parameter(criteria2[0], criteria2[1])
        if compare2 != 0:
            self.result_comparison = compare2
            return

    def compare_parameter(self, param, order, param_backup=None):
        _wks_to_compare_with_run = mtd[self.wks_to_compare_with_run]
        _wks_to_position_run = mtd[self.wks_to_position_run]

        _wks_to_compare_with_run = _wks_to_compare_with_run.getRun()
        _wks_to_position_run = _wks_to_position_run.getRun()

        try:
            _param_wks_to_compare_with = float(_wks_to_compare_with_run.getProperty(param).value[0])
            _param_wks_to_position = float(_wks_to_position_run.getProperty(param).value[0])
        except:
            _param_wks_to_compare_with = float(_wks_to_compare_with_run.getProperty(param_backup).value[0])
            _param_wks_to_position = float(_wks_to_position_run.getProperty(param_backup).value[0])

        self.param_wks_to_compare_with = _param_wks_to_compare_with
        self.param_wks_to_position = _param_wks_to_position

        if order == 'ascending':
            result_less_than = -1
            result_more_than = 1
        else:
            result_less_than = 1
            result_more_than = -1

        if _param_wks_to_position < _param_wks_to_compare_with:
            return result_less_than
        elif _param_wks_to_position > _param_wks_to_compare_with:
            return result_more_than
        else:
            return 0

    def result(self):
        return self.result_comparison
