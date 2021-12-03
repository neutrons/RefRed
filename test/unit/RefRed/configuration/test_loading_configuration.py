# package imports
from RefRed.configuration.loading_configuration import LoadingConfiguration

# third party packages
import unittest.mock as mock
import pytest


class TestLoadingConfiguration(object):
    def evaluate(self, expected, actual):
        if str(actual).replace('.', '', 1).isdigit():
            assert expected == pytest.approx(actual)
            return True
        return False

    def test_init(self):
        with mock.patch('RefRed.configuration.loading_configuration.StatusMessageHandler') as mockStatusMessageHandler:
            m = mock.Mock()
            loadingConfiguration = LoadingConfiguration(parent=m)
            mockStatusMessageHandler.assert_called()
            return loadingConfiguration

    @mock.patch('os.path.isfile')
    @mock.patch('RefRed.configuration.loading_configuration.StatusMessageHandler')
    @mock.patch('RefRed.configuration.loading_configuration.LoadingConfiguration.loading')
    @mock.patch('qtpy.QtWidgets.QFileDialog')
    def test_run_file_found(self, mockQFileDialog, mockLoading, mockStatusMessageHandler, mockOsPathIsFile):
        mockFileDialog = mock.Mock()
        mockFileDialog.exec_.return_value = True
        mockFileDialog.selectedFiles.return_value = 'this is a filename'

        mockOsPathIsFile.return_value = True

        mockQFileDialog.return_value = mockFileDialog
        loadingConfiguration = self.test_init()
        loadingConfiguration.run()

        mockQFileDialog.assert_called()
        mockFileDialog.exec_.assert_called()
        mockFileDialog.selectedFiles.assert_called()
        mockOsPathIsFile.assert_called()
        mockStatusMessageHandler.assert_called_with(
            parent=loadingConfiguration.parent, message='Done!', is_threaded=True
        )
        mockLoading.assert_called()

    @mock.patch('os.path.isfile')
    @mock.patch('RefRed.configuration.loading_configuration.StatusMessageHandler')
    @mock.patch('RefRed.configuration.loading_configuration.LoadingConfiguration.loading')
    @mock.patch('qtpy.QtWidgets.QFileDialog')
    def test_run_file_not_found(self, mockQFileDialog, mockLoading, mockStatusMessageHandler, mockOsPathIsFile):
        mockFileDialog = mock.Mock()
        mockFileDialog.exec_.return_value = True
        mockFileDialog.selectedFiles.return_value = ''

        mockOsPathIsFile.return_value = True

        mockQFileDialog.return_value = mockFileDialog
        loadingConfiguration = self.test_init()
        loadingConfiguration.run()

        mockQFileDialog.assert_called()
        mockFileDialog.exec_.assert_called()
        mockFileDialog.selectedFiles.assert_called()
        not mockOsPathIsFile.called
        mockStatusMessageHandler.assert_called_with(
            parent=loadingConfiguration.parent, message='User Canceled loading!', is_threaded=True
        )
        assert not mockLoading.called

    @mock.patch('os.path.isfile')
    @mock.patch('RefRed.configuration.loading_configuration.StatusMessageHandler')
    @mock.patch('RefRed.configuration.loading_configuration.LoadingConfiguration.loading')
    @mock.patch('qtpy.QtWidgets.QFileDialog')
    def test_run_file_found_but_filename_is_list(
        self, mockQFileDialog, mockLoading, mockStatusMessageHandler, mockOsPathIsFile
    ):
        mockFileDialog = mock.Mock()
        mockFileDialog.exec_.return_value = True
        mockFileDialog.selectedFiles.return_value = ['', 'this is a filename']

        mockOsPathIsFile.return_value = True

        mockQFileDialog.return_value = mockFileDialog
        loadingConfiguration = self.test_init()
        loadingConfiguration.run()

        mockQFileDialog.assert_called()
        mockFileDialog.exec_.assert_called()
        mockFileDialog.selectedFiles.assert_called()
        mockOsPathIsFile.assert_called()
        mockStatusMessageHandler.assert_called_with(
            parent=loadingConfiguration.parent, message='Done!', is_threaded=True
        )
        mockLoading.assert_called()

    @mock.patch('RefRed.configuration.loading_configuration.LoadingConfiguration.getMetadataObject')
    def test_populate_big_table_data_with_lconfig(self, mockGetMetadataObject):
        loadingConfiguration = self.test_init()
        loadingConfiguration.parent.nbr_row_table_reduction = 1
        loadingConfiguration.parent.big_table_data = [[0]]

        mockGetMetadataObject.return_value = mock.Mock()

        loadingConfiguration.dom = mock.Mock()
        loadingConfiguration.dom.getElementsByTagName.return_value = [mock.Mock()]

        loadingConfiguration.populate_big_table_data_with_lconfig()
        assert loadingConfiguration.parent.big_table_data[0, 2] == mockGetMetadataObject.return_value

    def test_populate_main_gui_general_settings(self):
        loadingConfiguration = self.test_init()

        loadingConfiguration.parent.ui.selectIncidentMediumList.count.return_value = 2

        values = {
            'q_step': 1.001,
            'q_min': 2.002,
            'angle_offset': 2.5025,
            'angle_offset_error': 3.003,
            'scaling_factor_file': 'scaling_factor_file',
            'incident_medium_index_selected': 5.005,
            'scaling_factor_flag': 6.006,
        }

        def side_effect(node, arg):
            return values[arg]

        loadingConfiguration.getNodeValue = mock.Mock()
        loadingConfiguration.getNodeValue.side_effect = side_effect

        loadingConfiguration.dom = mock.Mock()
        node_0 = mock.Mock()
        loadingConfiguration.dom.getElementsByTagName.return_value = [node_0]

        mockGuiMetadata = mock.MagicMock()
        mockGuiMetadata.__getitem__.side_effect = lambda x: getattr(mockGuiMetadata, x)

        loadingConfiguration.parent.gui_metadata = mockGuiMetadata

        loadingConfiguration.populate_main_gui_general_settings()
        loadingConfiguration.getNodeValue.assert_has_calls([mock.call(node_0, k) for k in values.keys()])

    # test that iMetadata.data_peak gets set properly
    def test_getMetadataObject(self):
        loadingConfiguration = self.test_init()
        mockNode = mock.Mock()

        values = {
            'from_peak_pixels': 1.001,
            'to_peak_pixels': 2.002,
            'back_roi1_from': 3.003,
            'back_roi1_to': 4.004,
            'x_min_pixel': 5.005,
            'x_max_pixel': 6.006,
            'background_flag': 'background_flag',
            'x_range_flag': 'x_range_flag',
            'from_tof_range': 7.007,
            'to_tof_range': 8.008,
            'from_q_range': 9.009,
            'to_q_range': 10.010,
            'from_lambda_range': 11.011,
            'to_lambda_range': 12.012,
            'data_sets': 'dataset1, dataset2',
            'tof_range_flag': 'tof_range_flag',
            'norm_flag': 'norm_flag',
            'norm_from_peak_pixels': 13.013,
            'norm_to_peak_pixels': 14.014,
            'norm_from_back_pixels': 15.015,
            'norm_to_back_pixels': 16.016,
            'norm_dataset': 'normData1, normData2',
            'norm_x_min': 17.017,
            'norm_x_max': 18.018,
            'norm_background_flag': 'norm_background_flag',
            'norm_x_range_flag': 'norm_x_range_flag',
            'data_full_file_name': 'dataFullFileName1,dataFullFileName2',
            'norm_full_file_name': 'normFullFileName1,normFullFileName2',
        }

        def side_effect(node, arg):
            return values[arg]

        loadingConfiguration.getNodeValue = mock.Mock()
        loadingConfiguration.getNodeValue.side_effect = side_effect

        iMetadata = loadingConfiguration.getMetadataObject(mockNode)

        loadingConfiguration.getNodeValue.assert_has_calls([mock.call(mockNode, k) for k in values.keys()])
        assert iMetadata.data_peak[0] == values['from_peak_pixels']
        assert iMetadata.data_peak[1] == values['to_peak_pixels']

        assert iMetadata.data_back[0] == values['back_roi1_from']
        assert iMetadata.data_back[1] == values['back_roi1_to']

        metaDict = iMetadata.__dict__

        expectedValue = 1.001
        for key, value in metaDict.items():
            if isinstance(value, list):
                for item in value:
                    if key == 'tof_range':
                        self.evaluate(expectedValue, float(item) / 1000)
                        expectedValue += 1.001
                    elif self.evaluate(expectedValue, item):
                        expectedValue += 1.001
            else:
                if self.evaluate(expectedValue, value):
                    expectedValue += 1.001


if __name__ == '__main__':
    pytest.main([__file__])
