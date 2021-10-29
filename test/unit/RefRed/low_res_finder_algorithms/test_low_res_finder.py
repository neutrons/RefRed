# package imports
from RefRed.file_loading_utility import loadCsvFile
from RefRed.low_res_finder_algorithms.low_res_finder import LowResFinder

# 3rd party imports
import pytest
import numpy as np


@pytest.fixture(scope="function")
def test_loadcsvfile_easy(data_server):
    '''Step0 - Loading: checking that loadCsvFile works correctly on easy'''
    csvfn = data_server.get_path("easy_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    # x-axis
    xdata10 = xdata[0:10]
    ref_x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    np.testing.assert_array_equal(xdata10, ref_x)
    # y-axis
    ydata10 = ydata[0:10]
    ref_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 12.0])
    np.testing.assert_array_equal(ydata10, ref_y)
    # e-axis
    edata10 = edata[0:10]
    ref_e = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.5])
    np.testing.assert_array_equal(edata10, ref_e)


@pytest.fixture(scope="function")
def test_loadcsvfile_medium(data_server):
    '''Step0 - Loading: checking that loadCsvFile works correctly on medium'''
    csvfn = data_server.get_path("medium_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    # x-axis
    xdata10 = xdata[0:10]
    ref_x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    np.testing.assert_array_equal(xdata10, ref_x)
    # y-axis
    ydata10 = ydata[0:10]
    ref_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 26.0])
    np.testing.assert_array_equal(ydata10, ref_y)
    # e-axis
    edata10 = edata[0:10]
    ref_e = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.6, 5.1])
    np.testing.assert_array_equal(edata10, ref_e)


@pytest.fixture(scope="function")
def test_loadcsvfile_hard(data_server):
    '''Step0 - Loading: checking that loadCsvFile works correctly on hard'''
    csvfn = data_server.get_path("hard_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    # x-axis
    xdata10 = xdata[0:10]
    ref_x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    np.testing.assert_array_equal(xdata10, ref_x)
    # y-axis
    ydata10 = ydata[0:10]
    ref_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 28.0, 18.0])
    np.testing.assert_array_equal(ydata10, ref_y)
    # e-axis
    edata10 = edata[0:10]
    ref_e = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 5.3, 4.2])
    np.testing.assert_array_equal(edata10, ref_e)


@pytest.fixture(scope="function")
def test_calculate_first_derivative_easy(data_server):
    '''Step1 - derivative: testing the first derivative calculation of easy data set'''
    csvfn = data_server.get_path("easy_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    [xdata_first, ydata_first] = peakfinder.get_first_derivative()
    # x-axis
    xdata10 = xdata_first[0:10]
    ref_x = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])
    np.testing.assert_array_equal(xdata10, ref_x)
    # y-axis
    ydata10 = ydata_first[0:10]
    ref_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 11.0, 0.0])
    np.testing.assert_array_equal(ydata10, ref_y)


@pytest.fixture(scope="function")
def test_calculate_first_derivative_yaxis_medium(data_server):
    '''Step1 - derivative: testing the first derivative calculation of medium data set - axis y'''
    csvfn = data_server.get_path("medium_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    [_, ydata_first] = peakfinder.get_first_derivative()
    # y-axis only
    ydata10 = ydata_first[0:10]
    ref_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 19.0, -13.0])
    np.testing.assert_array_equal(ydata10, ref_y)


@pytest.fixture(scope="function")
def test_calculatefirstderivative_yaxis_hard(data_server):
    '''Step1 - derivative: testing the first derivative calculation of hard data set - axis y'''
    csvfn = data_server.get_path("hard_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    [_, ydata_first] = peakfinder.get_first_derivative()
    # y-axis only
    ydata10 = ydata_first[0:10]
    ref_y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 28.0, -10.0, 18.0])
    np.testing.assert_array_equal(ydata10, ref_y)


