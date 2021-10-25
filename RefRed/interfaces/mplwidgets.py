#!/usr/bin/env python
import os
import tempfile
from qtpy import QtCore, QtGui, QtWidgets
import matplotlib.cm
import matplotlib.colors
from matplotlib.colors import LogNorm, Normalize
from RefRed.config import plotting
from matplotlib.figure import Figure


# set the default backend to be compatible with Qt in case someone uses pylab from IPython console
def _set_default_rc():
    matplotlib.rc("font", **plotting.font)
    matplotlib.rc("savefig", **plotting.savefig)


_set_default_rc()

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    "default", ["#0000ff", "#00ff00", "#ffff00", "#ff0000", "#bd7efc", "#000000"], N=256
)
matplotlib.cm.register_cmap("default", cmap=cmap)


# set the default backend to be compatible with Qt in case someone uses pylab from IPython console
def set_matplotlib_backend():
    """MUST be called before anything tries to use matplotlib

    This will set the backend if it hasn't been already. It also returns
    the name of the backend to be the name to be used for importing the
    correct matplotlib widgets."""
    backend = matplotlib.get_backend()
    if backend.startswith("module://"):
        if backend.endswith("qt4agg"):
            backend = "Qt4Agg"
        elif backend.endswith("workbench") or backend.endswith("qt5agg"):
            backend = "Qt5Agg"
    else:
        from qtpy import PYQT4, PYQT5  # noqa

        if PYQT5:
            backend = "Qt5Agg"
        elif PYQT4:
            backend = "Qt4Agg"
        else:
            raise RuntimeError("Do not know which matplotlib backend to set")
        matplotlib.use(backend)
    return backend


BACKEND = set_matplotlib_backend()
if BACKEND == "Qt4Agg":
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
elif BACKEND == "Qt5Agg":
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
    from matplotlib.cbook import Stack

# path where all of the icons are
ICON_DIR = os.path.join(os.path.split(__file__)[0], "../", "icons")


def getIcon(filename: str) -> "QtGui.QIcon":
    filename_full = os.path.join(ICON_DIR, filename)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(filename_full), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return icon


