import logging

from RefRed.sf_calculator.compare_two_nxsdata_for_sfcalculator import CompareTwoNXSDataForSFcalculator


class Position(object):
    before = -1
    same = 0
    after = 1

class SortNXSData(object):

    sortedArrayOfNXSData = None
    sf_gui = None

    def __init__(self, arrayOfNXSDataToSort, parent=None):
        nbr_runs = len(arrayOfNXSDataToSort)
        if nbr_runs < 2:
            self.sortedArrayOfNXSData = arrayOfNXSDataToSort

        self.sf_gui = parent
        _sortedArrayOfNXSData = [arrayOfNXSDataToSort[0]]
        _positionIndexNXSDataToPosition = 0

        for source_index in range(1, nbr_runs):
            _is_same_nxs = False
            _nxsdataToPosition = arrayOfNXSDataToSort[source_index]
            for indexInPlace in range(len(_sortedArrayOfNXSData)):
                _nxsdataToCompareWith = _sortedArrayOfNXSData[indexInPlace]
                compareTwoNXSData = CompareTwoNXSDataForSFcalculator(_nxsdataToCompareWith, _nxsdataToPosition)
                _isBeforeSameOrAfter = compareTwoNXSData.result()
                if _isBeforeSameOrAfter == Position.before:
                    _positionIndexNXSDataToPosition = indexInPlace
                    break
                elif _isBeforeSameOrAfter == Position.after:
                    _positionIndexNXSDataToPosition += 1
                else:
                    #TODO: it's not clear what this branch does and whether we ever get here
                    _new_nxsdata = self.mergedNXSData(_nxsdataToPosition, _nxsdataToCompareWith)
                    _sortedArrayOfNXSData[indexInPlace] = _new_nxsdata
                    _is_same_nxs = True
                    break
            if not _is_same_nxs:
                _sortedArrayOfNXSData.insert(_positionIndexNXSDataToPosition, _nxsdataToPosition)
        self.sortedArrayOfNXSData = _sortedArrayOfNXSData

    def mergedNXSData(self, nxsdata1, nxsdata2):
        logging.error("SortNXSData.mergedNXSData not implemented")
        _full_file_name1 = nxsdata1.active_data.filename
        _full_file_name2 = nxsdata2.active_data.filename
        #_new_nxsdata = NXSData([_full_file_name1, _full_file_name2], bins=self.sf_gui.bin_size, is_auto_peak_finder=True)
        return None #_new_nxsdata

    def getSortedList(self):
        return self.sortedArrayOfNXSData
