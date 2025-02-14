import math

import numpy as np


class PeakFinderDerivation(object):
    peaks = [-1, -1]
    xdata_firstderi = []
    ydata_firstderi = []
    edata_firstderi = []
    five_highest_ydata = []
    five_highest_xdata = []
    sum_peak_counts = -1
    sum_peak_counts_time_pixel = -1
    peak_pixel = -1
    deri_min = 1
    deri_max = -1
    deri_min_pixel_value = -1
    deri_max_pixel_value = -1
    mean_counts_firstderi = -1
    std_deviation_counts_firstderi = -1
    peak_max_final_value = -1
    peak_min_final_value = -1

    def __init__(self, xdata, ydata, edata=[], back_offset=3):
        self.initArrays()

        self.xdata = np.array(xdata)
        self.ydata = np.array(ydata)
        self.edata = np.array(edata)

        self.calculate5HighestPoints()  # step2
        self.calculatePeakPixel()  # step3

        self.calculateFirstDerivative()  # step4
        self.calculateMinMaxDerivativePixels()  # step5
        self.calculateAvgAndStdDerivative()  # step6
        self.calculateMinMaxSignalPixel()  # step7

    def initArrays(self):
        self.xdata_firstderi = []
        self.ydata_firstderi = []
        self.edata_firstderi = []
        self.peaks = [-1, -1]
        self.five_highest_ydata = []
        self.five_highest_xdata = []
        self.sum_five_highest_ydata = -1
        self.peak_pixel = -1
        self.deri_min = 1
        self.deri_max = -1
        self.deri_min_pixel_value = -1
        self.deri_max_pixel_value = -1
        self.mean_counts_firstderi = -1
        self.std_deviation_counts_firstderi = -1
        self.peak_max_final_value = -1
        self.peak_min_final_value = -1

    def calculate5HighestPoints(self):
        _xdata = self.xdata
        _ydata = self.ydata

        _sort_ydata = np.sort(_ydata)
        _decreasing_sort_ydata = _sort_ydata[::-1]
        self.five_highest_ydata = _decreasing_sort_ydata[0:5]

        _sort_index = np.argsort(_ydata)
        _decreasing_sort_index = _sort_index[::-1]
        _5decreasing_sort_index = _decreasing_sort_index[0:5]
        self.five_highest_xdata = _xdata[_5decreasing_sort_index]

    def calculatePeakPixel(self):
        self.sum_peak_counts = sum(self.five_highest_ydata)
        _sum_peak_counts_time_pixel = -1
        for index, yvalue in enumerate(self.five_highest_ydata):
            _sum_peak_counts_time_pixel += yvalue * self.five_highest_xdata[index]
        self.sum_peak_counts_time_pixel = _sum_peak_counts_time_pixel
        self.peak_pixel = round(self.sum_peak_counts_time_pixel / self.sum_peak_counts)

    def calculateFirstDerivative(self):
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

    def calculateMinMaxDerivativePixels(self):
        _pixel = self.xdata_firstderi
        _counts_firstderi = self.ydata_firstderi

        _sort_counts_firstderi = np.sort(_counts_firstderi)
        self.deri_min = _sort_counts_firstderi[0]
        self.deri_max = _sort_counts_firstderi[-1]

        _sort_index = np.argsort(_counts_firstderi)
        self.deri_min_pixel_value = min([_pixel[_sort_index[0]], _pixel[_sort_index[-1]]])
        self.deri_max_pixel_value = max([_pixel[_sort_index[0]], _pixel[_sort_index[-1]]])

    def calculateAvgAndStdDerivative(self):
        _counts_firstderi = np.array(self.ydata_firstderi)
        self.mean_counts_firstderi = np.mean(_counts_firstderi)
        _mean_counts_firstderi = np.mean(_counts_firstderi * _counts_firstderi)
        self.std_deviation_counts_firstderi = math.sqrt(_mean_counts_firstderi)

    def calculateMinMaxSignalPixel(self):
        _counts = self.ydata_firstderi
        _pixel = self.xdata_firstderi

        _deri_min_pixel_value = self.deri_min_pixel_value
        _deri_max_pixel_value = self.deri_max_pixel_value

        _std_deviation_counts_firstderi = self.std_deviation_counts_firstderi

        px_offset = 0
        while abs(_counts[int(_deri_min_pixel_value - px_offset)]) > _std_deviation_counts_firstderi:
            px_offset += 1
        _peak_min_final_value = _pixel[int(_deri_min_pixel_value - px_offset)]

        px_offset = 0
        while abs(_counts[int(round(_deri_max_pixel_value + px_offset))]) > _std_deviation_counts_firstderi:
            px_offset += 1
        _peak_max_final_value = _pixel[int(round(_deri_max_pixel_value + px_offset))]

        self.peaks = [int(_peak_min_final_value), int(np.ceil(_peak_max_final_value))]

    # getters

    def getAverageOfFirstDerivationCounts(self):
        return self.mean_counts_firstderi

    def getStdDeviationOfFirstDerivationCounts(self):
        return self.std_deviation_counts_firstderi

    def getMinDerivativeValue(self):
        return self.deri_min

    def getMaxDerivativeValue(self):
        return self.deri_max

    def getMinDerivationPixelValue(self):
        return self.deri_min_pixel_value

    def getMaxDerivationPixelValue(self):
        return self.deri_max_pixel_value

    def getPeakPixel(self):
        return self.peak_pixel

    def getSumPeakCounts(self):
        return self.sum_peak_counts

    def getSumPeakCountsTimePixel(self):
        return self.sum_peak_counts_time_pixel

    def get5HighestPoints(self):
        return [self.five_highest_xdata, self.five_highest_ydata]

    def getFirstDerivative(self):
        return [self.xdata_firstderi, self.ydata_firstderi]

    def getPeaks(self):
        return self.peaks


if __name__ == "__main__":
    from file_loading_utility import loadCsvFile

    [xdata, ydata, edata] = loadCsvFile("easy_data_set.csv")
    peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
    [high_x, high_y] = peakfinder1.get5HighestPoints()
