# package import
from RefRed.widgets import getOpenFileName, getSaveFileName

# 3rd party imports
import pytest
import unittest.mock as mock

FILENAME_SINGLE = "/tmp/test.txt"
FILTER = "(*.txt)"


def create_faker(qt_version):
    if qt_version == "Qt4":

        def faker(*args, **kwargs):
            # only return filename
            return FILENAME_SINGLE

        return faker
    elif qt_version == "Qt5":

        def faker(*args, **kwargs):
            # return filename and filter
            return FILENAME_SINGLE, FILTER

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
    Test that getSaveFileName returns a file name and an empty filter
    under Qt4.
    """
    # setup the fake QtFileSaver
    mockQtFileOpener.getOpenFileName = create_faker(qt_version)
    # run
    fn, ff = getOpenFileName(None, "testing", "tt.txt")
    # assert
    assert fn == FILENAME_SINGLE
    assert ff == filter


if __name__ == "__main__":
    pytest.main([__file__])
