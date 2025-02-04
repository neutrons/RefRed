from numpy.version import version as numpy_version_str
from matplotlib import __version__ as matplotlib_version_str
from RefRed import __version__ as RefRed_version_str
from qtpy import QtWidgets, QT_VERSION, PYQT_VERSION
import sys
import mantid
import lr_reduction


class AboutDialog(object):
    parent = None

    def __init__(self, parent=None):
        self.parent = parent

    def display(self):
        python_version = self.get_python_version()
        numpy_version = numpy_version_str
        mantid_version = mantid.__version__
        matplotlib_version = matplotlib_version_str
        qt_version = QT_VERSION
        pyqt_version = PYQT_VERSION

        message = f"""RefRed - Liquids Reflectrometry Reduction program

        RefRed version {RefRed_version_str}
        Reduction version {lr_reduction.__version__}

        Library versions:
          - Python: {python_version}
          - Numpy: {numpy_version}
          - Mantid:  {mantid_version}
          - Matplotlib: {matplotlib_version}
          - Qt: {qt_version}
          - PyQt: {pyqt_version}"""

        QtWidgets.QMessageBox.about(self.parent, "About RefRed", message)

    def get_python_version(self):
        str_version = sys.version_info
        str_array = []
        for value in str_version:
            str_array.append(str(value))
        return ".".join(str_array[0:3])
