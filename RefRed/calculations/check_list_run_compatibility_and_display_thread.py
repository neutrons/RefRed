class CheckListRunCompatibilityAndDisplayThread(object):
    
    def __init__(self, parent=None, 
                 list_run=None,
                 list_nexs=None,
                 row=-1,
                 is_working_with_data_column=True,
                 is_display_requested=False):
        if parent is None:
            return
        
        self.parent = parent
        self.list_run = list_run
        self.list_nexus = list_nexus
        self.row = row
        self.is_working_with_data_column = is_working_with_data_column
        self.is_display_requested = is_display_requested
        