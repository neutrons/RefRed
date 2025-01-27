# standard imports
import logging
import math
from typing import List, Optional, Type

import numpy as np

# third-party imports
from mantid.api import mtd
from mantid.simpleapi import Rebin

# package imports
from RefRed.lconfigdataset import LConfigDataset
from RefRed.low_res_finder_algorithms.low_res_finder import LowResFinder
from RefRed.peak_finder_algorithms.peak_finder_derivation import PeakFinderDerivation
from RefRed.plot.all_plot_axis import AllPlotAxis
from RefRed.utilities import convert_angle

NEUTRON_MASS = 1.675e-27  # kg
PLANCK_CONSTANT = 6.626e-34  # m^2 kg s^-1
H_OVER_M_NEUTRON = PLANCK_CONSTANT / NEUTRON_MASS

NEW_GEOMETRY_DATE = "2014-10-01"


class LRData(object):
    read_options = dict(
        is_auto_tof_finder=True, is_auto_peak_finder=True, back_offset_from_peak=3, bins=50, angle_offset=0.001
    )

    tof_range = None
    tof_range_manual = None
    tof_range_auto = None
    tof_range_auto_flag = True

    low_res = [0, 255]
    low_res_flag = True
    use_it_flag = True
    full_file_name = [""]
    filename = ""
    ipts = "N/A"
    total_counts = 0

    def __init__(
        self,
        workspace,
        lconfig: Optional[LConfigDataset] = None,
        is_data=True,
        parent=None,
        reduction_table_cell: Optional[Type["LRData"]] = None,
    ):
        """
        Constructor for LRData class

        :param workspace: run workspace
        :param lconfig: if defined, use for peak, background, low res, TOF range
        :param is_data: if True, this is the data run, otherwise it is the normalization run
        :param parent: parent object
        :param reduction_table_cell: if defined, use for peak, background, low res, TOF range
        """
        # TODO: there appears to be duplicate instances of this class being
        #      created when loading a file.
        if lconfig and reduction_table_cell:
            raise ValueError("Can't use both lconfig and reduction_table_cell")

        self.parent = parent
        self._tof_axis: List[float] = []
        self.Ixyt: List[float] = []

        self.countxdata: List[int] = []
        self.ycountsdata: List[int] = []
        self.workspace_name = str(workspace)
        workspace = mtd[self.workspace_name]  # convert to workspace pointer

        mt_run = workspace.getRun()

        self.ipts = mt_run.getProperty("experiment_identifier").value
        self.run_number = mt_run.getProperty("run_number").value

        self.lambda_requested = float(mt_run.getProperty("LambdaRequest").value[0])
        self.lambda_requested_units = mt_run.getProperty("LambdaRequest").units
        self.thi = mt_run.getProperty("thi").value[0]
        self.thi_units = mt_run.getProperty("thi").units
        self.ths = mt_run.getProperty("ths").value[0]
        self.ths_units = mt_run.getProperty("ths").units
        self.tthd = mt_run.getProperty("tthd").value[0]
        self.tthd_units = mt_run.getProperty("tthd").units
        self.S1W = mt_run.getProperty("S1HWidth").value[0]
        self.S1H = mt_run.getProperty("S1VHeight").value[0]
        self.parent.current_ipts = mt_run.getProperty("experiment_identifier").value
        self.total_counts = workspace.getNumberEvents()

        try:
            self.SiW = mt_run.getProperty("SiHWidth").value[0]
            self.SiH = mt_run.getProperty("SiVHeight").value[0]
            self.isSiThere = True
        except:
            self.S2W = mt_run.getProperty("S2HWidth").value[0]
            self.S2H = mt_run.getProperty("S2VHeight").value[0]
            self.isSiThere = False

        self.attenuatorNbr = mt_run.getProperty("vATT").value[0] - 1
        self.date = mt_run.getProperty("run_start").value

        sample = workspace.getInstrument().getSample()
        source = workspace.getInstrument().getSource()
        self.dMS = sample.getDistance(source)

        # create array of distances pixel->sample
        self.number_x_pixels = int(workspace.getInstrument().getNumberParameter("number-of-x-pixels")[0])  # 256
        self.number_y_pixels = int(workspace.getInstrument().getNumberParameter("number-of-y-pixels")[0])

        # distance sample->center of detector
        x_index, y_index = int(self.number_x_pixels / 2), int(self.number_y_pixels / 2)
        detector = workspace.getDetector(self.number_x_pixels * x_index + y_index)
        self.dSD = sample.getDistance(detector)
        del x_index, y_index, detector

        # distance source->center of detector
        self.dMD = self.dSD + self.dMS

        # calculate theta
        self.theta = self.calculate_theta()
        self.frequency = float(mt_run.getProperty("Speed1").value[0])

        # Determine the range to select in TOF according to how the DAS computed the
        # chopper settings
        use_emission_delay = False
        if "BL4B:Chop:Skf2:ChopperModerator" in mt_run:
            base_path = mt_run.getProperty("BL4B:Det:TH:DlyDet:BasePath").value[0]
            moderator_calc = mt_run.getProperty("BL4B:Chop:Skf2:ChopperModerator").value[0]
            t_mult = mt_run.getProperty("BL4B:Chop:Skf2:ChopperMultiplier").value[0]
            t_off = mt_run.getProperty("BL4B:Chop:Skf2:ChopperOffset").value[0]
            use_emission_delay = moderator_calc == 1

        wl_half_width = 1.7 * 60 / self.frequency
        wl_delta_full_range = 0.8 * 60 / self.frequency

        # Calculate the TOF range to select
        if use_emission_delay:
            self.dMD = base_path

        tmin = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested - wl_half_width) * 1e-4
        tmax = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + wl_half_width) * 1e-4

        if use_emission_delay:
            wl_min = self.lambda_requested - wl_half_width
            wl_max = self.lambda_requested + wl_half_width
            tmin -= t_off + t_mult * wl_min
            tmax -= t_off + t_mult * wl_max

        if lconfig is not None:
            autotmin = float(lconfig.tof_range[0])
            autotmax = float(lconfig.tof_range[1])
        else:
            autotmin = tmin
            autotmax = tmax

        self.tof_range_auto = [autotmin, autotmax]  # microS

        # manual tof range (if user wants to use a manual time range)
        self.tof_range = [autotmin, autotmax]  # for the first time, initialize tof_range like auto (microS)
        self.tof_range_manual = [autotmin, autotmax]

        # Widen the range to show the entire TOF range in the plots
        delta_t = self.dMD / H_OVER_M_NEUTRON * wl_delta_full_range * 1e-4
        tmin -= delta_t
        if tmin < 0:
            tmin = 0
        tmax += delta_t

        self.binning = [tmin, self.read_options["bins"], tmax]
        self.calculate_lambda_range()
        self.incident_angle = 2.0 * self.calculate_theta(with_offset=False)  # 2.theta
        self.calculate_q_range()
        # self.lambda_range = self.calculate_lambda_range()

        # Proton charge
        _proton_charge = float(mt_run.getProperty("gd_prtn_chrg").value)
        # _proton_charge_units = mt_run.getProperty('gd_prtn_chrg').units
        new_proton_charge_units = "mC"

        self.proton_charge = _proton_charge * 3.6  # to go from microA/h to mC
        self.proton_charge_units = new_proton_charge_units

        self.peak: List[int] = [0, 0]  # lower and upper boundaries for the peak
        self.back: List[int] = [0, 0]  # lower and upper boundaries for the first background
        self.back2: List[int] = [0, 0]  # lower and upper boundaries for the second background
        self.back_flag: bool = True
        self.two_backgrounds: bool = False

        self.const_q: bool = False  # reduction using constant Q binning

        self.all_plot_axis = AllPlotAxis()
        self.tof_auto_flag = True
        self.new_detector_geometry_flag = self.is_nexus_taken_after_refDate()
        self.data_loaded = False
        self.read_data()

        if lconfig is not None:
            self.tof_auto_flag = bool(lconfig.tof_auto_flag)

            if is_data:
                self.peak = [int(lconfig.data_peak[0]), int(lconfig.data_peak[1])]
                self.back = [int(lconfig.data_back[0]), int(lconfig.data_back[1])]
                self.back2 = [int(lconfig.data_back2[0]), int(lconfig.data_back2[1])]

                self.low_res = [int(lconfig.data_low_res[0]), int(lconfig.data_low_res[1])]
                self.low_res_flag = bool(lconfig.data_low_res_flag)
                self.back_flag = bool(lconfig.data_back_flag)
                self.two_backgrounds = bool(lconfig.data_two_backgrounds)
                self.const_q = bool(lconfig.const_q)
            else:
                self.peak = [int(lconfig.norm_peak[0]), int(lconfig.norm_peak[1])]
                self.back = [int(lconfig.norm_back[0]), int(lconfig.norm_back[1])]
                self.back2 = [int(lconfig.norm_back2[0]), int(lconfig.norm_back2[1])]
                self.low_res = [int(lconfig.norm_low_res[0]), int(lconfig.norm_low_res[1])]
                self.low_res_flag = bool(lconfig.norm_low_res_flag)
                self.back_flag = bool(lconfig.norm_back_flag)
                self.two_backgrounds = bool(lconfig.norm_two_backgrounds)
                self.const_q = bool(lconfig.const_q)

        elif reduction_table_cell is not None:
            self.tof_auto_flag = reduction_table_cell.tof_auto_flag
            self.tof_range_auto = reduction_table_cell.tof_range_auto
            self.tof_range = reduction_table_cell.tof_range_auto
            self.tof_range_manual = reduction_table_cell.tof_range_auto
            self.peak = reduction_table_cell.peak
            self.back = reduction_table_cell.back
            self.back2 = reduction_table_cell.back2
            self.low_res = reduction_table_cell.low_res
            self.low_res_flag = reduction_table_cell.low_res_flag
            self.back_flag = reduction_table_cell.back_flag
            self.two_backgrounds = reduction_table_cell.two_backgrounds
            self.const_q = reduction_table_cell.const_q

        else:
            pf = PeakFinderDerivation(list(range(len(self.ycountsdata))), self.ycountsdata)
            [peak1, peak2] = pf.getPeaks()
            self.peak = [int(peak1), int(peak2)]

            backOffsetFromPeak = self.read_options["back_offset_from_peak"]
            back1 = int(peak1 - backOffsetFromPeak)
            back2 = int(peak2 + backOffsetFromPeak)
            self.back = [back1, back2]

            lw_pf = LowResFinder(list(range(len(self.countsxdata))), self.countsxdata)
            [lowres1, lowres2] = lw_pf.get_low_res()
            self.low_res = [int(lowres1), int(lowres2)]

    # Properties for easy data access
    # return the size of the data stored in memory for this dataset
    @property
    def xdata(self):
        return self.xydata.mean(axis=0)

    @property
    def ydata(self):
        return self.xydata.mean(axis=1)

    @property
    def tofdata(self):
        return self.xtofdata.mean(axis=0)

    # coordinates corresponding to the data items
    @property
    def x(self):
        return np.arange(self.xydata.shape[1])

    @property
    def y(self):
        return np.arange(self.xydata.shape[0])

    @property
    def xy(self):
        return np.meshgrid(self.x, self.y)

    @property
    def tof(self):
        return (self.tof_edges[:-1] + self.tof_edges[1:]) / 2.0

    @property
    def xtof(self):
        return np.meshgrid(self.tof, self.x)

    def calculate_q_range(self):
        """
        calculate q range
        """
        [lambda_min, lambda_max] = self.lambda_range
        _const = float(4) * math.pi
        theta_rad = convert_angle(angle=self.incident_angle)

        _const_theta = _const * math.sin(float(theta_rad) / 2.0)
        q_min = _const_theta / float(lambda_max)
        q_max = _const_theta / float(lambda_min)

        self.q_range = [q_min, q_max]

    def calculate_lambda_range(self, tof_range=None):
        """
        calculate lambda range
        """
        _const = PLANCK_CONSTANT / (NEUTRON_MASS * self.dMD)

        # retrieve tof from GUI
        if tof_range is None:
            [tof_min, tof_max] = self.tof_range
        else:
            [tof_min, tof_max] = tof_range

        lambda_min = _const * (tof_min * 1e-6) / float(1e-10)
        lambda_max = _const * (tof_max * 1e-6) / float(1e-10)

        lambda_min = "%.2f" % lambda_min
        lambda_max = "%.2f" % lambda_max

        self.lambda_range = [lambda_min, lambda_max]

    def calculate_theta(self, with_offset=True):
        """
        calculate theta
        """
        tthd_value = self.tthd
        thi_value = self.thi

        theta = math.fabs(tthd_value - thi_value) / 2.0
        if theta < 0.001:
            logging.debug("thi and tthd are equal: is this a direct beam?")

        # Add the offset
        angle_offset = 0.0
        if with_offset and "angle_offset" in self.read_options:
            angle_offset = float(self.read_options["angle_offset"])
            angle_offset_deg = angle_offset
            theta = theta + angle_offset_deg * math.pi / 180.0

        return theta

    def _getIxyt(self, nxs_histo):
        """
        will format the histogrma NeXus to retrieve the full 3D data set
        """
        self._tof_axis = nxs_histo.readX(0)[:].copy()
        nbr_tof = len(self._tof_axis)

        self.Ixyt = nxs_histo.extractY().reshape(self.number_x_pixels, self.number_y_pixels, nbr_tof - 1)

    def read_data(self):
        output_workspace_name = self.workspace_name + "_rebin"
        nxs_histo = Rebin(
            InputWorkspace=self.workspace_name,
            OutputWorkspace=output_workspace_name,
            Params=self.binning,
            PreserveEvents=True,
        )
        # retrieve 3D array
        self._getIxyt(nxs_histo)
        nxs_histo.delete()
        self.tof_axis_auto_with_margin = self._tof_axis

        # # keep only the low resolution range requested
        from_pixel = 0
        to_pixel = self.number_x_pixels - 1

        # keep only low resolution range defined
        self.Ixyt = self.Ixyt[from_pixel:to_pixel, :, :]

        # create projections for the 2D datasets
        self.xydata = self.Ixyt.sum(axis=2).transpose()  # 2D dataset
        self.ytofdata = self.Ixyt.sum(axis=0)  # 2D dataset

        self.countstofdata = self.Ixyt.sum(axis=0).sum(axis=0)
        self.countsxdata = self.Ixyt.sum(axis=2).sum(axis=1)
        self.ycountsdata = self.ytofdata.sum(axis=1)

        self.data_loaded = True

    def is_nexus_taken_after_refDate(self):
        """
        This function parses the output.date and returns true if this date is after the ref date
        """
        nexus_date = self.date
        nexus_date_acquistion = nexus_date.split("T")[0]
        return nexus_date_acquistion > NEW_GEOMETRY_DATE
