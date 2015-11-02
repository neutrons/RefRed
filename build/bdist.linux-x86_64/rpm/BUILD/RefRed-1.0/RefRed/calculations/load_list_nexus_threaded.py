import time

from mantid.simpleapi import *
from RefRed.thread.load_nexus import LoadNexus as ThreadLoadNexus

class LoadListNexusThreaded(object):

    list_nexus = None
    list_run = None
    list_wks = []
    thread_array = []
    
    run_found = 0
    number_of_runs = 0
    runs_loaded = 0 # use by thread to check when to stop
    
    def __init__(self, list_nexus=None, list_run=None, metadata_only=False):
        if list_nexus is None:
            return
        self.list_nexus = list_nexus
        self.list_run = list_run
        self.number_of_runs = len(list_run)
        
        self.init_thread_array()
        
        for index, nexus_name in enumerate(list_nexus):
            _run = list_run[index]
            _ws_name = "_data_file_%s" %_run
            _thread = self.thread_array[index]
            _thread.setup(self, nexus_name, _ws_name, metadata_only=metadata_only)
            _thread.start()
        
        print('-> self.runs_loaded: %d\n' %self.runs_loaded)
        print('-> self.number_of_runs: %d\n' %self.number_of_runs)
        while (self.runs_loaded < self.number_of_runs):
            print("inside while condition \n")
            time.sleep(0.5)
            
        print("Done!")
        print(len(self.list_wks))
        
    def init_thread_array(self):
        for i in range(len(self.list_nexus)):
            self.thread_array.append(ThreadLoadNexus())