class NavigationToolbar(NavigationToolbar2QT):
    """
    A small change to the original navigation toolbar.
    """

    _auto_toggle = False
    logtogx = QtCore.Signal(str)
    logtogy = QtCore.Signal(str)
    homeClicked = QtCore.Signal()
    exportClicked = QtCore.Signal()

    isCursorNormal = True

    isPanActivated = False
    isZoomActivated = False

    home_settings = None

    ylog = True
    xlog = False

    def __init__(
        self, canvas, parent, coordinates=False, with_logX=False, with_logY=False
    ):
        # these properties must be set before parent constructor is called
        # which automatically runs self._init_toolbar()
        self._with_logX = with_logX
        self._with_logY = with_logY
        NavigationToolbar2QT.__init__(self, canvas, parent, coordinates)
        self.setIconSize(QtCore.QSize(20, 20))
        #
        self.setup_toolbar()

    def _init_toolbar(self):
        pass

    def setup_toolbar(self):
        if not hasattr(self, "_actions"):
            self._actions = {}
        if BACKEND == "Qt4Agg":
            self.basedir = os.path.join(matplotlib.rcParams["datapath"], "images")

        icon = getIcon("zoom-previous.png")
        a = self.addAction(icon, "Back", self.back)
        a.setToolTip("Back to previous view")

        icon = getIcon("zoom-next.png")
        a = self.addAction(icon, "Forward", self.forward)
        a.setToolTip("Forward to next view")

        self.addSeparator()

        icon = getIcon("transform-move.png")
        a = self.addAction(icon, "Pan", self.pan)
        a.setToolTip("Pan axes with left mouse, zoom with right")
        a.setCheckable(True)
        self._actions["pan"] = a

        icon = getIcon("zoom-select.png")
        a = self.addAction(icon, "Zoom", self.zoom)
        a.setToolTip("Zoom to rectangle")
        a.setCheckable(True)
        self._actions["zoom"] = a

        self.addSeparator()

        icon = getIcon("edit-guides.png")
        a = self.addAction(icon, "Subplots", self.configure_subplots)
        a.setToolTip("Configure plot boundaries")

        icon = getIcon("document-save.png")
        a = self.addAction(icon, "Save", self.save_figure)
        a.setToolTip("Save the figure")

        icon = getIcon("document-print.png")
        a = self.addAction(icon, "Print", self.print_figure)
        a.setToolTip("Print the figure with the default printer")

        icon = getIcon("export_ascii.png")
        a = self.addAction(icon, "Export", self.export_ascii)
        a.setToolTip("Export the plot into ASCII file")

        if self._with_logY:
            icon = getIcon("toggle-log.png")
            a = self.addAction(icon, "Log", self.toggle_ylog)
            a.setToolTip("Toggle logarithmic y scale")

            self.addSeparator()

        if self._with_logX:
            icon = getIcon("toggle-xlog.png")
            a = self.addAction(icon, "Log", self.toggle_xlog)
            a.setToolTip("Toggle logarithmic x scale")

            self.addSeparator()

        self.buttons = {}

        # Add the x,y location widget at the right side of the toolbar
        # The stretch factor is 1 which means any resizing of the toolbar
        # will resize this label instead of the buttons.
        self.locLabel = QtWidgets.QLabel("", self)
        self.locLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.locLabel.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored
            )
        )
        self.labelAction = self.addWidget(self.locLabel)
        if self.coordinates:
            self.labelAction.setVisible(True)
        else:
            self.labelAction.setVisible(False)

        # reference holder for subplots_adjust window
        self.adj_window = None

    def activate_widget(self, widget_name, activateIt):

        if widget_name == "pan":
            if activateIt:
                self.isPanActivated = True
                self.isZoomActivated = False
            else:
                self.isPanActivated = False
        elif widget_name == "zoom":
            if activateIt:
                self.isZoomActivated = True
                self.isPanActivated = False
            else:
                self.isZoomActivated = False

    def home(self, *args):
        NavigationToolbar2QT.home(self, *args)
        self.homeClicked.emit()

    def pan(self, *args):
        NavigationToolbar2QT.pan(self, *args)
        self.activate_widget("pan", not self.isPanActivated)

    def zoom(self, *args):
        NavigationToolbar2QT.zoom(self, *args)
        self.activate_widget("zoom", not self.isZoomActivated)

    # def logtoggle(self, checked):
    # print 'inside mplwidgetxlog logtoggle'
    # self.logtog.emit(checked)

    def export_ascii(self):
        self.exportClicked.emit()

    def print_figure(self):
        """
        Save the plot to a temporary png file and show a preview dialog also used for printing.
        """
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = list(filetypes.items())
        sorted_filetypes.sort()

        filename = os.path.join(tempfile.gettempdir(), "quicknxs_print.png")
        self.canvas.print_figure(filename, dpi=600)
        imgpix = QtGui.QPixmap(filename)
        os.remove(filename)

        imgobj = QtWidgets.QLabel()
        imgobj.setPixmap(imgpix)
        imgobj.setMask(imgpix.mask())
        imgobj.setGeometry(0, 0, imgpix.width(), imgpix.height())

        def getPrintData(printer):
            imgobj.render(printer)

        printer = QtGui.QPrinter()
        printer.setPrinterName("mrac4a_printer")
        printer.setPageSize(QtGui.QPrinter.Letter)
        printer.setResolution(600)
        printer.setOrientation(QtGui.QPrinter.Landscape)

        pd = QtGui.QPrintPreviewDialog(printer)
        pd.paintRequested.connect(getPrintData)
        pd.exec_()

    def save_figure(self, *args):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = list(filetypes.items())
        sorted_filetypes.sort()
        default_filetype = self.canvas.get_default_filetype()

        start = "image." + default_filetype
        filters = []
        for name, exts in sorted_filetypes:
            exts_list = " ".join(["*.%s" % ext for ext in exts])
            filter_ = "%s (%s)" % (name, exts_list)
            if default_filetype in exts:
                filters.insert(0, filter_)
            else:
                filters.append(filter_)
        filters = ";;".join(filters)
        caption = "Choose a filename to save to"
        figname, filters = QtWidgets.QFileDialog.getSaveFileName(
            self,
            caption,
            start,
            filters,
        )

        if figname:
            try:
                self.canvas.print_figure(str(figname))
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Error saving file",
                    str(e),
                    QtWidgets.QMessageBox.Ok,
                    QtGui.QMessageBox.NoButton,
                )

    def toggle_ylog(self, *args):
        ax = self.canvas.ax
        if len(ax.images) == 0 and all(
            [c.__class__.__name__ != "QuadMesh" for c in ax.collections]
        ):

            #      logstate=ax.get_xscale()
            if self.ylog:
                ax.set_yscale("linear")
            else:
                ax.set_yscale("log")
            self.ylog = not self.ylog

            self.canvas.draw_idle()
            self.logtogy.emit(ax.get_yscale())
        else:
            imgs = ax.images + [
                c for c in ax.collections if c.__class__.__name__ == "QuadMesh"
            ]
            norm = imgs[0].norm
            if norm.__class__ is LogNorm:
                for img in imgs:
                    img.set_norm(Normalize(norm.vmin, norm.vmax))
                else:
                    for img in imgs:
                        img.set_norm(LogNorm(norm.vmin, norm.vmax))
        self.canvas.draw_idle()

    def toggle_xlog(self, *args):
        ax = self.canvas.ax
        if len(ax.images) == 0 and all(
            [c.__class__.__name__ != "QuadMesh" for c in ax.collections]
        ):

            if self.xlog:
                ax.set_xscale("linear")
            else:
                ax.set_xscale("log")
            self.xlog = not self.xlog

            self.canvas.draw_idle()
            self.logtogx.emit(ax.get_xscale())
        else:
            imgs = ax.images + [
                c for c in ax.collections if c.__class__.__name__ == "QuadMesh"
            ]
            norm = imgs[0].norm
            if norm.__class__ is LogNorm:
                for img in imgs:
                    img.set_norm(Normalize(norm.vmin, norm.vmax))
                else:
                    for img in imgs:
                        img.set_norm(LogNorm(norm.vmin, norm.vmax))
        self.canvas.draw_idle()


