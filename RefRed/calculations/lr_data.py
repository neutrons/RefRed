import numpy as np
import logging
import math
import os
import gc

from mantid.simpleapi import *
from RefRed.peak_finder_algorithms.peak_finder_derivation import PeakFinderDerivation
from RefRed.low_res_finder_algorithms.low_res_finder import LowResFinder
from RefRed.clocking_algorithms.clocking_finder import ClockingFinder
import RefRed.constants as constants
from RefRed.plot.all_plot_axis import AllPlotAxis
from RefRed.utilities import convert_angle


NEUTRON_MASS = 1.675e-27  # kg
PLANCK_CONSTANT = 6.626e-34  # m^2 kg s^-1
H_OVER_M_NEUTRON = PLANCK_CONSTANT / NEUTRON_MASS

class LRData(object):

    read_options = dict(is_auto_tof_finder = True,
                        is_auto_peak_finder = True,
                        back_offset_from_peak = 3,
                        bins = 50,
                        angle_offset = 0.001)

    tof_range = None
    tof_range_manual = None
    tof_range_auto = None
    tof_range_auto_flag = True
    tof_range_auto_with_margin = []

    low_res = ['0', '255']
    low_res_flag = True 
    use_it_flag = True
    full_file_name = ['']
    filename = ''
    ipts = 'N/A'
    
    def __init__(self, workspace, lconfig=None, is_data=True):
        
        self._tof_axis = []
        self.Ixyt = []
        self.Exyt= []
        
        self.data = []
        self.xydata = []
        self.ytofdata = []

        self.countstofdata = []
        self.countxdata = []
        self.ycountsdata = []
        
        self.workspace = mtd[workspace]
        self.workspace_name = workspace

        mt_run = self.workspace.getRun()

        self.ipts = mt_run.getProperty('experiment_identifier').value
        self.run_number = mt_run.getProperty('run_number').value
        self.lambda_requested = float(mt_run.getProperty('LambdaRequest').value[0])
        self.lambda_requested_units = mt_run.getProperty('LambdaRequest').units
        self.thi = mt_run.getProperty('thi').value[0]
        self.thi_units = mt_run.getProperty('thi').units
        self.ths = mt_run.getProperty('ths').value[0]
        self.ths_units = mt_run.getProperty('ths').units
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
            self.isSiThere = False

        self.attenuatorNbr = mt_run.getProperty('vATT').value[0] - 1
        self.date = mt_run.getProperty('run_start').value
        
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
                dPS_array[y, x] = sample.getDistance(detector)

        # distance sample->center of detector
        self.dSD = dPS_array[self.number_x_pixels / 2, self.number_y_pixels / 2]
        # distance source->center of detector
        self.dMD = self.dSD + self.dMS

        # calculate theta
        self.theta = self.calculate_theta()
        self.frequency = float(mt_run.getProperty('Speed1').value[0])

        tof_coeff_narrow = 1.7 * 60 / self.frequency
        tof_coeff_large = 2.5 * 60 / self.frequency
        tof_coeff = 0.5 * 60 / self.frequency

        if lconfig is not None:
            autotmin = np.float(lconfig.tof_range[0])
            autotmax = np.float(lconfig.tof_range[1])
        else:
            autotmin = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + tof_coeff - tof_coeff_narrow) * 1e-4
            autotmax = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + tof_coeff + \
                                                      tof_coeff_narrow) * 1e-4

        # automatically calcualte the TOF range for display
        tmax = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + tof_coeff + tof_coeff_large) * 1e-4
        tmin = self.dMD / H_OVER_M_NEUTRON * (self.lambda_requested + tof_coeff - tof_coeff_large) * 1e-4

        if tmin < 0:
            tmin = 0

        self.tof_range_auto = [autotmin, autotmax]  # microS
        self.tof_range_auto_with_margin = [tmin, tmax]  # microS
        
        # manual tof range (if user wants to use a manual time range)
        self.tof_range = [autotmin, autotmax]  # for the first time, initialize tof_range like auto (microS)
        self.tof_range_manual = [autotmin, autotmax]

        self.binning = [tmin, self.read_options['bins'], tmax]
        self.calculate_lambda_range()
        self.incident_angle = 2.*self.calculate_theta(with_offset = False) # 2.theta
        self.calculate_q_range()
        # self.lambda_range = self.calculate_lambda_range()

        # Proton charge
        _proton_charge = float(mt_run.getProperty('gd_prtn_chrg').value)
        _proton_charge_units = mt_run.getProperty('gd_prtn_chrg').units
        new_proton_charge_units = 'mC'

        self.proton_charge = _proton_charge * 3.6  # to go from microA/h to mC
        self.proton_charge_units = new_proton_charge_units

        self.peak = [0, 0]
        self.back = [0, 0]
        self.clocking = [0, 0]
        self.back_flag = True
        self.all_plot_axis = AllPlotAxis()
        self.tof_auto_flag = True
        self.new_detector_geometry_flag = self.is_nexus_taken_after_refDate()
        self.data_loaded = False
        self.read_data()

        if lconfig is None:
            
            pf = PeakFinderDerivation(range(len(self.ycountsdata)), self.ycountsdata)
            [peak1, peak2] = pf.getPeaks()
            self.peak = [str(peak1), str(peak2)]

            backOffsetFromPeak = self.read_options['back_offset_from_peak']
            back1 = int(peak1 - backOffsetFromPeak)
            back2 = int(peak2 + backOffsetFromPeak)
            self.back = [str(back1), str(back2)]

            lw_pf = LowResFinder(range(len(self.countsxdata)), self.countsxdata)
            [lowres1, lowres2] = lw_pf.get_low_res()
            self.low_res = [str(lowres1), str(lowres2)]
            
            clocking_pf = ClockingFinder(range(len(self.ycountsdata)), self.ycountsdata)
            [clocking1, clocking2] = clocking_pf.clocking
            
            clock_array = [clocking1, clocking2]
            clock_array.sort()

            self.clocking  = [str(clocking1), str(clocking2)]

        else:
            
            # if we loaded a config that does not have the clocking info, we will have to retrieve once
            # everything has been loaded (before display)
            if lconfig.data_clocking[0] != '':
                self.clocking = [np.float(lconfig.data_clocking[0]), np.float(lconfig.data_clocking[1])]
            else:
                clocking_pf = LowResFinder(range(len(self.ycountsdata)), self.ycountsdata)
                [clocking1, clocking2] = clocking_pf.get_low_res()
                self.clocking  = [str(clocking1), str(clocking2)]
                
            self.tof_auto_flag = np.bool(lconfig.tof_auto_flag)

            if is_data:
                self.peak = [np.int(lconfig.data_peak[0]), np.int(lconfig.data_peak[1])]
                self.back = [np.int(lconfig.data_back[0]), np.int(lconfig.data_back[1])]
                self.low_res = [np.int(lconfig.data_low_res[0]), np.int(lconfig.data_low_res[1])] 
                self.low_res_flag = np.bool(lconfig.data_low_res_flag)
                self.back_flag = np.bool(lconfig.data_back_flag)
            else:
                self.peak = [np.int(lconfig.norm_peak[0]), np.int(lconfig.norm_peak[1])]
                self.back = [np.int(lconfig.norm_back[0]), np.int(lconfig.norm_back[1])]
                self.low_res = [np.int(lconfig.norm_low_res[0]), np.int(lconfig.norm_low_res[1])] 
                self.low_res_flag = np.bool(lconfig.norm_low_res_flag)
                self.back_flag = np.bool(lconfig.norm_back_flag)


    ################## Properties for easy data access ##########################
    # return the size of the data stored in memory for this dataset
    @property
    def nbytes(self): return (len(self._data_zipped) + 
                              self.xydata.nbytes + self.xtofdata.nbytes)
    @property
    def rawbytes(self): return (self.data.nbytes + self.xydata.nbytes + self.xtofdata.nbytes)

    USE_COMPRESSION = False
    if USE_COMPRESSION:
        @property
        def nbytes(self): return (len(self._data_zipped) + 
                                  self.xydata.nbytes + self.xtofdata.nbytes)
    else:
        nbytes = rawbytes

    @property
    def xdata(self): return self.xydata.mean(axis=0)

    @property
    def ydata(self): return self.xydata.mean(axis=1)

    @property
    def tofdata(self): return self.xtofdata.mean(axis=0)

    # coordinates corresponding to the data items
    @property
    def x(self): return np.arange(self.xydata.shape[1])

    @property
    def y(self): return np.arange(self.xydata.shape[0])

    @property
    def xy(self): return np.meshgrid(self.x, self.y)

    @property
    def tof(self): return (self.tof_edges[:-1] + self.tof_edges[1:]) / 2.

    @property
    def xtof(self): return np.meshgrid(self.tof, self.x)

    @property
    def lamda(self):
        v_n = self.dist_mod_det / self.tof * 1e6  # m/s
        lamda_n = H_OVER_M_NEUTRON / v_n * 1e10  # A
        return lamda_n

    def calculate_q_range(self):
        '''
        calculate q range
        '''
        [lambda_min, lambda_max] = self.lambda_range        
        _const = float(4) * math.pi
        theta_rad = convert_angle(angle = self.incident_angle)
        
        _const_theta = _const * math.sin(float(theta_rad)/2.)
        q_min = _const_theta / float(lambda_max)
        q_max = _const_theta / float(lambda_min)
        
        self.q_range = [q_min, q_max]
              
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

    def calculate_theta(self, with_offset = True):
        '''
        calculate theta
        '''
        tthd_value = self.tthd
        tthd_units = self.tthd_units
        thi_value = self.thi
        thi_units = self.thi_units

        # Make sure we have radians
        #if thi_units == 'degree':
        #    thi_value *= math.pi / 180.0
        #if tthd_units == 'degree':
        #    tthd_value *= math.pi / 180.0

        theta = math.fabs(tthd_value - thi_value) / 2.
        if theta < 0.001:
            logging.warning("thi and tthd are equal: is this a direct beam?")

        # Add the offset
        angle_offset = 0.0
        if with_offset and "angle_offset" in self.read_options:
            angle_offset = float(self.read_options['angle_offset'])
            angle_offset_deg = angle_offset
            theta = theta + angle_offset_deg * math.pi / 180.0
            
        return theta

    def getIxyt(self, nxs_histo):
        '''
        will format the histogrma NeXus to retrieve the full 3D data set
        '''
        self._tof_axis = nxs_histo.readX(0)[:].copy()
        nbr_tof = len(self._tof_axis)

        Ixyt = np.zeros((self.number_x_pixels, self.number_y_pixels, nbr_tof - 1))
        Exyt = np.zeros((self.number_x_pixels, self.number_y_pixels, nbr_tof - 1))

        x_range = range(self.number_x_pixels)
        y_range = range(self.number_y_pixels)

        for x in x_range:
            for y in y_range:
                _index = int(self.number_y_pixels * x + y)
                Ixyt[x, y, :] = nxs_histo.readY(_index)[:].copy()
                Exyt[x, y, :] = nxs_histo.readE(_index)[:].copy()
        gc.collect()
        self.Ixyt = Ixyt
        self.Exyt = Exyt

    def read_data(self):
        output_workspace_name = self.workspace_name + '_rebin'
        nxs_histo = Rebin(InputWorkspace = self.workspace, 
                          OutputWorkspace = output_workspace_name,
                          Params = self.binning, 
                          PreserveEvents = True)
        # retrieve 3D array
        nxs_histo = mtd[output_workspace_name]
        #[_tof_axis, Ixyt, Exyt] = self.getIxyt(nxs_histo)
        self.getIxyt(nxs_histo)
        self.tof_axis_auto_with_margin = self._tof_axis

        # # keep only the low resolution range requested
        from_pixel = 0
        to_pixel = self.number_x_pixels-1

        # keep only low resolution range defined
        self.Ixyt = self.Ixyt[from_pixel:to_pixel, :, :]
        self.Exyt = self.Exyt[from_pixel:to_pixel, :, :]

        # create projections for the 2D datasets
        Ixy = self.Ixyt.sum(axis=2)
        Iyt = self.Ixyt.sum(axis=0)
        Iit = Iyt.sum(axis=0)
        Iix = Ixy.sum(axis=1)
        Iyi = Iyt.sum(axis=1)

        self.xydata = Ixy.transpose().astype(float)  # 2D dataset
        self.ytofdata = Iyt.astype(float)  # 2D dataset

        self.countstofdata = Iit.astype(float)
        self.countsxdata = Iix.astype(float)
        self.ycountsdata = Iyi.astype(float)
        
        self.data_loaded = True

    def is_nexus_taken_after_refDate(self):
        '''
        This function parses the output.date and returns true if this date is after the ref date
        '''
        ref_date = constants.new_geometry_detector_date
        nexus_date = self.date
        nexus_date_acquistion = nexus_date.split('T')[0]

        if nexus_date_acquistion > ref_date:
            return True
        else:
            return False

