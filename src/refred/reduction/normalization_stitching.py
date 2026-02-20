from lr_reduction.scaling_factors import OverlapScalingFactor, ReducedData, scaling_factor_critical_edge


def _lconfig_to_reduced_data(lconfig) -> ReducedData:
    """Convert LConfigDataset to the ReducedData dataclass used in scaling factor calculation"""
    return ReducedData(
        q=lconfig.reduce_q_axis,
        r=lconfig.reduce_y_axis,
        err=lconfig.reduce_e_axis,
    )


class ParentHandler(object):
    def __init__(self, parent=None, row_index=0, n_runs=1):
        self.parent = parent
        self.row_index = row_index
        self.n_runs = n_runs

    def _calculateSFCE(self, first_q_row: int, data_type="absolute"):
        """
        Scaling factor calculation of Critical Edge (CE)
        """
        q_min = float(str(self.parent.ui.sf_qmin_value.text()))
        q_max = float(str(self.parent.ui.sf_qmax_value.text()))

        # Build list of ReducedData for all runs
        all_data = [
            _lconfig_to_reduced_data(self.parent.big_table_data.reduction_config(row_index))
            for row_index in range(self.n_runs)
        ]

        sf = scaling_factor_critical_edge(q_min, q_max, all_data)

        # Save the SF in the lowest-q run (first in q-sorted order)
        self.saveSFinLConfig(self.parent.big_table_data.reduction_config(first_q_row), sf, data_type=data_type)

    def saveSFinLConfig(self, lconfig, sf, data_type="absolute"):
        if data_type == "absolute":
            lconfig.sf_abs_normalization = sf
        elif data_type == "auto":
            lconfig.sf_auto = sf
        else:
            lconfig.sf_manual = sf
        return lconfig

    def getLConfig(self, row_index):
        big_table_data = self.parent.big_table_data
        data_set = big_table_data[row_index, 2]
        return data_set


class AbsoluteNormalization(ParentHandler):
    """
    Absolute normalization of reduced data.
    """

    def __init__(self, parent=None, row_index=0, n_runs=1):
        super().__init__(parent=parent, row_index=row_index, n_runs=n_runs)

    def run(self):
        sorted_indices = self.parent.big_table_data.get_q_sorted_indices()
        first_q_row = sorted_indices[0] if sorted_indices else 0

        if self.row_index == first_q_row:
            if self.parent.ui.sf_button.isChecked():
                self.useManuallyDefineSF(first_q_row)
            else:
                self._calculateSFCE(first_q_row)
        else:
            self.copySFtoOtherAngles(first_q_row)

    def useManuallyDefineSF(self, first_q_row: int):
        _sf = float(str(self.parent.ui.sf_value.text()))
        data_set = self.getLConfig(first_q_row)
        data_set.sf_abs_normalization = _sf

    def copySFtoOtherAngles(self, first_q_row: int):
        ce_lconfig = self.getLConfig(first_q_row)
        _sf = ce_lconfig.sf_abs_normalization
        lconfig = self.getLConfig(self.row_index)
        self.saveSFinLConfig(lconfig, _sf, data_type="absolute")


class AutomaticStitching(ParentHandler):
    """
    Automatic stitching of the reduced data using the Q overlap range.
    """

    def __init__(self, parent=None, row_index=0, n_runs=1):
        super().__init__(parent=parent, row_index=row_index, n_runs=n_runs)

    def run(self):
        self.use_first_angle_range()

    def use_first_angle_range(self):
        sorted_indices = self.parent.big_table_data.get_q_sorted_indices()
        first_q_row = sorted_indices[0] if sorted_indices else 0

        if self.row_index == first_q_row:
            self._calculateSFCE(first_q_row, data_type="auto")
        else:
            self._calculateSFOtherAngles()

    def _calculateSFOtherAngles(self):
        """
        Scaling factor calculation for non-first-angle runs
        """
        sorted_indices = self.parent.big_table_data.get_q_sorted_indices()

        try:
            q_position = sorted_indices.index(self.row_index)
        except ValueError:
            return

        left_row = sorted_indices[q_position - 1]
        right_row = self.row_index

        left_lconfig = self.getLConfig(left_row)
        right_lconfig = self.getLConfig(right_row)

        left_data = _lconfig_to_reduced_data(left_lconfig)
        right_data = _lconfig_to_reduced_data(right_lconfig)

        calculator = OverlapScalingFactor(
            left_data=left_data,
            right_data=right_data,
            sf_auto=left_lconfig.sf_auto,  # propagate the cumulative auto-SF of the left neighbor
        )
        sf = 1.0 / calculator.get_scaling_factor()
        right_lconfig.sf_auto = sf


class ManualStitching(ParentHandler):
    """
    Manual stitching: uses the sf_manual value from the table as-is.
    """

    def __init__(self, parent=None, row_index=0, n_runs=1):
        super().__init__(parent=parent, row_index=row_index, n_runs=n_runs)

    def run(self):
        ce_lconfig = self.getLConfig(self.row_index)
        _sf = ce_lconfig.sf_manual
        lconfig = self.getLConfig(self.row_index)
        self.saveSFinLConfig(lconfig, _sf, data_type="manual")
