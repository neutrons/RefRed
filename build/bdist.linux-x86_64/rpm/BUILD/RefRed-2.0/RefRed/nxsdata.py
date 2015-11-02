class NXSdata(object):

    loading_success = False
    
    def __init__(self, nexus_file_name = None):
        if nexus_file_name is None:
            return
        
        
        