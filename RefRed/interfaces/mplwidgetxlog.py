from qtpy import QtCore, QtGui, QtWidgets
from matplotlib.cbook import Stack
from matplotlib.colors import LogNorm
from RefRed.interfaces.mplwidgets import set_matplotlib_backend, MplCanvasMine, NavigationToolbarMine


BACKEND = set_matplotlib_backend()


class MPLWidgetXLog(QtWidgets.QWidget):
    cplot = None
    cbar = None

    logtogx = QtCore.Signal(str)
    # logtogy = QtCore.Signal(str)
    singleClick = QtCore.Signal(bool)
    leaveFigure = QtCore.Signal()

    def __init__(self, parent=None, with_toolbar=True, coordinates=False):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvasMine()

        self.canvas.ax2 = None
        self.vbox = QtWidgets.QVBoxLayout()
        if BACKEND == 'Qt4Agg':
            self.vbox.setMargin(1)
        self.vbox.addWidget(self.canvas)
        if with_toolbar:
            self.toolbar = NavigationToolbarMine(self.canvas, self, with_logX=True, with_logY=False)
            self.toolbar.coordinates = coordinates
            self.vbox.addWidget(self.toolbar)
            self.toolbar.logtogy.connect(self.logtoggle)
        else:
            self.toolbar = None
        self.setLayout(self.vbox)
        self.canvas.trigger_click.connect(self._singleClick)
        self.canvas.trigger_figure_left.connect(self._leaveFigure)

    def _singleClick(self):
        status = self.toolbar.isPanActivated or self.toolbar.isZoomActivated
        self.singleClick.emit(status)

    def _leaveFigure(self):
        #    status = self.toolbar.isPanActivated or self.toolbar.isZoomActivated
        self.leaveFigure.emit()

    def logtoggle(self, status):
        self.logtogx.emit(status)

    def leaveEvent(self, event):
        '''
        Make sure the cursor is reset to it's default when leaving the widget.
        In some cases the zoom cursor does not reset when leaving the plot.
        '''
        if self.toolbar:
            QtWidgets.QApplication.restoreOverrideCursor()
            self.toolbar._lastCursor = None
        return QtWidgets.QWidget.leaveEvent(self, event)

    def set_config(self, config):
        self.canvas.fig.subplots_adjust(**config)

    def get_config(self):
        spp = self.canvas.fig.subplotpars
        config = dict(left=spp.left, right=spp.right, bottom=spp.bottom, top=spp.top)
        return config

    def draw(self):
        '''
        Convenience to redraw the graph.
        '''
        self.canvas.draw()

    def plot(self, *args, **opts):
        '''
        Convenience wrapper for self.canvas.ax.plot
        '''
        return self.canvas.ax.plot(*args, **opts)

    def semilogy(self, *args, **opts):
        '''
        Convenience wrapper for self.canvas.ax.semilogy
        '''
        return self.canvas.ax.semilogy(*args, **opts)

    def errorbar(self, *args, **opts):
        '''
        Convenience wrapper for self.canvas.ax.semilogy
        '''
        return self.canvas.ax.errorbar(*args, **opts)

    def pcolormesh(self, datax, datay, dataz, log=False, imin=None, imax=None, update=False, **opts):
        '''
        Convenience wrapper for self.canvas.ax.plot
        '''
        if self.cplot is None or not update:
            if log:
                self.cplot = self.canvas.ax.pcolormesh(datax, datay, dataz, norm=LogNorm(imin, imax), **opts)
            else:
                self.cplot = self.canvas.ax.pcolormesh(datax, datay, dataz, **opts)
        else:
            self.update(datax, datay, dataz)
        return self.cplot

    def imshow(self, data, log=False, imin=None, imax=None, update=True, **opts):
        '''
        Convenience wrapper for self.canvas.ax.plot
        '''
        if self.cplot is None or not update:
            if log:
                self.cplot = self.canvas.ax.imshow(data, norm=LogNorm(imin, imax), **opts)
            else:
                self.cplot = self.canvas.ax.imshow(data, **opts)
        else:
            self.update(data, **opts)
        return self.cplot

    def set_title(self, new_title):
        return self.canvas.ax.title.set_text(new_title)

    def set_xlabel(self, label):
        return self.canvas.ax.set_xlabel(label)

    def set_ylabel(self, label):
        return self.canvas.ax.set_ylabel(label)

    def set_xscale(self, scale):
        try:
            return self.canvas.ax.set_xscale(scale)
        except ValueError:
            pass

    def set_yscale(self, scale):
        try:
            return self.canvas.ax.set_yscale(scale)
        except ValueError:
            pass

    def clear_fig(self):
        self.cplot = None
        self.cbar = None
        self.canvas.fig.clear()
        self.canvas.ax = self.canvas.fig.add_subplot(111, sharex=None, sharey=None)

    def clear(self):
        self.cplot = None
        self.canvas.ax.clear()
        if self.canvas.ax2 is not None:
            self.canvas.ax2.clear()

    def update(self, *data, **opts):
        self.cplot.set_data(*data)
        self.toolbar.update(*data, **opts)
        if 'extent' in opts:
            self.cplot.set_extent(opts['extent'])
            if BACKEND == 'Qt4Agg':
                oldviews = self.toolbar._views
            else:
                oldviews = []
            if BACKEND == 'Qt4Agg' and self.toolbar._views:
                # set the new extent as home for the new data
                newviews = Stack()
                newviews.push([tuple(opts['extent'])])
                for item in oldviews[1:]:
                    newviews.push(item)
                self.toolbar._views = newviews
            if not oldviews or oldviews[oldviews._pos] == oldviews[0]:
                self.canvas.ax.set_xlim(opts['extent'][0], opts['extent'][1])
                self.canvas.ax.set_ylim(opts['extent'][2], opts['extent'][3])

    def legend(self, *args, **opts):
        return self.canvas.ax.legend(*args, **opts)

    def adjust(self, **adjustment):
        return self.canvas.fig.subplots_adjust(**adjustment)
