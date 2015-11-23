from numpy.version import version as numpy_version
from matplotlib import __version__ as matplotlib_version
from PyQt4.pyqtconfig import Configuration as pyqt_configuration
import RefRed.version
from PyQt4 import QtGui, QtCore
import sys


class AboutDialog(object):
        
        parent = None
        
        def __init__(self, parent=None):
                self.parent = parent

        def display(self):
                RefRed_version = RefRed.version.str_version
                python_version =  sys.version
                numpy_version = numpy_version
                mantid_version = ''
                matplotlib_version = matplotlib_version
                qt_version = QtCore.QT_VERSION_STR
                pyqt_version = pyqt_configuration().pyqt_version_str

                message = '''RefRed - Liquids Reflectrometry Reduction program
                version %s on Python %s
                
                Library versions:
                  - Numpy %s
                  - Mantid  %s
                  - Matplotlib %s
                  - Qt %s
                  - PyQt %s''' %(ref_red_version, 
                                 python_version,
                                 numpy_version,
                                 mantid_version,
                                 matplotlib_version,
                                 qt_version,
                                 pyqt_version)

                QtGui.QMessageBox.about(self, 'About RefRed', message)


