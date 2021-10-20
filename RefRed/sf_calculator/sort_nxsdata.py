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
                    # we should never get here since run number and data (ws) is
                    # one-to-one mapping
                    _is_same_nxs = True
                    break
            if not _is_same_nxs:
                _sortedArrayOfNXSData.insert(_positionIndexNXSDataToPosition, _nxsdataToPosition)
        self.sortedArrayOfNXSData = _sortedArrayOfNXSData

    def getSortedList(self):
        return self.sortedArrayOfNXSData
