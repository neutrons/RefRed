# third party packages
import unittest.mock as mock

import pytest

# RefRed imports
from RefRed.configuration.loading_configuration import LoadingConfiguration
from RefRed.tabledata import TableData


class TestLoadingConfiguration(object):
    def test_init(self):
        with mock.patch("RefRed.configuration.loading_configuration.StatusMessageHandler") as mockStatusMessageHandler:
            m = mock.Mock()
            loadingConfiguration = LoadingConfiguration(parent=m)
            mockStatusMessageHandler.assert_called()
            return loadingConfiguration

    @pytest.mark.parametrize(
        "filepath, message",
        [
            ("REF_L_188298_tiny_template.xml", "Done!"),
            (["other", "REF_L_188298_tiny_template.xml"], "Done!"),
            ("", "File not found"),
        ],
    )
    @mock.patch("RefRed.configuration.loading_configuration.QFileDialog")
    @mock.patch("RefRed.configuration.loading_configuration.StatusMessageHandler")
    def test_run_file_search(self, StatusMessageHandlerMock, QFileDialogMock, filepath, message, data_server):
        def add_abspath(input_filepath):
            r"""helper to add the absolute path to file REF_L_188298_tiny_template.xml"""
            if input_filepath:
                if isinstance(input_filepath, str):
                    return data_server.path_to(input_filepath)
                elif isinstance(input_filepath, list):
                    return input_filepath[:-1] + [add_abspath(input_filepath[-1])]
            else:
                return input_filepath  # an empty string

        # instantiate a LoadingConfiguration object
        parent = mock.Mock()  # mock MainGui
        loader = LoadingConfiguration(parent=parent)
        loader.loading = lambda: None  # we're not interested in loading the file, thus override this method
        StatusMessageHandlerMock.assert_called()

        # When QFileDialog is called within loadingConfiguration.run(), it will return this mock file dialog object
        file_dialog_mock = mock.Mock()
        file_dialog_mock.exec_.return_value = True  # need to mock QFileDialog.exec_()
        filepath = add_abspath(filepath)
        file_dialog_mock.selectedFiles.return_value = filepath
        QFileDialogMock.return_value = file_dialog_mock  # now QFileDialog(...) should return out file_dialog_mock

        loader.run()  # test is the file is found
        StatusMessageHandlerMock.assert_called_with(parent=parent, message=message, is_threaded=True)

    @mock.patch("RefRed.tabledata.TableData._validate_type")
    @mock.patch("RefRed.configuration.loading_configuration.LoadingConfiguration.getMetadataObject")
    def test_populate_big_table_data_with_lconfig(self, mockGetMetadataObject, mock_validate_type):
        mockGetMetadataObject.return_value = mock.Mock()
        mock_validate_type.return_value = None  # don't check the type of elements when inserted in the table

        loadingConfiguration = self.test_init()
        REDUCTIONTABLE_MAX_ROWCOUNT = 1
        loadingConfiguration.parent.REDUCTIONTABLE_MAX_ROWCOUNT = REDUCTIONTABLE_MAX_ROWCOUNT
        loadingConfiguration.parent.big_table_data = TableData(REDUCTIONTABLE_MAX_ROWCOUNT)

        loadingConfiguration.dom = mock.Mock()
        loadingConfiguration.dom.getElementsByTagName.return_value = [mock.Mock()]
        loadingConfiguration.populate_big_table_data_with_lconfig()
        assert loadingConfiguration.parent.big_table_data.reduction_config(0) == mockGetMetadataObject.return_value

    def test_populate_main_gui_general_settings(self):
        loadingConfiguration = self.test_init()

        loadingConfiguration.parent.ui.selectIncidentMediumList.count.return_value = 2

        values = {
            "q_step": 1.001,
            "q_min": 2.002,
            # Applying normalization is a global setting
            "norm_flag": True,
            "angle_offset": 2.5025,
            "angle_offset_error": 3.003,
            "scaling_factor_file": "scaling_factor_file",
            "incident_medium_index_selected": 5.005,
            "scaling_factor_flag": 6.006,
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

        # Mock the deadtime_settings object and its method
        mock_deadtime_settings = mock.MagicMock()
        mock_deadtime_settings.from_xml = mock.Mock()
        loadingConfiguration.parent.deadtime_settings = mock_deadtime_settings

        # Mock the applyCheckBox object and its method
        mock_applyCheckBox = mock.MagicMock()
        mock_applyCheckBox.setChecked = mock.Mock()
        loadingConfiguration.parent.ui.deadtime_entry.applyCheckBox = mock_applyCheckBox

        # call the method of interest
        loadingConfiguration.populate_main_gui_general_settings()

        # verify getNodeValue was called
        loadingConfiguration.getNodeValue.assert_has_calls([mock.call(node_0, k) for k in values.keys()])

        # Assert if the 'from_xml' method of 'deadtime_settings' is called
        mock_deadtime_settings.from_xml.assert_called_once_with(node_0)
        # Assert if the 'setChecked' method of 'applyCheckBox' is called
        mock_applyCheckBox.setChecked.assert_called_once_with(
            loadingConfiguration.parent.deadtime_settings.apply_deadtime
        )

    # test that iMetadata.data_peak gets set properly
    def test_getMetadataObject(self):
        loader = self.test_init()
        node_mock = mock.Mock()  # mocks the Node instance associated to an XML block of an input configuration file

        values = {
            "from_peak_pixels": 1,
            "to_peak_pixels": 2,
            "back_roi1_from": 3,
            "back_roi1_to": 4,
            "x_min_pixel": 5.005,
            "x_max_pixel": 6.006,
            "background_flag": "background_flag",
            "x_range_flag": "x_range_flag",
            "from_tof_range": 7.007,
            "to_tof_range": 8.008,
            "from_q_range": 9.009,
            "to_q_range": 10.010,
            "from_lambda_range": 11.011,
            "to_lambda_range": 12.012,
            "data_sets": "dataset1, dataset2",
            "tof_range_flag": "tof_range_flag",
            "norm_from_peak_pixels": 13.013,
            "norm_to_peak_pixels": 14.014,
            "norm_from_back_pixels": 15.015,
            "norm_to_back_pixels": 16.016,
            "norm_dataset": "normData1, normData2",
            "norm_x_min": 17.017,
            "norm_x_max": 18.018,
            "norm_background_flag": "norm_background_flag",
            "norm_x_range_flag": "norm_x_range_flag",
            "data_full_file_name": "dataFullFileName1,dataFullFileName2",
            "norm_full_file_name": "normFullFileName1,normFullFileName2",
            "const_q": True,
        }

        def side_effect(_, arg, default=""):
            return values.get(arg, default)

        # getNodeValue() will read data from dict `values`, instead of read from some configuration file
        loader.getNodeValue = mock.Mock()
        loader.getNodeValue.side_effect = side_effect

        config = loader.getMetadataObject(node_mock)

        assert config.data_peak[0] == values["from_peak_pixels"]
        assert config.data_peak[1] == values["to_peak_pixels"]
        assert config.data_back[0] == values["back_roi1_from"]
        assert config.data_back[1] == values["back_roi1_to"]
        assert config.data_low_res == [values["x_min_pixel"], values["x_max_pixel"]]
        assert config.const_q == values["const_q"]


if __name__ == "__main__":
    pytest.main([__file__])
