from qtpy import QtGui, QtCore, QtWidgets

import socket

from RefRed import WINDOW_TITLE
from RefRed.plot.all_plot_axis import AllPlotAxis
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.gui_handling.update_plot_widget_status import UpdatePlotWidgetStatus


class Gui(object):

    parent = None
    vertical_header = [
        "Plotted",
        "Data Run #",
        "Norm. Run #",
        "2\u03b8 (\u00B0)",
        "\u03bbmin (\u00c5)",
        "\u03bbmax (\u00c5)",
        "Qmin (1/\u00c5)",
        "Qmax (1/\u00c5)",
        "Comments",
    ]
    column_widths = [60, 200, 200, 65, 85, 85, 95, 95, 400]
    stitching_column_widths = [150, 60, 60]
    gui_size_coeff = 2.0 / 3.0

    def __init__(self, parent):

        self.parent = parent
        self.set_gui_title()
        self.set_gui_size()
        self.set_statusbar()
        self.set_main_table()
        self.set_stiching_table()
        self.set_reduced_table()
        self.set_default_path()
        self.init_error_label_widgets()
        parent.allPlotAxis = AllPlotAxis()

        # enabled all widgets
        o_update_plot = UpdatePlotWidgetStatus(parent=parent)
        o_update_plot.disable_all()

        parent.ui.reductionTable.setCurrentCell(0, 1)
        parent.ui.data_sequence_lineEdit.setFocus()

        self.init_autopopulate_widgets()

        o_gui = GuiUtility(parent=self.parent)
        o_gui.init_widgets_value()

        # This is the angle offset box, which is no longer needed
        # but kept for advanced usage
        self.parent.ui.angleOffsetError.setVisible(False)
        self.parent.ui.offset_pm.setVisible(False)
        self.parent.ui.sf_button.setChecked(True)

        # Select the `DATA` tab as the currently active one
        self.parent.ui.dataNormTabWidget.setCurrentIndex(0)  # 0: DATA, 1: NORMALIZATION

    def init_autopopulate_widgets(self):
        pixmap = QtGui.QPixmap(":/General/check_icon.png")
        self.parent.ui.check1.setFixedWidth(25)
        self.parent.ui.check1.setFixedHeight(25)
        self.parent.ui.check1.setPixmap(pixmap)
        self.parent.ui.check1.setVisible(False)
        self.parent.ui.check2.setFixedWidth(25)
        self.parent.ui.check2.setFixedHeight(25)
        self.parent.ui.check2.setPixmap(pixmap)
        self.parent.ui.check2.setVisible(False)
        self.parent.ui.check3.setFixedWidth(25)
        self.parent.ui.check3.setFixedHeight(25)
        self.parent.ui.check3.setPixmap(pixmap)
        self.parent.ui.check3.setVisible(False)
        self.parent.ui.check4.setFixedWidth(25)
        self.parent.ui.check4.setFixedHeight(25)
        self.parent.ui.check4.setPixmap(pixmap)
        self.parent.ui.check4.setVisible(False)
        self.parent.ui.check5.setFixedWidth(25)
        self.parent.ui.check5.setFixedHeight(25)
        self.parent.ui.check5.setPixmap(pixmap)
        self.parent.ui.check5.setVisible(False)

        self.parent.ui.progressBar_check2.setVisible(False)
        self.parent.ui.progressBar_check3.setVisible(False)
        self.parent.ui.progressBar_check4.setVisible(False)
        self.parent.ui.progressBar_check5.setVisible(False)

        self.parent.ui.frame_autofill_check_status.setVisible(False)
        self.parent.ui.frame_reduction.setVisible(False)

    def set_gui_title(self):
        """Define the raw title of the main window"""
        parent = self.parent

        # title = window_title
        parent.setWindowTitle("%s%s" % (WINDOW_TITLE, "~/tmp.xml"))

    def set_gui_size(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.parent.setGeometry(
            50,
            50,
            int(self.gui_size_coeff * screen.width()),
            int(self.gui_size_coeff * screen.height()),
        )

    def set_statusbar(self):
        """Add the statusbar widgets"""
        parent = self.parent

        parent.eventProgress = QtWidgets.QProgressBar(parent.ui.statusbar)
        parent.eventProgress.setMinimumSize(20, 14)
        parent.eventProgress.setMaximumSize(140, 100)
        parent.eventProgress.setVisible(False)
        parent.ui.statusbar.addPermanentWidget(parent.eventProgress)

    def set_main_table(self):
        """Define the labels and size of the main reduction table"""
        parent = self.parent

        vertical_header = self.vertical_header

        parent.ui.reductionTable.setHorizontalHeaderLabels(vertical_header)
        parent.ui.reductionTable.resizeColumnsToContents()

        column_widths = self.column_widths
        for index, width in enumerate(column_widths):
            parent.ui.reductionTable.setColumnWidth(index, width)

        for row_index in range(self.parent.REDUCTIONTABLE_MAX_ROWCOUNT):
            for col_index in range(len(self.column_widths)):
                if col_index == 0:
                    _widget = QtWidgets.QCheckBox()
                    _widget.setChecked(False)
                    _widget.setEnabled(True)
                    # action to take when a checkbox is either unchecked (state==0) or checked (state==2)
                    _signal_func = lambda state=0, row=row_index: self.parent.reduction_table_visibility_changed_test(  # noqa: E501, E731
                        state, row
                    )
                    _widget.stateChanged.connect(_signal_func)

                    parent.ui.reductionTable.setCellWidget(row_index, col_index, _widget)
                elif (col_index == 1) or (col_index == 2):
                    _item = QtWidgets.QTableWidgetItem()
                    _flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
                    _item.setFlags(_flags)
                    parent.ui.reductionTable.setItem(row_index, col_index, _item)

                else:
                    _item = QtWidgets.QTableWidgetItem()
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    parent.ui.reductionTable.setItem(row_index, col_index, _item)

    def set_stiching_table(self):
        """initialize the stiching table (labels, size...)"""
        parent = self.parent

        vertical_header = ["Data Run #", "SF", "Clock."]
        parent.ui.dataStitchingTable.setHorizontalHeaderLabels(vertical_header)
        # parent.ui.dataStitchingTable.resizeColumnsToContents()
        column_widths = self.stitching_column_widths
        for index, width in enumerate(column_widths):
            parent.ui.dataStitchingTable.setColumnWidth(index, width)

        palette_green = QtGui.QPalette()
        palette_green.setColor(QtGui.QPalette.Foreground, QtCore.Qt.darkGreen)
        parent.ui.sf_found_label.setPalette(palette_green)

        palette_red = QtGui.QPalette()
        palette_red.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        parent.ui.sf_not_found_label.setPalette(palette_red)

    def set_reduced_table(self):
        """initialize the reduced table from the stitching tabe"""
        parent = self.parent

        vertical_header = ["ASCII files", "Active"]
        parent.ui.reducedAsciiDataSetTable.horizontalHeader().setVisible(True)
        parent.ui.reducedAsciiDataSetTable.setHorizontalHeaderLabels(vertical_header)
        parent.ui.reducedAsciiDataSetTable.setColumnWidth(0, 240)
        parent.ui.reducedAsciiDataSetTable.setColumnWidth(1, 50)

        for row_index in range(self.parent.nbr_row_table_ascii):
            _widget = QtWidgets.QCheckBox()
            _widget.setChecked(False)
            _widget.setEnabled(True)
            _widget.stateChanged.connect(self.parent.reduced_ascii_data_set_table_visibility_changed)
            parent.ui.reducedAsciiDataSetTable.setCellWidget(row_index, 1, _widget)

    def set_default_path(self):
        """set up the default path when looking for nexus"""
        parent = self.parent

        if socket.gethostname() == "lrac.sns.gov":
            from ..config.instrument import data_base

            parent.path_ascii = data_base
        elif socket.gethostname() == "mac83978":
            from ..config.instrument import local_data_base

            parent.path_ascii = local_data_base
        print("Using database in", parent.path_ascii)

    def init_error_label_widgets(self) -> None:
        """will hide the error label by default"""
        parent: QtWidgets.QWidget = self.parent
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)  # type: ignore

        for label_text in (
            "peakFromError",
            "peakToError",
            "backFromError",
            "backToError",
            "back2FromError",
            "back2ToError",
        ):
            label: QtWidgets.QLabel = getattr(parent.ui, label_text)
            label.setVisible(False)
            label.setPalette(palette)

        parent.ui.normPeakFromError.setVisible(False)
        parent.ui.normPeakFromError.setPalette(palette)

        parent.ui.normPeakToError.setVisible(False)
        parent.ui.normPeakToError.setPalette(palette)

        parent.ui.normBackFromError.setVisible(False)
        parent.ui.normBackFromError.setPalette(palette)

        parent.ui.normBackToError.setVisible(False)
        parent.ui.normBackToError.setPalette(palette)

        parent.ui.normBack2FromError.setVisible(False)
        parent.ui.normBack2FromError.setPalette(palette)

        parent.ui.normBack2ToError.setVisible(False)
        parent.ui.normBack2ToError.setPalette(palette)

        parent.ui.data_selection_error_label.setVisible(False)
        parent.ui.data_selection_error_label.setPalette(palette)
        parent.ui.norm_selection_error_label.setVisible(False)
        parent.ui.norm_selection_error_label.setPalette(palette)
