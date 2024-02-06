# standard imports
from typing import List


class LConfigDataset(object):
    """
    This class will be used when loading an XML configuration file and will
    keep record of all the information loaded, such as peak, back, TOF range...
    until the data/norm file has been loaded
    """

    proton_charge = -1

    data_runs_compatible = True
    data_wks = None
    data_sets = ['']
    data_full_file_name = ['']
    data_peak: List[int] = ['0', '0']  # lower and upper boundaries for the peak
    data_back: List[int] = ['0', '0']  # lower and upper boundaries for the first background
    data_back2: List[int] = ['0', '0']  # lower and upper boundaries for the second background
    data_low_res = ['50', '200']
    data_back_flag: bool = True
    data_functional_background: bool = False
    data_two_backgrounds: bool = False
    data_low_res_flag = True
    data_lambda_requested = -1

    tof_range = ['0', '0']
    tof_units = 'ms'
    tof_auto_flag = True

    norm_runs_compatible = True
    norm_wks = None
    norm_sets = ['']
    norm_full_file_name = ['']
    norm_flag = True
    norm_peak = ['0', '0']
    norm_back = ['0', '0']
    norm_back2: List[int] = ['0', '0']  # lower and upper boundaries for the second background
    norm_back_flag: bool = True
    norm_functional_background: bool = False
    norm_two_backgrounds: bool = False

    norm_low_res = ['50', '200']
    norm_low_res_flag = True
    norm_lambda_requested = -1

    q_range = ['0', '0']
    lambda_range = ['0', '0']

    reduce_q_axis = []
    reduce_y_axis = []
    reduce_e_axis = []

    wks = None
    wks_scaled = None
    meta_data = None

    sf_auto = 1  # auto scaling calculated by program (auto stitching)
    sf_manual = 1  # manual scaling (manual stitching)
    sf_abs_normalization = 1  # absolute normalization

    sf_auto_found_match = False
    sf = 1  # scaling factor apply to data (will be either the auto, manual or 1)

    q_axis_for_display = []
    y_axis_for_display = []
    e_axis_for_display = []

    # use in the auto SF class
    tmp_y_axis = []
    tmp_e_axis = []

    def clear_normalization(self):
        """
        Clear the normalization information
        Note: it's not clear what data_sets and data_full_file_name are good for,
        so we are clearing them by assigning them the default in the class definition.
        """
        self.norm_wks = None
        self.norm_sets = LConfigDataset.norm_sets
        self.norm_full_file_name = LConfigDataset.norm_full_file_name

    def clear_data(self):
        """
        Clear the scattering data information
        Note: it's not clear what norm_sets and norm_full_file_name are good for,
        so we are clearing them by assigning them the default in the class definition.
        """
        self.data_wks = None
        self.data_sets = LConfigDataset.norm_sets
        self.data_full_file_name = LConfigDataset.norm_full_file_name