class MplCanvas(FigureCanvas):

    trigger_click = QtCore.Signal(bool, bool, int, int)
    trigger_figure_left = QtCore.Signal()

    def __init__(
        self,
        parent=None,
        width=3,
        height=3,
        dpi=100,
        sharex=None,
        sharey=None,
        adjust={},
    ):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot(111, sharex=sharex, sharey=sharey)
        self.fig.subplots_adjust(left=0.15, bottom=0.1, right=0.95, top=0.95)
        self.xtitle = ""
        self.ytitle = ""
        self.PlotTitle = ""
        self.grid_status = True
        self.xaxis_style = "linear"
        self.yaxis_style = "linear"
        self.format_labels()
        FigureCanvas.__init__(self, self.fig)
        # self.fc = FigureCanvas(self.fig)
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

        self.fig.canvas.mpl_connect("button_press_event", self.button_pressed)
        self.fig.canvas.mpl_connect("figure_leave_event", self.figure_leave)

    def button_pressed(self, event):
        is_x_axis_manual_zoom_requested = False
        is_manual_zoom_requested = False

        if event.button == 3:
            is_manual_zoom_requested = True
            if event.xdata is None:
                x = event.x
                y = event.y
                if x > y:
                    is_x_axis_manual_zoom_requested = True
                else:
                    is_x_axis_manual_zoom_requested = False
            else:
                is_manual_zoom_requested = False

        mouse_x = event.x
        mouse_y = event.y
        self.trigger_click.emit(
            is_manual_zoom_requested, is_x_axis_manual_zoom_requested, mouse_x, mouse_y
        )  # button pressed

    def figure_leave(self, event):
        self.trigger_figure_left.emit()

    def format_labels(self):
        self.ax.set_title(self.PlotTitle)

    def sizeHint(self):
        w, h = self.get_width_height()
        w = max(w, self.height())
        h = max(h, self.width())
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(40, 40)

    def get_default_filetype(self):
        return "png"


