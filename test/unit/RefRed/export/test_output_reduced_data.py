# package imports


# 3rd party imports
import os
import pytest
import unittest.mock as mock


# ----- Create a mocked object for testing only ----- #
FILEPATH = "/tmp"
FILENAME = "test.txt"
FULLPATH = os.path.join(FILEPATH, FILENAME)
FILEEXT = "Reduced Ascii (*.txt)"


# NOTE:
# mocking QDialog (which is necessary to get testing started) will mask out
# most of the sub-function returns
# e.g.
# ord.func() -> <MagicMock name='QDialog.func()' id='139838433727440'>
@mock.patch("qtpy.QtWidgets.QFileDialog.getExistingDirectory")
@mock.patch("qtpy.QtWidgets.QFileDialog.getSaveFileName")
@mock.patch("qtpy.QtWidgets.QDialog")
def getMockedORD(fakeQDialog, fakeGetSaveFileName, fakeGetExistingDirectory):
    # make sure flake8 is happy
    fakeQDialog.mocked = True
    fakeGetSaveFileName = mock.MagicMock(return_value=(FULLPATH, FILEEXT))
    _ = fakeGetSaveFileName()
    fakeGetExistingDirectory = mock.MagicMock(return_value=FILEPATH)
    _ = fakeGetExistingDirectory()
    # actual test
    # NOTE:
    # Due to the many level circular imports with RefRed, the mock patch only
    # works if we import the class last so that Python does not have a chance
    # to get the non-mocked version.
    from RefRed.export.output_reduced_data import OutputReducedData

    parent = mock.Mock()
    parent.o_stitching_ascii_widget = "o_stitching_ascii_widget"
    parent._gui_metadata = {"q_min": 1.0}
    parent.ui = mock.Mock()
    parent.ui.reductionTable = mock.Mock()

    def fake_item(*arg, **kwarg):
        item = mock.Mock()
        item.text = mock.MagicMock(return_value="1")
        return item

    parent.ui.reductionTable.item = fake_item
    parent.path_ascii = FILEPATH
    #
    mocked_ord = OutputReducedData(parent)
    # *********************************************** #
    # mocked out methods that relies on other modules #
    # *********************************************** #
    mocked_ord.generate_selected_sf = mock.MagicMock()
    mocked_ord.apply_sf = mock.MagicMock(return_value=["test_ws"])
    mocked_ord.collect_list_wks = mock.MagicMock(return_value=["test_ws"])
    mocked_ord.create_output_file = mock.MagicMock()
    mocked_ord.write_n_ascii = mock.MagicMock()
    mocked_ord.retrieve_metadata = mock.MagicMock(return_value=["test"])
    mocked_ord.retrieve_individual_metadata = mock.MagicMock(return_value=["test"])
    # NOTE:
    # Func produce_data_with_common_q_axis is an important function, but its
    # complex internal dependencies is prevent us from writing a unit test for
    # it.  It might become testable if refactored.
    mocked_ord.produce_data_with_common_q_axis = mock.MagicMock()
    mocked_ord.create_file = mock.MagicMock()
    mocked_ord.retrieve_sf = mock.MagicMock(return_value=1)
    mocked_ord.retrieve_scaling_factor = mock.MagicMock(return_value="1")
    mocked_ord.is_folder_access_granted = mock.MagicMock(return_value=True)
    mocked_ord.apply_scaling_factor = mock.MagicMock()
    mocked_ord.get_q_range = mock.MagicMock(return_value=[1.0, 2.0])
    return mocked_ord


ord = getMockedORD()


# ----- Testing methods ----- #
def test_auto_qmin_button_clicked():
    ord.ui.manual_qmin_frame.setEnabled = mock.MagicMock()
    # call the method
    ord.auto_qmin_button_clicked(True)
    # check
    ord.auto_qmin_button_clicked.assert_called_once()


def test_output_format_radio_buttons_event():
    # call without any error is consider a success here
    ord.output_format_radio_buttons_event()


def test_create_reduce_ascii_button_event():
    # only testing the None branch, the rest are done in other tests
    ord.parent.o_stitching_ascii_widget = None
    # call without any error is consider a success here
    ord.create_reduce_ascii_button_event()


def test_create_n_files():
    # call without any error is consider a success here
    ord.create_n_files()


def test_create_1_common_file():
    # call without any error is consider a success here
    ord.create_1_common_file()


def test_save_back_widget_parameters_used():
    # call without any error is consider a success here
    ord.save_back_widget_parameters_used()


def test_format_n_filename():
    # call without any error is consider a success here as we cannot get the
    # name back
    _ = ord.format_n_filename(0)


def test_write_1_common_ascii():
    # call without any error is consider a success here
    ord.write_1_common_ascii()


def test_format_metadata():
    # can't verify the output as the mocking of QDialog hides the return
    outstr = ord.format_metadata()
    assert outstr


def test_retrieve_total_counts():
    ord.retrieve_total_counts(1)


def test_retrieve_pcCharge():
    ord.retrieve_pcCharge(1)


def test_produce_data_without_common_q_axis():
    ord.produce_data_without_common_q_axis()


def test_applySF():
    ord.applySF()


def test_format_data():
    ord.format_data()


def test_centering_q_axis():
    ord.centering_q_axis()


def test_cleanup_data():
    ord.cleanup_data()


def test_closeEvent():
    ord.closeEvent()


if __name__ == "__main__":
    pytest.main([__file__])
