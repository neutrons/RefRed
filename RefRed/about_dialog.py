from numpy.version import version as numpy_version_str
from matplotlib import __version__ as matplotlib_version_str
import RefRed.version
from qtpy import QtWidgets, QT_VERSION, PYQT_VERSION
import sys
import mantid


class AboutDialog(object):

    parent = None

    def __init__(self, parent=None):
        self.parent = parent

    def display(self):
        RefRed_version = RefRed.version.str_version
        python_version = self.get_python_version()
        numpy_version = numpy_version_str
        mantid_version = mantid.__version__
        matplotlib_version = matplotlib_version_str
        qt_version = QT_VERSION
        pyqt_version = PYQT_VERSION

        message = '''RefRed - Liquids Reflectrometry Reduction program

        version %s

        Library versions:
          - Python: %s
          - Numpy: %s
          - Mantid:  %s
          - Matplotlib: %s
          - Qt: %s
          - PyQt: %s''' % (RefRed_version, python_version,
                           numpy_version, mantid_version,
                           matplotlib_version, qt_version,
                           pyqt_version)

        QtWidgets.QMessageBox.about(self.parent, 'About RefRed', message)

    def get_python_version(self):
        str_version = sys.version_info
        str_array = []
        for value in str_version:
                str_array.append(str(value))
        return ".".join(str_array[0:3])
