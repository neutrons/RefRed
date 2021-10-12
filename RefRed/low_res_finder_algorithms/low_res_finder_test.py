import unittest
from RefRed.file_loading_utility import loadCsvFile
from RefRed.low_res_finder_algorithms.low_res_finder import LowResFinder


class LowResFinderTest(unittest.TestCase):
    '''
    easy_data_set.csv -> run 130063
    medium_data_set.csv -> run 130092
    hard_datas_set.csv -> run 130092 (last one in John's spreadsheet)
    '''

    def setUp(self):
        self.top_folder = 'RefRed/low_res_finder_algorithms'

    def test_loadcsvfile_xaxis_easy(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on easy xaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        xdata10 = xdata[0:10]
        self.assertEqual(xdata10, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])

    def test_loadcsvfile_yaxis_easy(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on easy yaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        ydata10 = ydata[0:10]
        self.assertEqual(ydata10, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 12.0])

    def test_loadcsvfile_eaxis_easy(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on easy eaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        edata10 = edata[0:10]
        self.assertEqual(edata10, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.5])

    def test_loadcsvfile_xaxis_medium(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on medium xaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        xdata10 = xdata[0:10]
        self.assertEqual(xdata10, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])

    def test_loadcsvfile_yaxis_medium(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on medium yaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        ydata10 = ydata[0:10]
        self.assertEqual(ydata10, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 26.0])

    def test_loadcsvfile_eaxis_medium(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on medium eaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        edata10 = edata[0:10]
        self.assertEqual(edata10, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.6, 5.1])

    def test_loadcsvfile_xaxis_hard(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on hard xaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        xdata10 = xdata[0:10]
        self.assertEqual(xdata10, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])

    def test_loadcsvfile_yaxis_hard(self):
        '''Step0 - Loading: checking that loadCsvFile works correctly on hard yaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        ydata10 = ydata[0:10]
        self.assertEqual(ydata10, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 28.0, 18.0])

    def test_loadcsvfile_eaxis_hard(self):
        '''Step0- - Loading: checking that loadCsvFile works correctly on hard eaxis'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        edata10 = edata[0:10]
        self.assertEqual(edata10, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 5.3, 4.2])

    def test_calculate_first_derivative_xaxis_easy(self):
        '''Step1 - derivative: testing the first derivative calculation of easy data set - axis x'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        [xdata_first, ydata_first] = peakfinder.get_first_derivative()
        xdata10 = xdata_first[0:10]
        self.assertEqual(xdata10, [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])

    def test_calculatefirstderivative_yaxis_easy(self):
        '''Step1 - derivative: testing the first derivative calculation of easy data set - axis y'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        [xdata_first, ydata_first] = peakfinder.get_first_derivative()
        ydata10 = ydata_first[0:10]
        self.assertEqual(ydata10, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 11.0, 0.0])

    def test_calculatefirstderivative_yaxis_medium(self):
        '''Step1 - derivative: testing the first derivative calculation of medium data set - axis y'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        [xdata_first, ydata_first] = peakfinder.get_first_derivative()
        ydata10 = ydata_first[0:10]
        self.assertEqual(ydata10, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 19.0, -13.0])

    def test_calculatefirstderivative_yaxis_hard(self):
        '''Step1 - derivative: testing the first derivative calculation of hard data set - axis y'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        [xdata_first, ydata_first] = peakfinder.get_first_derivative()
        ydata10 = ydata_first[0:10]
        self.assertEqual(ydata10, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 28.0, -10.0, 18.0])

    def test_calculateMinMaxDervativePixels_minValue_easy(self):
        '''Step2 - calculate min derivative counts value of easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_min_derivative_value()
        self.assertEqual(min_derivative_value, -4152.0)

    def test_calculateMinMaxDervativePixels_minValuePixel_easy(self):
        '''Step2 - calculate Pixel of min derivative counts value of easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_min_derivation_pixel_value()
        self.assertEqual(min_derivative_value, 130.5)

    def test_calculateMinMaxDervativePixels_minValue_medium(self):
        '''Step2 - calculate min derivative counts value of medium data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_min_derivative_value()
        self.assertEqual(min_derivative_value, -949.0)

    def test_calculateMinMaxDervativePixels_minValue_hard(self):
        '''Step2 - calculate min derivative counts value of hard data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_min_derivative_value()
        self.assertEqual(min_derivative_value, -475.0)

    def test_calculateMinMaxDervativePixels_maxValue_easy(self):
        '''Step2 - calculate max derivative counts value of easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_max_derivative_value()
        self.assertEqual(min_derivative_value, 4001.0)

    def test_calculateMinMaxDervativePixels_maxValuePixel_easy(self):
        '''Step2 - calculate max derivative counts value of easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_max_derivation_pixel_value()
        self.assertEqual(min_derivative_value, 131.5)

    def test_calculateMinMaxDervativePixels_maxValue_medium(self):
        '''Step2 - calculate max derivative counts value of medium data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_max_derivative_value()
        self.assertEqual(min_derivative_value, 1052.0)

    def test_calculateMinMaxDervativePixels_maxValue_hard(self):
        '''Step2 - calculate max derivative counts value of hard data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        min_derivative_value = peakfinder.get_max_derivative_value()
        self.assertEqual(min_derivative_value, 324.0)

    def test_calculateAvgAndStdDerivation_mean_counts_firstderi_easy(self):
        '''Step3 - calculate average of first derivation counts of easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        mean_counts_firstderi = peakfinder.get_average_of_first_derivation_counts()
        self.assertEqual(mean_counts_firstderi, 0)

    def test_calculateAvgAndStdDerivation_mean_counts_firstderi_medium(self):
        '''Step3 - calculate average of first derivation counts of medium data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        mean_counts_firstderi = peakfinder.get_average_of_first_derivation_counts()
        self.assertEqual(mean_counts_firstderi, 0)

    def test_calculateAvgAndStdDerivation_mean_counts_firstderi_hard(self):
        '''Step3 - calculate average of first derivation counts of hard data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        mean_counts_firstderi = peakfinder.get_average_of_first_derivation_counts()
        self.assertEqual(mean_counts_firstderi, 0)

    def test_calculateAvgAndStdDerivation_std_deviation_counts_firstderi_easy(self):
        '''Step3 - calculate standard deviation of first derivation counts of easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        std_deviation_counts_firstderi = peakfinder.get_std_deviation_of_first_derivation_counts()
        self.assertAlmostEqual(std_deviation_counts_firstderi, 948.8, 0.1)

    def test_calculateAvgAndStdDerivation_std_deviation_counts_firstderi_medium(self):
        '''Step3 - calculate standard deviation of first derivation counts of medium data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        std_deviation_counts_firstderi = peakfinder.get_std_deviation_of_first_derivation_counts()
        self.assertAlmostEqual(std_deviation_counts_firstderi, 222.5, 0.1)

    def test_calculateAvgAndStdDerivation_std_deviation_counts_firstderi_hard(self):
        '''Step3 - calculate standard deviation of first derivation counts of hard data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        std_deviation_counts_firstderi = peakfinder.get_std_deviation_of_first_derivation_counts()
        self.assertAlmostEqual(std_deviation_counts_firstderi, 76.3, 0.1)

    def test_calculateLowResPixel_min_value_easy(self):
        ''' 'Step4 - assert the min value of low res for an easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        low_res_range = peakfinder.get_low_res()
        self.assertEqual(low_res_range[0], 93)

    def test_calculateLowResPixel_max_value_easy(self):
        ''' 'Step4 - assert the max value of low res for an easy data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/easy_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        low_res_range = peakfinder.get_low_res()
        self.assertEqual(low_res_range[1], 163)

    def test_calculateLowResPixel_min_value_medium(self):
        ''' 'Step4 - assert the min value of low res for an medium data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        low_res_range = peakfinder.get_low_res()
        self.assertEqual(low_res_range[0], 89)

    def test_calculateLowResPixel_max_value_medium(self):
        ''' 'Step4 - assert the max value of low res for an medium data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/medium_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        low_res_range = peakfinder.get_low_res()
        self.assertEqual(low_res_range[1], 167)

    def test_calculateLowResPixel_min_value_hard(self):
        ''' 'Step4 - assert the min value of low res for an hard data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        low_res_range = peakfinder.get_low_res()
        self.assertEqual(low_res_range[0], 116)

    def test_calculateLowResPixel_max_value_hard(self):
        ''' 'Step4 - assert the max value of low res for an hard data set'''
        [xdata, ydata, edata] = loadCsvFile(self.top_folder + '/hard_data_set.csv')
        peakfinder = LowResFinder(xdata, ydata, edata)
        low_res_range = peakfinder.get_low_res()
        self.assertEqual(low_res_range[1], 197)


if __name__ == '__main__':
    unittest.main()
