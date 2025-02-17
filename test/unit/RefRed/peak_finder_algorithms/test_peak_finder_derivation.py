import pytest

from RefRed.file_loading_utility import loadCsvFile
from RefRed.peak_finder_algorithms.peak_finder_derivation import PeakFinderDerivation


class TestPeakFinderDerivation(object):
    def test_get5HighestPoints_xdata(self, data_server):
        """Step2 - 5highest points: using run 125682 to check calculation of 5 highest points - xdata"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        [high_x, _] = peakfinder1.get5HighestPoints()
        high_x = high_x.tolist()
        assert high_x == pytest.approx([155.0, 156.0, 154.0, 157.0, 153.0])

    def test_get5HighestPoints_ydata(self, data_server):
        """Step2 - 5highest points: using run 125682 to check calculation of 5 highest points - ydata"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        [_, high_y] = peakfinder1.get5HighestPoints()
        high_y = high_y.tolist()
        assert high_y == pytest.approx([32351.0, 28999.0, 19351.0, 9503.0, 2796.0])

    def test_calculatePeakPixel_sumPeakCounts(self, data_server):
        """Step3 - calculate peak pixel using run 125682 to check calculation of 5 highest points - sum_xdata"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        sum_five_highest_xdata = peakfinder1.getSumPeakCounts()
        assert sum_five_highest_xdata == pytest.approx(93000.0)

    def test_calcuatePeakPixel_sumPeakCountTimePixel(self, data_server):
        """Step3 - calculate peak pixel using run 125682 to check calculation of 5 highest points - sum_ydata"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        sum_five_highest_ydata = peakfinder1.getSumPeakCountsTimePixel()
        assert sum_five_highest_ydata == pytest.approx(14438061.0)

    def test_calculatePeakPixel_peakPixelValue(self, data_server):
        """Step3 - calculate peak pixel value using run 125682"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        peak_pixel = peakfinder1.getPeakPixel()
        assert peak_pixel == pytest.approx(155.0)

    def test_calculatefirstderivative_xaxis(self, data_server):
        """Step4 - derivative: testing the first derivative calculation - axis x"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        [xdata_first, _] = peakfinder.getFirstDerivative()
        xdata10 = xdata_first[0:10]
        assert xdata10 == pytest.approx([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])

    def test_calculatefirstderivative_yaxis(self, data_server):
        """Step4 - derivative: testing the first derivative calculation - axis y"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        [_, ydata_first] = peakfinder.getFirstDerivative()
        ydata10 = ydata_first[0:10]
        assert ydata10 == pytest.approx([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 1.0, -1.0])

    def test_calculateMinMaxDervativePixels_minValue(self, data_server):
        """Step5 - calculate min derivative counts value"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        min_derivative_value = peakfinder.getMinDerivativeValue()
        assert min_derivative_value == pytest.approx(-19496.0)

    def test_calculateMinMaxDervativePixels_maxValue(self, data_server):
        """Step5 - calculate max derivative counts value"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        max_derivative_value = peakfinder.getMaxDerivativeValue()
        assert max_derivative_value == pytest.approx(16555.0)

    def test_calculateMinMaxDervativePixels_minPixelValue(self, data_server):
        """Step5 - calculate pixel of min derivative counts value"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        min_pixel_derivative_value = peakfinder.getMinDerivationPixelValue()
        assert min_pixel_derivative_value == pytest.approx(153.5)

    def test_calculateMinMaxDervativePixels_maxPixelValue(self, data_server):
        """Step5 - calculate pixel of max derivative counts value"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        max_pixel_derivative_value = peakfinder.getMaxDerivationPixelValue()
        assert max_pixel_derivative_value == pytest.approx(156.5)

    def test_calculateAvgAndStdDerivation_mean_counts_firstderi(self, data_server):
        """Step6 - calculate average of first derivation counts"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        mean_counts_firstderi = peakfinder.getAverageOfFirstDerivationCounts()
        assert mean_counts_firstderi == pytest.approx(0)

    def test_calculateAvgAndStdDerivation_std_deviation_counts_firstderi(self, data_server):
        """Step6 - calculate standard deviation of first derivation counts"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder = PeakFinderDerivation(xdata, ydata, edata)
        std_deviation_counts_firstderi = peakfinder.getStdDeviationOfFirstDerivationCounts()
        assert std_deviation_counts_firstderi == pytest.approx(1741.838, abs=0.001)

    def test_case_easy_data_set(self, data_server):
        """Step7 - calculate final peak range using run 125682 (easy data set)"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("easy_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        peaks = peakfinder1.getPeaks()
        assert peaks == pytest.approx([151, 159])

    def test_case_medium_data_set(self, data_server):
        """Step7 - calculate final peak range using run 124211 (medium data set)"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("medium_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        peaks = peakfinder1.getPeaks()
        assert peaks == pytest.approx([151, 159])

    def test_case_hard_data_set(self, data_server):
        """Step7 - calculate final peak range using run 124135 (hard data set)"""
        [xdata, ydata, edata] = loadCsvFile(data_server.path_to("hard_data_set.csv"))
        peakfinder1 = PeakFinderDerivation(xdata, ydata, edata)
        peaks = peakfinder1.getPeaks()
        assert peaks == pytest.approx([145, 167], abs=0.001)


if __name__ == "__main__":
    pytest.main([__file__])
