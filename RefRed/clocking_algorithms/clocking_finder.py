import numpy as np
import math


class ClockingAlgorithm(object):

    clocking_left = -1
    clocking_right = -1

    xdata_firstderi = []
    ydata_firstderi = []
    edata_firstderi = []
    peak_pixel = -1
    deri_min = 1
    deri_max = -1
    deri_min_pixel_value = -1
    deri_max_pixel_value = -1
    mean_counts_firstderi = -1
    std_deviation_counts_firstderi = -1

    def __init__(self, xdata=None, ydata=None, edata=None):
        self.initArrays()

        self.xdata = np.array(xdata)
        self.ydata = np.array(ydata)
        self.edata = np.array(edata)

        self.calculate_first_derivative()
        self.calculate_min_max_derivative_pixels()
        self.calculate_avg_and_std_derivative()
        self.calculate_main_central_peak_region()

    def initArrays(self):
        self.xdata_firstderi = []
        self.ydata_firstderi = []
        self.edata_firstderi = []
        self.clocking = [-1, -1]
        self.deri_min = 1
        self.deri_max = -1
        self.deri_min_pixel_value = -1
        self.deri_max_pixel_value = -1
        self.mean_counts_firstderi = -1
        self.std_deviation_counts_firstderi = -1

    def calculate_first_derivative(self):
        xdata = self.xdata
        ydata = self.ydata

        _xdata_firstderi = []
        _ydata_firstderi = []
        for i in range(len(xdata) - 1):
            _left_x = xdata[i]
            _right_x = xdata[i + 1]
            _xdata_firstderi.append(np.mean([_left_x, _right_x]))

            _left_y = ydata[i]
            _right_y = ydata[i + 1]
            _ydata_firstderi.append((_right_y - _left_y) / (_right_x - _left_x))

        self.xdata_firstderi = _xdata_firstderi
        self.ydata_firstderi = _ydata_firstderi

    def calculate_min_max_derivative_pixels(self):
        _pixel = self.xdata_firstderi
        _counts_firstderi = self.ydata_firstderi

        _sort_counts_firstderi = np.sort(_counts_firstderi)
        self.deri_min = _sort_counts_firstderi[0]
        self.deri_max = _sort_counts_firstderi[-1]

        _sort_index = np.argsort(_counts_firstderi)
        self.deri_min_pixel_value = min([_pixel[_sort_index[0]], _pixel[_sort_index[-1]]])
        self.deri_max_pixel_value = max([_pixel[_sort_index[0]], _pixel[_sort_index[-1]]])

    def calculate_avg_and_std_derivative(self):
        _counts_firstderi = np.array(self.ydata_firstderi)
        self.mean_counts_firstderi = np.mean(_counts_firstderi)
        _mean_counts_firstderi = np.mean(_counts_firstderi * _counts_firstderi)
        self.std_deviation_counts_firstderi = math.sqrt(_mean_counts_firstderi)

    def calculate_main_central_peak_region(self):
        _counts = self.ydata_firstderi
        _pixel = self.xdata_firstderi

        _std_deviation_counts_firstderi = self.std_deviation_counts_firstderi

        # starting from left
        px_offset = 0
        while abs(_counts[int(px_offset)]) < _std_deviation_counts_firstderi:
            px_offset += 1
        _tmp_value = _pixel[int(px_offset)]
        _peak_min_final_value = _tmp_value if _tmp_value > 5 else 5

        px_offset = len(_counts) - 1
        while abs(_counts[int(round(px_offset))]) < _std_deviation_counts_firstderi:
            px_offset -= 1
        _tmp_value = _pixel[int(round(px_offset))]
        _peak_max_final_value = _tmp_value if _tmp_value < 250 else 250

        self.clocking = [int(_peak_min_final_value), int(np.ceil(_peak_max_final_value))]


class ClockingFinder(object):
    clocking = [-1, -1]

    def __init__(self, parent=None, xdata=None, ydata=None, edata=None):
        self.clocking = [-1, -1]
        self.parent = parent
        # make 121 and 197 the default pixel choices for the clocking correction, pending development
        # of a better peak-finding algorithm
        self.clocking = self.parent.gui_metadata['clocking_pixel']
        return

        o_clocking_algo = ClockingAlgorithm(xdata=xdata, ydata=ydata, edata=edata)
        [left_max, right_min] = o_clocking_algo.clocking

        left_xdata = xdata[0:left_max]
        left_ydata = ydata[0:left_max]
        o_clocking_left = ClockingAlgorithm(xdata=left_xdata, ydata=left_ydata)
        left_clocking = o_clocking_left.clocking[0]

        right_xdata = xdata[right_min:-1]
        right_ydata = ydata[right_min:-1]
        o_clocking_right = ClockingAlgorithm(xdata=right_xdata, ydata=right_ydata)
        right_clocking = o_clocking_right.clocking[1]

        self.clocking = [left_clocking, right_clocking]