@pytest.fixture(scope="function")
def test_calculateMinMaxDervativePixels_easy(data_server):
    '''Step2 - calculate derivative counts value of easy data set'''
    csvfn = data_server.get_path("easy_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    # minValue
    min_derivative_value = peakfinder.get_min_derivative_value()
    np.testing.assert_equal(min_derivative_value, -4152.0)
    # maxValue
    max_derivative_value = peakfinder.get_max_derivative_value()
    np.testing.assert_equal(max_derivative_value, 4001.0)
    # minValuePixel
    min_derivative_pixel_value = peakfinder.get_min_derivation_pixel_value()
    np.testing.assert_equal(min_derivative_pixel_value, 130.5)
    # maxValuePixel
    max_derivative_pixel_value = peakfinder.get_max_derivation_pixel_value()
    np.testing.assert_equal(max_derivative_pixel_value, 131.5)


@pytest.fixture(scope="function")
def test_calculateMinMaxDervativePixels_medium(data_server):
    '''Step2 - calculate derivative counts value of medium data set'''
    csvfn = data_server.get_path("medium_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    # minValue
    min_derivative_value = peakfinder.get_min_derivative_value()
    np.testing.assert_equal(min_derivative_value, -949.0)
    # maxValue
    max_derivative_value = peakfinder.get_max_derivative_value()
    np.testing.assert_equal(max_derivative_value, 1052.0)


@pytest.fixture(scope="function")
def test_calculateMinMaxDervativePixels_hard(data_server):
    '''Step2 - calculate derivative counts value of hard data set'''
    csvfn = data_server.get_path("hard_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    # minValue
    min_derivative_value = peakfinder.get_min_derivative_value()
    np.testing.assert_equal(min_derivative_value, -475.0)
    # maxValue
    max_derivative_value = peakfinder.get_max_derivative_value()
    np.testing.assert_equal(max_derivative_value, 324.0)


@pytest.fixture(scope="function")
def test_calculateAvgAndStdDerivation_counts_firstderi_easy(data_server):
    '''Step3 - calculate mean and std of first derivation counts of easy data set'''
    csvfn = data_server.get_path("easy_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    # mean
    mean_counts_firstderi = peakfinder.get_average_of_first_derivation_counts()
    np.testing.assert_equal(mean_counts_firstderi, 0)
    # std
    std_deviation_counts_firstderi = peakfinder.get_std_deviation_of_first_derivation_counts()
    np.testing.assert_almost_equal(std_deviation_counts_firstderi, 948.8, 0.1)


@pytest.fixture(scope="function")
def test_calculateAvgAndStdDerivation_counts_firstderi_medium(data_server):
    '''Step3 - calculate mean and std of first derivation counts of medium data set'''
    csvfn = data_server.get_path("medium_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    # mean
    mean_counts_firstderi = peakfinder.get_average_of_first_derivation_counts()
    np.testing.assert_equal(mean_counts_firstderi, 0)
    # std
    std_deviation_counts_firstderi = peakfinder.get_std_deviation_of_first_derivation_counts()
    np.testing.assert_almost_equal(std_deviation_counts_firstderi, 222.5, 0.1)


@pytest.fixture(scope="function")
def test_calculateAvgAndStdDerivation_counts_firstderi_hard(data_server):
    '''Step3 - calculate mean and std of first derivation counts of hard data set'''
    csvfn = data_server.get_path("hard_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    # mean
    mean_counts_firstderi = peakfinder.get_average_of_first_derivation_counts()
    np.testing.assert_equal(mean_counts_firstderi, 0)
    # std
    std_deviation_counts_firstderi = peakfinder.get_std_deviation_of_first_derivation_counts()
    np.testing.assert_almost_equal(std_deviation_counts_firstderi, 76.3, 0.1)


@pytest.fixture(scope="function")
def test_calculateLowResPixel_easy(data_server):
    '''Step4 - assert the min&max value of low res for an easy data set'''
    csvfn = data_server.get_path("easy_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    low_res_range = peakfinder.get_low_res()
    # minValue
    np.testing.assert_equal(low_res_range[0], 93)
    # maxValue
    np.testing.assert_equal(low_res_range[1], 163)


@pytest.fixture(scope="function")
def test_calculateLowResPixel_medium(data_server):
    '''Step4 - assert the min&max value of low res for a medium data set'''
    csvfn = data_server.get_path("medium_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    low_res_range = peakfinder.get_low_res()
    # minValue
    np.testing.assert_equal(low_res_range[0], 89)
    # maxValue
    np.testing.assert_equal(low_res_range[1], 167)


@pytest.fixture(scope="function")
def test_calculateLowResPixel_hard(data_server):
    '''Step4 - assert the min&max value of low res for a hard data set'''
    csvfn = data_server.get_path("hard_data_set_low_res_finder_alg.csv")
    [xdata, ydata, edata] = loadCsvFile(csvfn)
    peakfinder = LowResFinder(xdata, ydata, edata)
    low_res_range = peakfinder.get_low_res()
    # minValue
    np.testing.assert_equal(low_res_range[0], 116)
    # maxValue
    np.testing.assert_equal(low_res_range[1], 197)


if __name__ == '__main__':
    pytest.main([__file__])
