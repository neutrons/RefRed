"""
Generate reduction options from the reduction table.

Note from code review:
It's not clear why the configuration stored in big_table_data[:, 3]
is saved if it's not used here. It creates confusion as to where we should
keep this information.
"""

# standard imports
from typing import Any, List, Optional

# package imports
from RefRed.calculations.lr_data import LRData
from RefRed.tabledata import TableData


class IndividualReductionSettingsHandler(object):

    data = None
    norm = None
    output_workspace = ''

    def __init__(self, parent=None, row_index=-1):
        self.parent = parent
        self.row_index = row_index
        self.big_table_data: TableData = self.parent.big_table_data
        self.data: LRData = self.big_table_data.reflectometry_data(row_index)
        self.norm: Optional[LRData] = self.big_table_data.normalization_data(row_index)
        self.retrieve()

    def retrieve(self):
        self._data_run_numbers = self.get_data_run_numbers()
        self._data_peak_range = self.get_data_peak_range()
        self._data_back_range = self.get_data_back_range()
        self._data_low_res_flag = self.get_data_low_res_flag()
        self._data_low_res_range = self.get_data_low_res_range()

        if self.norm is None:
            self._norm_run_numbers = None
            self._norm_peak_range = None
            self._norm_back_range = None
            self._norm_low_res_flag = None
            self._norm_low_res_range = None
        else:
            self._norm_run_numbers = self.get_norm_run_numbers()
            self._norm_peak_range = self.get_norm_peak_range()
            self._norm_back_range = self.get_norm_back_range()
            self._norm_low_res_flag = self.get_norm_low_res_flag()
            self._norm_low_res_range = self.get_norm_low_res_range()

        self._tof_range = self.get_tof_range()
        self._output_workspace_name = self.define_output_workspace_name(run_numbers=self._data_run_numbers)
        self._const_q = self.get_const_q()

    def to_dict(self):
        """
        Return a dictionary with the reduction options
        """
        self.retrieve()

        def norm_setting(setting: str) -> Optional[Any]:
            r"""Normalization data item, or None if we have no normalization"""
            return None if self.norm is None else getattr(self.norm, setting)

        pars = dict(
            data_files=self._data_run_numbers,
            norm_file=self._norm_run_numbers,
            data_peak_range=self._data_peak_range,
            subtract_background=self.data.back_flag,
            two_backgrounds=self.data.two_backgrounds,  # should we use both background regions?
            functional_background=self.data.two_backgrounds,  # should have same value as `two_backgrounds`
            background_roi=self._data_back_range,
            data_x_range_flag=self._data_low_res_flag,
            data_x_range=self._data_low_res_range,
            norm_peak_range=self._norm_peak_range,
            subtract_norm_background=norm_setting("back_flag"),
            norm_background_roi=self._norm_back_range,
            norm_x_range_flag=self._norm_low_res_flag,
            norm_x_range=self._norm_low_res_range,
            tof_range=self._tof_range,
            const_q=self._const_q,
        )
        return pars

    def define_output_workspace_name(self, run_numbers=None):
        str_run_numbers = run_numbers
        return "reflectivity_%s" % str_run_numbers

    def get_tof_range(self):
        is_auto_tof_range_selected = self.is_auto_tof_range_selected()
        if is_auto_tof_range_selected:
            tof_range = self.get_auto_tof_range()
        else:
            tof_range = self.get_manual_tof_range()
        tof_range_micros = self.convert_tof_range_to_micros(tof_range=tof_range)
        return tof_range_micros

    def convert_tof_range_to_micros(self, tof_range=None):
        tof1 = float(tof_range[0])
        if tof1 < 100:
            tof1_micros = tof1 * 1000.0
            tof2_micros = float(tof_range[1]) * 1000.0
        else:
            tof1_micros = tof1
            tof2_micros = float(tof_range[1])
        return [tof1_micros, tof2_micros]

    def get_auto_tof_range(self):
        _data = self.data
        return _data.tof_range_auto

    def get_manual_tof_range(self):
        _data = self.data
        return _data.tof_range_manual

    def is_auto_tof_range_selected(self):
        _data = self.data
        return bool(_data.tof_range_auto_flag)

    def get_data_low_res_flag(self):
        _data = self.data
        return self.get_low_res_flag(data=_data)

    def get_norm_low_res_flag(self):
        _norm = self.norm
        return self.get_low_res_flag(data=_norm)

    def get_low_res_flag(self, data=None):
        return bool(data.low_res_flag)

    def get_data_low_res_range(self):
        _data = self.data
        return self.get_low_res_range(data=_data)

    def get_norm_low_res_range(self):
        _norm = self.norm
        return self.get_low_res_range(data=_norm)

    def get_low_res_range(self, data=None):
        low_res1 = int(data.low_res[0])
        low_res2 = int(data.low_res[1])
        low_res_min = min([low_res1, low_res2])
        low_res_max = max([low_res1, low_res2])
        return [low_res_min, low_res_max]

    def get_data_back_range(self):
        _data = self.data
        return self.get_back_range(data=_data, is_data=True)

    def get_norm_back_range(self):
        _norm = self.norm
        return self.get_back_range(data=_norm, is_data=False)

    def get_back_range(self, data=None, is_data: bool = True) -> List[int]:
        r"""
        Genenerate a list containing the lower and upper bounds of the background regions.

        For reflectivity data we return two background regions, and only one region for direct-beam data.

        Parameters
        ----------
        data: LRData
            either reflectivity or direct-beam data
        is_data: bool
            `True` for reflectivity data and `False` for direct-beam data

        Returns
        -------
            Single list containing the lower and upper ranges for the background regions
        """
        assert data

        def sort_background(back: List[Any]):
            return sorted([int(back[0]), int(back[1])])

        if is_data:
            return sort_background(data.back) + sort_background(data.back2)
        else:
            return sort_background(data.back)  # for direct-beam data, fetch only the first background

    def get_data_peak_range(self):
        _data = self.data
        return self.get_peak_range(data=_data)

    def get_norm_peak_range(self):
        _norm = self.norm
        return self.get_peak_range(data=_norm)

    def get_peak_range(self, data=None):
        peak1 = int(data.peak[0])
        peak2 = int(data.peak[1])
        peak_min = min([peak1, peak2])
        peak_max = max([peak1, peak2])
        return [peak_min, peak_max]

    def get_norm_run_numbers(self):
        return self.get_run_numbers(column_index=2)

    def get_data_run_numbers(self):
        return self.get_run_numbers(column_index=1)

    def get_run_numbers(self, column_index=1):
        run_numbers = self.parent.ui.reductionTable.item(self.row_index, column_index).text()
        return str(run_numbers)

    def get_const_q(self):
        return bool(self.data.const_q)
