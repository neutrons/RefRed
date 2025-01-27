# package imports
# third party packages
import pytest

from RefRed.file_loading_utility import loadCsvFile


@pytest.fixture(scope="function")
def csv_data(data_server):
    return loadCsvFile(data_server.path_to("easy_data_set.csv"))


def test_loadcsvfile_xaxis(csv_data):
    """Step1 - Loading: checking that loadCsvFile works correctly on xaxis"""
    [xdata, _, _] = csv_data
    xdata10 = xdata[0:10]
    assert xdata10 == pytest.approx([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])


def test_loadcsvfile_yaxis(csv_data):
    """Step1 - Loading: checking that loadCsvFile works correctly on yaxis"""
    [_, ydata, _] = csv_data
    ydata10 = ydata[0:10]
    assert ydata10 == pytest.approx([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 5.0])


def test_loadcsvfile_eaxis(csv_data):
    """Step1 - Loading: checking that loadCsvFile works correctly on eaxis"""
    [_, _, edata] = csv_data
    edata10 = edata[0:10]
    assert edata10 == pytest.approx([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.236067977])
