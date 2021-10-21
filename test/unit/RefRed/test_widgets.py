# package import
from RefRed.widgets import getSaveFileName

# 3rd party imports
import pytest
import unittest.mock as mock


@mock.patch("qtpy.QtWidgets.QFileDialog")
def test_getSaveFileName_Qt4(mockQtFileSaver):
    """
    Test that getSaveFileName returns a file name and an empty filter
    under Qt4.
    """
    # setup the fake QtFileSaver
    def faker(*args, **kwargs):
        return "test.txt"
    mockQtFileSaver.getSaveFileName = faker
    # run
    fn, ff = getSaveFileName(None, "testing", "tt.txt")
    # assert
    assert fn == "test.txt"
    assert ff == ""

@mock.patch("qtpy.QtWidgets.QFileDialog")
def test_getSaveFileName_Qt5(mockQtFileSaver):
    """
    Test that getSaveFileName returns a file name and a filter
    under Qt5.
    """
    # setup the fake QtFileSaver
    def faker(*args, **kwargs):
        return "/tmp/test.txt", "(*.txt)"
    mockQtFileSaver.getSaveFileName = faker
    # run
    fn, ff = getSaveFileName(None, "testing", "tt.txt")
    # assert
    assert fn == "/tmp/test.txt"
    assert ff == "(*.txt)"


if __name__ == '__main__':
    pytest.main([__file__])
