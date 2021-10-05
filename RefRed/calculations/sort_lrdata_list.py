from RefRed.calculations.compare_two_lrdata import CompareTwoLRData


class Position(object):
    before = -1
    same = 0
    after = 1


class SortLRDataList(object):
    parent = None

    list_lrdata_sorted = None
    list_runs_sorted = None
    list_wks_sorted = None
    list_nexus_sorted = None

    list_lrdata = None
    list_runs = None
    list_wks = None
    list_nexus = None

    criteria1_value = None
    criteria1_type = ''

    criteria2_value = None
    criteria2_type = ''

    def __init__(
        self, parent=None, list_lrdata=None, list_runs=None, list_wks=None, list_nexus=None, data_type_selected='data'
    ):

        self.list_lrdata = list_lrdata
        self.list_runs = list_runs
        self.list_wks = list_wks
        self.parent = parent
        self.list_nexus = list_nexus
        self.is_data_type_selected = True if data_type_selected == 'data' else False

    def run(self):
        if len(self.list_lrdata) < 2:
            self.list_lrdata_sorted = self.list_lrdata
            self.list_runs_sorted = self.list_runs
            self.list_wks_sorted = self.list_wks
            self.list_nexus_sorted = self.list_nexus
            return

        if not self.is_data_type_selected:
            self.list_lrdata_sorted = list(self.list_lrdata)
            self.list_runs_sorted = list(self.list_runs)
            self.list_wks_sorted = list(self.list_wks)
            self.list_nexus_sorted = list(self.list_nexus)
            return

        self.run_data()

    def run_data(self):
        _list_wks = self.list_wks
        _list_runs = self.list_runs
        _list_lrdata = self.list_lrdata
        _list_nexus = self.list_nexus

        list_lrdata_sorted = [_list_lrdata[0]]
        list_runs_sorted = [_list_runs[0]]
        list_wks_sorted = [_list_wks[0]]
        list_nexus_sorted = [_list_nexus[0]]

        for index_lrdata_mov in range(1, len(_list_lrdata)):
            lrdata_mov = _list_lrdata[index_lrdata_mov]
            runs_mov = _list_runs[index_lrdata_mov]
            wks_mov = _list_wks[index_lrdata_mov]
            nexus_mov = _list_nexus[index_lrdata_mov]

            for index_lrdata_fix in range(len(list_lrdata_sorted)):
                lrdata_fix = list_lrdata_sorted[index_lrdata_fix]
                runs_fix = list_runs_sorted[index_lrdata_fix]
                wks_fix = list_wks_sorted[index_lrdata_fix]
                nexus_fix = list_nexus_sorted[index_lrdata_fix]

                if type(lrdata_fix) == type([]):
                    lrdata_fix = lrdata_fix[0]
                    runs_fix = runs_fix[0]
                    wks_fix = wks_fix[0]
                    nexus_fix = nexus_fix[0]

                o_compare_lrdata = CompareTwoLRData(lrdata_1=lrdata_fix, lrdata_2=lrdata_mov)

                if o_compare_lrdata.result_comparison < 0:
                    list_lrdata_sorted.insert(index_lrdata_fix, lrdata_mov)
                    list_runs_sorted.insert(index_lrdata_fix, runs_mov)
                    list_wks_sorted.insert(index_lrdata_fix, wks_mov)
                    list_nexus_sorted.insert(index_lrdata_fix, nexus_mov)
                    break

                elif o_compare_lrdata.result_comparison > 0:
                    if index_lrdata_fix == (len(list_lrdata_sorted) - 1):
                        list_lrdata_sorted.append(lrdata_mov)
                        list_runs_sorted.append(runs_mov)
                        list_wks_sorted.append(wks_mov)
                        list_nexus_sorted.append(nexus_mov)
                        break

                else:
                    if type(lrdata_fix) == type([]):
                        lrdata_mov = lrdata_fix.append(lrdata_mov)
                        runs_mov = runs_fix.append(runs_mov)
                        wks_mov = wks_fix.append(wks_mov)
                        nexus_mov = nexus_fix.append(nexus_mov)
                    else:
                        lrdata_mov = [lrdata_fix, lrdata_mov]
                        runs_mov = [runs_fix, runs_mov]
                        wks_mov = [wks_fix, wks_mov]
                        nexus_mov = [nexus_fix, nexus_mov]

                    list_lrdata_sorted[index_lrdata_fix] = lrdata_mov
                    list_runs_sorted[index_lrdata_fix] = runs_mov
                    list_wks_sorted[index_lrdata_fix] = wks_mov
                    list_nexus_sorted[index_lrdata_fix] = nexus_mov
                    break

            self.list_runs_sorted = list_runs_sorted
            self.list_lrdata_sorted = list_lrdata_sorted
            self.list_wks_sorted = list_wks_sorted
            self.list_nexus_sorted = list_nexus_sorted
