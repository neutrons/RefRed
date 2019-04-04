from mantid.simpleapi import *

class CheckIfSameNxsProperty(object):

    is_same_property = False
    property_name = ''

    def __init__(self, list_wks=None, property_name=property_name):
        if list_wks is None:
            return
        self.property_name = property_name

        if len(list_wks) < 2:
            self.is_same_property = True
            return

        _lambda_source = self.get_lambda_requested(list_wks[0])
        for index in range(1, len(list_wks)):
                _lambda_target = self.get_lambda_requested(list_wks[index])
                if (_lambda_target != _lambda_source):
                    self.is_same_property = False
                    return

        self.is_same_property = True

    def get_lambda_requested(self, wks):
        wks = mtd[wks]
        mt_run = wks.getRun()
        lambda_requested = float(mt_run.getProperty(self.property_name).value[0])
        return lambda_requested
