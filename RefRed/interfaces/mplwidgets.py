#!/usr/bin/env python
import os
import tempfile
from qtpy import QtCore, QtGui, QtWidgets
import matplotlib.cm
import matplotlib.colors
from . import icons_rc  # @UnusedImport
from RefRed.config import plotting


# set the default backend to be compatible with Qt in case someone uses pylab from IPython console
def _set_default_rc():
    matplotlib.rc('font', **plotting.font)
    matplotlib.rc('savefig', **plotting.savefig)
_set_default_rc()

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'default', ['#0000ff', '#00ff00', '#ffff00', '#ff0000', '#bd7efc', '#000000'], N=256
)
matplotlib.cm.register_cmap('default', cmap=cmap)

# set the default backend to be compatible with Qt in case someone uses pylab from IPython console
def set_matplotlib_backend():
    '''MUST be called before anything tries to use matplotlib

    This will set the backend if it hasn't been already. It also returns
    the name of the backend to be the name to be used for importing the
    correct matplotlib widgets.'''
    backend = matplotlib.get_backend()
    if backend.startswith('module://'):
        if backend.endswith('qt4agg'):
            backend = 'Qt4Agg'
        elif backend.endswith('workbench') or backend.endswith('qt5agg'):
            backend = 'Qt5Agg'
    else:
        from qtpy import PYQT4, PYQT5  # noqa
        if PYQT5:
            backend = 'Qt5Agg'
        elif PYQT4:
            backend = 'Qt4Agg'
        else:
            raise RuntimeError('Do not know which matplotlib backend to set')
        matplotlib.use(backend)
    return backend

BACKEND = set_matplotlib_backend()
if BACKEND == 'Qt4Agg':
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
elif BACKEND == 'Qt5Agg':
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

try:
    import matplotlib.backends.qt4_editor.figureoptions as figureoptions
except ImportError:
    figureoptions = None