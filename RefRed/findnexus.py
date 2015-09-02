from run_sequence_breaker import RunSequenceBreaker
import nexus_utilities

class FindNexus(object):
    
    nexus_found = []
    run_number_not_found = []
    
    def __init__(self, runs_string = None):
        if list_runs == None:
            return ''
        
        oListRuns = RunSequenceBreaker(list_runs)
        list_run_number = oListRuns.getFinalList()
        
        for run_number in list_run_number:
            try:
                full_file_name = nexus_utilities.findNeXusFullPath(int(run_number))
                self.nexus_found.append(full_file_name)
            except:
                run_number_found.append(run_number)
        