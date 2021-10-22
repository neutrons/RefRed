# package import
from RefRed.widgets import getOpenFileName, getOpenFileNames, getSaveFileName

# 3rd party imports
import pytest
import unittest.mock as mock

FILENAME_SINGLE = "/tmp/test.txt"
FILENAME_MULTIPLE = [FILENAME_SINGLE, FILENAME_SINGLE]
FILTER = "(*.txt)"


def create_faker(qt_version, multiple_files=False):
    # decide how many files to return
    if multiple_files:
        filename = FILENAME_MULTIPLE
    else:
        filename = FILENAME_SINGLE

    if qt_version == "Qt4":

        def faker(*args, **kwargs):
            # only return filename
            return filename

        return faker
    elif qt_version == "Qt5":

        def faker(*args, **kwargs):
            # return filename and filter
            return filename, FILTER

        return faker
    else:
        raise ValueError(f"Cannot create mock for qt_version={qt_version}")


@mock.patch("qtpy.QtWidgets.QFileDialog")
@pytest.mark.parametrize("qt_version,filter", [("Qt4", ""), ("Qt5", FILTER)])
def test_getSaveFileName(mockQtFileSaver, qt_version, filter):
    """
    Test that getSaveFileName returns a file name and an empty filter
    under Qt4.
    """
    # setup the fake QtFileSaver
    mockQtFileSaver.getSaveFileName = create_faker(qt_version)
    # run
    fn, ff = getSaveFileName(None, "testing", "tt.txt")
    # assert
    assert fn == FILENAME_SINGLE
    assert ff == filter


@mock.patch("qtpy.QtWidgets.QFileDialog")
@pytest.mark.parametrize("qt_version,filter", [("Qt4", ""), ("Qt5", FILTER)])
def test_getOpenFileName(mockQtFileOpener, qt_version, filter):
    """
    Test that getOpenFileName returns a file name and an empty filter
    under Qt4.
    """
    # setup the fake QtFileSaver
    mockQtFileOpener.getOpenFileName = create_faker(qt_version)
    # run
    fn, ff = getOpenFileName(None, "testing", "tt.txt")
    # assert
    assert fn == FILENAME_SINGLE
    assert ff == filter


@mock.patch("qtpy.QtWidgets.QFileDialog")
@pytest.mark.parametrize("qt_version,filter", [("Qt4", ""), ("Qt5", FILTER)])
def test_getOpenFileNames(mockQtFileOpener, qt_version, filter):
    """
    Test that getOpenFileNames returns a list of file names and an empty filter
    under Qt4.
    """
    # setup the fake QtFileSaver
    mockQtFileOpener.getOpenFileNames = create_faker(qt_version, multiple_files=True)
    # run
    fn, ff = getOpenFileNames(None, "testing", "tt.txt")
    # assert
    assert fn == FILENAME_MULTIPLE
    assert ff == filter


if __name__ == "__main__":
    pytest.main([__file__])
