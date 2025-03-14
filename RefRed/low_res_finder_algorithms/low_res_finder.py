import math

import numpy as np


class LowResFinder(object):
    low_res = [-1, -1]
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
    peak_max_final_value = -1
    peak_min_final_value = -1
    back_offset = 4

    def __init__(self, xdata=None, ydata=None, edata=None, back_offset=4):
        self.initArrays()

        self.xdata = np.array(xdata)
        self.ydata = np.array(ydata)
        self.edata = np.array(edata)
        self.back_offset = back_offset

        self.calculate_first_derivative()  # step1
        self.calculate_min_max_derivative_pixels()  # step2
        self.calculate_avg_and_std_derivative()  # step3

        self.calculate_low_res_pixel()  # step4

    def initArrays(self):
        self.xdata_firstderi = []
        self.ydata_firstderi = []
        self.edata_firstderi = []
        self.low_res = [-1, -1]
        self.deri_min = 1
        self.deri_max = -1
        self.deri_min_pixel_value = -1
        self.deri_max_pixel_value = -1
        self.mean_counts_firstderi = -1
        self.std_deviation_counts_firstderi = -1
        self.peak_max_final_value = -1
        self.peak_min_final_value = -1

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

    def calculate_low_res_pixel(self):
        _counts = self.ydata_firstderi
        _pixel = self.xdata_firstderi

        _back_offset = self.back_offset
        _std_deviation_counts_firstderi = self.std_deviation_counts_firstderi

        # starting from left
        px_offset = 0
        while abs(_counts[int(px_offset)]) < _std_deviation_counts_firstderi:
            px_offset += 1
        _peak_min_final_value = _pixel[int(px_offset) - _back_offset]

        px_offset = len(_counts) - 1
        while abs(_counts[int(round(px_offset))]) < _std_deviation_counts_firstderi:
            px_offset -= 1
        _peak_max_final_value = _pixel[int(round(px_offset)) + _back_offset]

        self.low_res = [int(_peak_min_final_value), int(np.ceil(_peak_max_final_value))]

    # getters
    def get_average_of_first_derivation_counts(self):
        return self.mean_counts_firstderi

    def get_std_deviation_of_first_derivation_counts(self):
        return self.std_deviation_counts_firstderi

    def get_min_derivative_value(self):
        return self.deri_min

    def get_max_derivative_value(self):
        return self.deri_max

    def get_min_derivation_pixel_value(self):
        return self.deri_min_pixel_value

    def get_max_derivation_pixel_value(self):
        return self.deri_max_pixel_value

    def get_first_derivative(self):
        return [self.xdata_firstderi, self.ydata_firstderi]

    def get_low_res(self):
        return self.low_res


if __name__ == "__main__":
    from RefRed.file_loading_utility import loadCsvFile

    [xdata, ydata, edata] = loadCsvFile("easy_data_set.csv")
    peakfinder1 = LowResFinder(xdata, ydata, edata)
