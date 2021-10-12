class CompareTwoNXSDataForSFcalculator(object):
    '''
    will return -1, 0 or 1 according to the position of the nexusToPosition in relation to the
    nexusToCompareWith based on the following criteria
    #1: number of attenuators (ascending order)
    #2: lambda requested (descending order)
    #3: S2W (ascending order)
    #4: S2H (descending order)
    #5 if everything up to this point is identical, return 0
    '''

    nexusToCompareWithRun = None
    nexusToPositionRun = None
    mtdToCompareWith = None
    mtdToPosition = None

    resultComparison = 0

    def __init__(self, nxsdataToCompareWith, nxsdataToPosition):
        self.nexusToCompareWithRun = nxsdataToCompareWith.workspace.getRun()
        self.nexusToPositionRun = nxsdataToPosition.workspace.getRun()

        self.mtdToCompareWith = nxsdataToCompareWith.workspace
        self.mtdToPosition = nxsdataToPosition.workspace

        compare1 = self.compareParameter('LambdaRequest', 'descending')
        if compare1 != 0:
            self.resultComparison = compare1
            return

        compare2 = self.compareParameter('vATT', 'ascending')
        if compare2 != 0:
            self.resultComparison = compare2
            return

        compare3 = self.comparepCharge('descending')
        if compare3 != 0:
            self.resultComparison = compare3
            return

    def comparepCharge(self, order):
        _mtdToCompareWith = self.mtdToCompareWith
        _mtdToPosition = self.mtdToPosition

        _paramNexusToCompareWith = self.get_normalized_pcharge(_mtdToCompareWith)
        _paramNexusToPosition = self.get_normalized_pcharge(_mtdToPosition)

        if order == 'ascending':
            resultLessThan = -1
            resultMoreThan = 1
        else:
            resultLessThan = 1
            resultMoreThan = -1

        if _paramNexusToPosition < _paramNexusToCompareWith:
            return resultLessThan
        elif _paramNexusToPosition > _paramNexusToCompareWith:
            return resultMoreThan
        else:
            return 0

    def get_normalized_pcharge(self, _mtd):
        _run = _mtd.getRun()
        pcharge = float(_run.getProperty('gd_prtn_chrg').value)

        # FIXME get total counts and divide pcharge/total_counts
        total_counts = float(_mtd.getNumberEvents())

        normalized_pcharge = pcharge / total_counts
        return normalized_pcharge

    def compareParameter(self, param, order, param_backup=None):
        _nexusToCompareWithRun = self.nexusToCompareWithRun
        _nexusToPositionRun = self.nexusToPositionRun

        try:
            _paramNexusToCompareWith = float(_nexusToCompareWithRun.getProperty(param).value[0])
            _paramNexusToPosition = float(_nexusToPositionRun.getProperty(param).value[0])
        except:
            _paramNexusToCompareWith = float(_nexusToCompareWithRun.getProperty(param_backup).value[0])
            _paramNexusToPosition = float(_nexusToPositionRun.getProperty(param_backup).value[0])

        if order == 'ascending':
            resultLessThan = -1
            resultMoreThan = 1
        else:
            resultLessThan = 1
            resultMoreThan = -1

        if _paramNexusToPosition < _paramNexusToCompareWith:
            return resultLessThan
        elif _paramNexusToPosition > _paramNexusToCompareWith:
            return resultMoreThan
        else:
            return 0

    def result(self):
        return self.resultComparison
