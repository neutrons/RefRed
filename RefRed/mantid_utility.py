from mantid.api import AnalysisDataService
from mantid.simpleapi import DeleteWorkspace


class MantidUtility(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def cleanup_workspaces(self):
        ws_list = AnalysisDataService.getObjectNames()
        for _ws in ws_list:
            # if (_ws.endswith('_rebin') or _ws.startswith('_')):
            DeleteWorkspace(_ws)