class MPLWidgetMine(QtWidgets.QWidget):
    cplot = None
    cbar = None

    logtogx = QtCore.Signal(str)
    logtogy = QtCore.Signal(str)
    singleClick = QtCore.Signal(bool, int, bool, int, int)
    leaveFigure = QtCore.Signal()

    def __init__(
        self,
        parent=None,
        with_toolbar=True,
        coordinates=False,
        with_logX=False,
        with_logY=False,
    ):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()

        self.canvas.ax2 = None
        self.vbox = QtWidgets.QVBoxLayout()
        if BACKEND == "Qt4Agg":
            self.vbox.setMargin(1)
        self.vbox.addWidget(self.canvas)
        if with_toolbar:
            self.toolbar = NavigationToolbar(
                self.canvas, self, with_logX=with_logX, with_logY=with_logY
            )
            self.toolbar.coordinates = coordinates
            self.vbox.addWidget(self.toolbar)
            self.toolbar.logtogx.connect(self.logtogglex)
            self.toolbar.logtogy.connect(self.logtoggley)
        else:
            self.toolbar = None
        self.setLayout(self.vbox)
        self.canvas.trigger_click.connect(self._singleClick)
        self.canvas.trigger_figure_left.connect(self._leaveFigure)

    def _singleClick(
        self,
        is_manual_zoom_requested,
        is_x_axis_manual_zoom_requested,
        mouse_x,
        mouse_y,
    ):
        status = self.toolbar.isPanActivated or self.toolbar.isZoomActivated
        self.singleClick.emit(
            status,
            is_manual_zoom_requested,
            is_x_axis_manual_zoom_requested,
            mouse_x,
            mouse_y,
        )

    def _leaveFigure(self):
        self.leaveFigure.emit()

    def logtogglex(self, status):
        self.logtogx.emit(status)

    def logtoggley(self, status):
        self.logtogy.emit(status)

    def leaveEvent(self, event):
        """
        Make sure the cursor is reset to it's default when leaving the widget.
        In some cases the zoom cursor does not reset when leaving the plot.
        """
        # if self.toolbar:
        #     QtWidgets.QApplication.restoreOverrideCursor()
        #     self.toolbar._lastCursor = None
        return QtWidgets.QWidget.leaveEvent(self, event)

    def set_config(self, config):
        self.canvas.fig.subplots_adjust(**config)

    def get_config(self):
        spp = self.canvas.fig.subplotpars
        config = dict(left=spp.left, right=spp.right, bottom=spp.bottom, top=spp.top)
        return config

    def draw(self):
        """
        Convenience to redraw the graph.
        """
        if self.canvas.ax.has_data():
            self.canvas.draw_idle()

    def plot(self, *args, **opts):
        """
        Convenience wrapper for self.canvas.ax.plot
        """
        return self.canvas.ax.plot(*args, **opts)

    def semilogy(self, *args, **opts):
        """
        Convenience wrapper for self.canvas.ax.semilogy
        """
        return self.canvas.ax.semilogy(*args, **opts)

    def errorbar(self, *args, **opts):
        """
        Convenience wrapper for self.canvas.ax.semilogy
        """
        return self.canvas.ax.errorbar(*args, **opts)

    def pcolormesh(
        self, datax, datay, dataz, log=False, imin=None, imax=None, update=False, **opts
    ):
        """
        Convenience wrapper for self.canvas.ax.plot
        """
        if self.cplot is None or not update:
            if log:
                self.cplot = self.canvas.ax.pcolormesh(
                    datax, datay, dataz, norm=LogNorm(imin, imax), **opts
                )
            else:
                self.cplot = self.canvas.ax.pcolormesh(datax, datay, dataz, **opts)
        else:
            self.update(datax, datay, dataz)
        return self.cplot

    def imshow(self, data, log=False, imin=None, imax=None, update=True, **opts):
        """
        Convenience wrapper for self.canvas.ax.plot
        """
        if self.cplot is None or not update:
            if log:
                self.cplot = self.canvas.ax.imshow(
                    data, norm=LogNorm(imin, imax), **opts
                )
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
        if "extent" in opts:
            self.cplot.set_extent(opts["extent"])
            if BACKEND == "Qt4Agg":
                oldviews = self.toolbar._views
            else:
                oldviews = []
            if BACKEND == "Qt4Agg" and self.toolbar._views:
                # set the new extent as home for the new data
                newviews = Stack()
                newviews.push([tuple(opts["extent"])])
                for item in oldviews[1:]:
                    newviews.push(item)
                self.toolbar._views = newviews
            if not oldviews or oldviews[oldviews._pos] == oldviews[0]:
                self.canvas.ax.set_xlim(opts["extent"][0], opts["extent"][1])
                self.canvas.ax.set_ylim(opts["extent"][2], opts["extent"][3])

    def legend(self, *args, **opts):
        return self.canvas.ax.legend(*args, **opts)

    def adjust(self, **adjustment):
        return self.canvas.fig.subplots_adjust(**adjustment)


# Custom subclasses to get around the fact that qtcreator isn't making it easy to pass arguments to the constructor
class MPLWidgetNoLog(MPLWidgetMine):
    def __init__(self, parent=None, with_toolbar=True, coordinates=False):
        super().__init__(
            parent=parent,
            with_toolbar=with_toolbar,
            coordinates=coordinates,
            with_logX=False,
            with_logY=False,
        )


class MPLWidgetXLog(MPLWidgetMine):
    def __init__(self, parent=None, with_toolbar=True, coordinates=False):
        super().__init__(
            parent=parent,
            with_toolbar=with_toolbar,
            coordinates=coordinates,
            with_logX=True,
            with_logY=False,
        )


class MPLWidget(MPLWidgetMine):
    def __init__(self, parent=None, with_toolbar=True, coordinates=False):
        super().__init__(
            parent=parent,
            with_toolbar=with_toolbar,
            coordinates=coordinates,
            with_logX=False,
            with_logY=True,
        )


class MPLWidgetXLogYLog(MPLWidgetMine):
    def __init__(self, parent=None, with_toolbar=True, coordinates=False):
        super().__init__(
            parent=parent,
            with_toolbar=with_toolbar,
            coordinates=coordinates,
            with_logX=True,
            with_logY=True,
        )
