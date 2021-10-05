"""
    Notes from review: This class does a subset of what is done in calculations.lr_data.
    This code is probably not needed.
"""
from mantid.simpleapi import Rebin
import numpy as np
import logging
import math
import os

from RefRed.peak_finder_algorithms.peak_finder_derivation import PeakFinderDerivation
from RefRed.plot.all_plot_axis import AllPlotAxis

NEUTRON_MASS = 1.675e-27  # kg
PLANCK_CONSTANT = 6.626e-34  # m^2 kg s^-1
H_OVER_M_NEUTRON = PLANCK_CONSTANT / NEUTRON_MASS


class LRData(object):
    tof_range = None
    low_res = ['0', '255']
    low_res_flag = True
    is_better_chopper_coverage = True

    def __init__(self, workspace, read_options):
        self.workspace = workspace
        self.read_options = read_options
        mt_run = self.workspace.getRun()

        self.run_number = mt_run.getProperty('run_number').value

        self.lambda_requested = float(mt_run.getProperty('LambdaRequest').value[0])
        self.lambda_requested_units = mt_run.getProperty('LambdaRequest').units
        self.thi = mt_run.getProperty('thi').value[0]
        self.thi_units = mt_run.getProperty('thi').units
        self.tthd = mt_run.getProperty('tthd').value[0]
        self.tthd_units = mt_run.getProperty('tthd').units
        self.S1W = mt_run.getProperty('S1HWidth').value[0]
        self.S1H = mt_run.getProperty('S1VHeight').value[0]

        try:
            self.SiW = mt_run.getProperty('SiHWidth').value[0]
            self.SiH = mt_run.getProperty('SiVHeight').value[0]
            self.isSiThere = True
        except:
            self.S2W = mt_run.getProperty('S2HWidth').value[0]
            self.S2H = mt_run.getProperty('S2VHeight').value[0]

        self.attenuatorNbr = mt_run.getProperty('vATT').value[0] - 1
        self.date = mt_run.getProperty('run_start').value
        self.full_file_name = mt_run.getProperty('Filename').value[0]
        self.filename = os.path.basename(self.full_file_name)

        sample = self.workspace.getInstrument().getSample()
        source = self.workspace.getInstrument().getSource()
        self.dMS = sample.getDistance(source)

        # create array of distances pixel->sample
        self.number_x_pixels = int(self.workspace.getInstrument().getNumberParameter("number-of-x-pixels")[0])  # 256
        self.number_y_pixels = int(self.workspace.getInstrument().getNumberParameter("number-of-y-pixels")[0])

        dPS_array = np.zeros((self.number_x_pixels, self.number_y_pixels))
        for x in range(self.number_y_pixels):
            for y in range(self.number_x_pixels):
                _index = self.number_x_pixels * x + y
                detector = self.workspace.getDetector(_index)
                dPS_array[y][x] = sample.getDistance(detector)

        # distance sample->center of detector
        self.dSD = dPS_array[int(self.number_x_pixels / 2), int(self.number_y_pixels / 2)]
        # distance source->center of detector
        self.dMD = self.dSD + self.dMS

        # calculate theta
        self.theta = self.calculate_theta()
        self.frequency = float(mt_run.getProperty('Speed1').value[0])

        tof_coeff_large = 1.7 * 60 / self.frequency
        tmax = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + tof_coeff_large) * 1e-4
        tmin = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested - tof_coeff_large) * 1e-4

        if self.read_options['is_auto_tof_finder'] or self.tof_range == None:
            autotmin = tmin
            autotmax = tmax
        else:
            autotmin = np.float(self.tof_range[0])
            autotmax = np.float(self.tof_range[1])

        self.tof_range_auto = [autotmin, autotmax]  # microS
        self.tof_range_auto_with_margin = [tmin, tmax]  # microS
        self.tof_range = [autotmin, autotmax]  # for the first time, initialize tof_range like auto (microS)
        self.binning = [tmin, self.read_options['bins'], tmax]
        self.calculate_lambda_range()
        self.q_range = self.calculate_q_range()
        self.incident_angle = self.calculate_theta(False)

        # Proton charge
        _proton_charge = float(mt_run.getProperty('gd_prtn_chrg').value)
        _proton_charge_units = mt_run.getProperty('gd_prtn_chrg').units
        new_proton_charge_units = 'mC'

        self.proton_charge = _proton_charge * 3.6  # to go from microA/h to mC
        self.proton_charge_units = new_proton_charge_units

        self.peak = [0, 0]
        self.back = [0, 0]
        self.back_flag = True
        self.all_plot_axis = AllPlotAxis
        self.tof_auto_flag = True
        self.new_detector_geometry_flag = True
        self.data_loaded = False
        self.read_data()

        if self.read_options['is_auto_peak_finder']:
            pf = PeakFinderDerivation(list(range(len(self.ycountsdata))), self.ycountsdata)
            [peak1, peak2] = pf.getPeaks()
            self.peak = [str(peak1), str(peak2)]

            backOffsetFromPeak = self.read_options['back_offset_from_peak']
            back1 = int(peak1 - backOffsetFromPeak)
            back2 = int(peak2 + backOffsetFromPeak)
            self.back = [str(back1), str(back2)]

    ################## Properties for easy data access ##########################
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
        '''
        calculate q range
        '''
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
        '''
        calculate lambda range
        '''
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
        '''
        calculate theta
        '''
        tthd_value = self.tthd
        tthd_units = self.tthd_units
        thi_value = self.thi
        thi_units = self.thi_units

        # Make sure we have radians
        if thi_units == 'degree':
            thi_value *= math.pi / 180.0
        if tthd_units == 'degree':
            tthd_value *= math.pi / 180.0

        theta = math.fabs(tthd_value - thi_value) / 2.0
        if theta < 0.001:
            logging.debug("thi and tthd are equal: is this a direct beam?")

        # Add the offset
        angle_offset = 0.0
        if with_offset and "angle_offset" in self.read_options:
            angle_offset = float(self.read_options['angle_offset'])
        angle_offset_deg = angle_offset
        return theta + angle_offset_deg * math.pi / 180.0

    def getIxyt(self, nxs_histo):
        '''
        will format the histogrma NeXus to retrieve the full 3D data set
        '''
        _tof_axis = nxs_histo.readX(0)[:].copy()
        nbr_tof = len(_tof_axis)

        _y_axis = np.zeros((self.number_x_pixels, self.number_y_pixels, nbr_tof - 1))
        _y_error_axis = np.zeros((self.number_x_pixels, self.number_y_pixels, nbr_tof - 1))

        x_range = list(range(self.number_x_pixels))
        y_range = list(range(self.number_y_pixels))

        for x in x_range:
            for y in y_range:
                _index = int(self.number_y_pixels * x + y)
                _tmp_data = nxs_histo.readY(_index)[:]
                _y_axis[x, y, :] = _tmp_data
                _tmp_error = nxs_histo.readE(_index)[:]
                _y_error_axis[x, y, :] = _tmp_error

        return [_tof_axis, _y_axis, _y_error_axis]

    def read_data(self):
        nxs_histo = Rebin(InputWorkspace=self.workspace, Params=self.binning, PreserveEvents=True)
        # retrieve 3D array
        [_tof_axis, Ixyt, Exyt] = self.getIxyt(nxs_histo)
        self.tof_axis_auto_with_margin = _tof_axis

        # # keep only the low resolution range requested
        from_pixel = 0
        to_pixel = self.number_x_pixels - 1

        # keep only low resolution range defined
        Ixyt = Ixyt[from_pixel:to_pixel, :, :]
        Exyt = Exyt[from_pixel:to_pixel, :, :]

        self.Ixyt = Ixyt
        self.Exyt = Exyt

        # create projections for the 2D datasets
        Ixy = Ixyt.sum(axis=2)
        Iyt = Ixyt.sum(axis=0)
        Iit = Iyt.sum(axis=0)
        Iix = Ixy.sum(axis=1)
        Iyi = Iyt.sum(axis=1)

        self.data = Ixyt.astype(float)  # 3D dataset
        self.xydata = Ixy.transpose().astype(float)  # 2D dataset
        self.ytofdata = Iyt.astype(float)  # 2D dataset

        self.countstofdata = Iit.astype(float)
        self.countsxdata = Iix.astype(float)
        self.ycountsdata = Iyi.astype(float)

        self.data_loaded = True
