"""
Notes from review: This class does a subset of what is done in calculations.lr_data.
This code is probably not needed.
"""

import logging
import math
import os

import numpy as np
from mantid.simpleapi import Rebin

from RefRed.peak_finder_algorithms.peak_finder_derivation import PeakFinderDerivation
from RefRed.plot.all_plot_axis import AllPlotAxis

NEUTRON_MASS = 1.675e-27  # kg
PLANCK_CONSTANT = 6.626e-34  # m^2 kg s^-1
H_OVER_M_NEUTRON = PLANCK_CONSTANT / NEUTRON_MASS


class LRData(object):
    tof_range = None
    low_res = ["0", "255"]
    low_res_flag = True
    is_better_chopper_coverage = True

    def __init__(self, workspace, read_options):
        self.workspace = workspace  # retain the pointer for 3rd party calls
        self.read_options = read_options
        mt_run = workspace.getRun()

        self.run_number = mt_run.getProperty("run_number").value

        self.lambda_requested = float(mt_run.getProperty("LambdaRequest").value[0])
        self.lambda_requested_units = mt_run.getProperty("LambdaRequest").units
        self.thi = mt_run.getProperty("thi").value[0]
        self.thi_units = mt_run.getProperty("thi").units
        self.tthd = mt_run.getProperty("tthd").value[0]
        self.tthd_units = mt_run.getProperty("tthd").units
        self.S1W = mt_run.getProperty("S1HWidth").value[0]
        self.S1H = mt_run.getProperty("S1VHeight").value[0]

        try:
            self.SiW = mt_run.getProperty("SiHWidth").value[0]
            self.SiH = mt_run.getProperty("SiVHeight").value[0]
            self.isSiThere = True
        except:
            self.S2W = mt_run.getProperty("S2HWidth").value[0]
            self.S2H = mt_run.getProperty("S2VHeight").value[0]

        self.attenuatorNbr = mt_run.getProperty("vATT").value[0] - 1
        self.date = mt_run.getProperty("run_start").value
        self.full_file_name = mt_run.getProperty("Filename").value[0]
        self.filename = os.path.basename(self.full_file_name)

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

        # Calculate the TOF range to select
        if use_emission_delay:
            self.dMD = base_path

        tmax = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + wl_half_width) * 1e-4
        tmin = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested - wl_half_width) * 1e-4

        if use_emission_delay:
            wl_min = self.lambda_requested - wl_half_width
            wl_max = self.lambda_requested + wl_half_width
            tmin -= t_off + t_mult * wl_min
            tmax -= t_off + t_mult * wl_max

        if self.read_options["is_auto_tof_finder"] or self.tof_range is None:
            autotmin = tmin
            autotmax = tmax
        else:
            autotmin = float(self.tof_range[0])
            autotmax = float(self.tof_range[1])

        self.tof_range_auto = [autotmin, autotmax]  # microS
        self.tof_range_auto_with_margin = [tmin, tmax]  # microS
        self.tof_range = [autotmin, autotmax]  # for the first time, initialize tof_range like auto (microS)
        self.binning = [tmin, self.read_options["bins"], tmax]
        self.calculate_lambda_range()
        self.q_range = self.calculate_q_range()
        self.incident_angle = self.calculate_theta(False)

        # Proton charge
        _proton_charge = float(mt_run.getProperty("gd_prtn_chrg").value)
        # _proton_charge_units = mt_run.getProperty('gd_prtn_chrg').units
        new_proton_charge_units = "mC"

        self.proton_charge = _proton_charge * 3.6  # to go from microA/h to mC
        self.proton_charge_units = new_proton_charge_units

        self.peak = [0, 0]
        self.back = [0, 0]
        self.back_flag = True
        self.all_plot_axis = AllPlotAxis
        self.tof_auto_flag = True
        self.new_detector_geometry_flag = True
        self.data_loaded = False
        self._read_data(workspace)

        if self.read_options["is_auto_peak_finder"]:
            pf = PeakFinderDerivation(list(range(len(self.ycountsdata))), self.ycountsdata)
            [peak1, peak2] = pf.getPeaks()
            self.peak = [str(peak1), str(peak2)]

            back_offset_from_peak = self.read_options["back_offset_from_peak"]
            back1 = int(peak1 - back_offset_from_peak)
            back2 = int(peak2 + back_offset_from_peak)
            self.back = [str(back1), str(back2)]

    # Properties for easy data access #
    # return the size of the data stored in memory for this dataset
    @property
    def xdata(self):
        return self.xydata.mean(axis=0)

    @property
    def ydata(self):
        return self.xydata.mean(axis=1)

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
        theta_rad = self.theta
        dMD = self.dMD

        _const = float(4) * math.pi * dMD / H_OVER_M_NEUTRON

        # retrieve tof from GUI
        [tof_min, tof_max] = self.tof_range

        q_min = _const * math.sin(theta_rad) / (float(tof_max) * 1e-6) * float(1e-10)
        q_max = _const * math.sin(theta_rad) / (float(tof_min) * 1e-6) * float(1e-10)

        q_min = "%.5f" % q_min
        q_max = "%.5f" % q_max

        return [q_min, q_max]

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
        tthd_units = self.tthd_units
        thi_value = self.thi
        thi_units = self.thi_units

        # Make sure we have radians
        if thi_units == "degree":
            thi_value *= math.pi / 180.0
        if tthd_units == "degree":
            tthd_value *= math.pi / 180.0

        theta = math.fabs(tthd_value - thi_value) / 2.0
        if theta < 0.001:
            logging.debug("thi and tthd are equal: is this a direct beam?")

        # Add the offset
        angle_offset = 0.0
        if with_offset and "angle_offset" in self.read_options:
            angle_offset = float(self.read_options["angle_offset"])
        angle_offset_deg = angle_offset
        return theta + angle_offset_deg * math.pi / 180.0

    def _get_Ixyt(self, nxs_histo):
        """
        will format the histogrma NeXus to retrieve the full 3D data set
        """
        _tof_axis = nxs_histo.readX(0)[:].copy()
        nbr_tof = len(_tof_axis)

        _y_axis = nxs_histo.extractY().reshape(self.number_x_pixels, self.number_y_pixels, nbr_tof - 1)

        return [_tof_axis, _y_axis]

    def _read_data(self, workspace):
        nxs_histo = Rebin(InputWorkspace=workspace, Params=self.binning, PreserveEvents=True)
        # retrieve 3D array
        [_tof_axis, Ixyt] = self._get_Ixyt(nxs_histo)
        nxs_histo.delete()
        self.tof_axis_auto_with_margin = _tof_axis

        # # keep only the low resolution range requested
        from_pixel = 0
        to_pixel = self.number_x_pixels - 1

        # keep only low resolution range defined
        Ixyt = Ixyt[from_pixel:to_pixel, :, :]

        # create projections for the 2D datasets
        self.xydata = Ixyt.sum(axis=2).transpose()  # 2D dataset
        self.ytofdata = Ixyt.sum(axis=0)  # 2D dataset
        self.ycountsdata = Ixyt.sum(axis=0).sum(axis=1)

        self.data_loaded = True
