from PyQt4 import QtGui, QtCore
import socket
import os

from RefRed.version import str_version, window_title
from RefRed.export.export_stitching_ascii_settings import ExportStitchingAsciiSettings
from file_menu import FileMenu as InitFileMenu
from RefRed.reduced_config_files_handler import ReducedConfigFilesHandler
from RefRed.plot.all_plot_axis import AllPlotAxis
#from .gui_utils import DelayedTrigger
import colors
from RefRed.gui_handling.update_plot_widget_status import UpdatePlotWidgetStatus

class Gui(object):

    parent = None
    vertical_header = ["Ploted",
                       "Data Run #",
                       "Norm. Run #",
                       u'2\u03b8 (\u00B0)',
                       u'\u03bbmin(\u00c5)',
                       u'\u03bbmax (\u00c5)',
                       u'Qmin (1/\u00c5)',
                       u'Qmax (1/\u00c5)',
                       'Comments']
    column_widths = [60, 200, 200, 65, 85, 85, 95, 95, 400]	

    def __init__(self, parent):

        self.parent = parent

        self.set_gui_title()
        self.set_statusbar()
        self.set_main_table()
        #self.set_context_menu()
        self.set_stiching_table()
        self.set_reduced_table()
        self.set_export_stitching_settings()
        self.set_default_path()
        self.init_file_menu()
        self.init_error_label_widgets()
        parent.allPlotAxis = AllPlotAxis()
        self.init_primary_fraction_range_widgets() # NEW FEATURE COMING SOON

        #enabled all widgets
        o_update_plot = UpdatePlotWidgetStatus(parent=parent)
        o_update_plot.enable_data()
        o_update_plot.enable_norm()

        ## start a separate thread for delayed actions
        #parent.trigger=DelayedTrigger()
        #parent.trigger.activate.connect(parent.processDelayedTrigger)
        #parent.trigger.start()

        parent.ui.reductionTable.setCurrentCell(0,1)
        parent.ui.reductionTable.setFocus()	
        
        self.init_autopopulate_widgets()
        
    def init_autopopulate_widgets(self):
        pixmap = QtGui.QPixmap(u':/General/check_icon.png')
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
        
        self.parent.ui.progressBar_check1.setVisible(False)
        self.parent.ui.progressBar_check2.setVisible(False)
        self.parent.ui.progressBar_check3.setVisible(False)
        self.parent.ui.progressBar_check4.setVisible(False)
        self.parent.ui.progressBar_check5.setVisible(False)
        
        self.parent.ui.frame_autofill_check_status.setVisible(False)

    def set_gui_title(self):
        ''' Define the raw title of the main window '''
        parent = self.parent

        title = window_title
        parent.setWindowTitle(u'%s   %s'%(title, str_version))
        parent.setWindowTitle(u'%s%s' %(window_title, '~/tmp.xml'))

    def set_statusbar(self):
        ''' Add the statusbar widgets '''
        parent = self.parent

        parent.eventProgress=QtGui.QProgressBar(parent.ui.statusbar)
        parent.eventProgress.setMinimumSize(20, 14)
        parent.eventProgress.setMaximumSize(140, 100)
        parent.eventProgress.setVisible(False)
        parent.ui.statusbar.addPermanentWidget(parent.eventProgress)

    def set_main_table(self):
        ''' Define the labels and size of the main reduction table '''
        parent = self.parent

        vertical_header = self.vertical_header

        parent.ui.reductionTable.setHorizontalHeaderLabels(vertical_header)
        parent.ui.reductionTable.resizeColumnsToContents()

        column_widths = self.column_widths
        for index, width in enumerate(column_widths):
            parent.ui.reductionTable.setColumnWidth(index, width)

        for row_index in range(30):
            for col_index in range(len(self.column_widths)):
                if col_index == 0:
                    _widget = QtGui.QCheckBox()
                    _widget.setChecked(False)
                    _widget.setEnabled(True)
                    signal_function = self.get_checkbox_signal_function(row_index)

                    QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"), 
                                           eval(signal_function))
                    parent.ui.reductionTable.setCellWidget(row_index, col_index, _widget)
                elif (col_index == 1) or (col_index == 2):
                    _item = QtGui.QTableWidgetItem()
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    if (col_index == 1):
                        _color = QtGui.QColor(colors.DATA_TABLE_BACKGROUND)
                        _item.setBackground(_color)
                    else:
                        _color = QtGui.QColor(colors.NORM_TABLE_BACKGROUND)
                        _item.setBackground(_color)
                    parent.ui.reductionTable.setItem(row_index, col_index, _item)

                else:
                    _item = QtGui.QTableWidgetItem()
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    parent.ui.reductionTable.setItem(row_index, col_index, _item)

    def get_checkbox_signal_function(self, row_index):
        root_function_name = 'self.parent.reduction_table_visibility_changed_' + str(row_index)
        return root_function_name

    def set_context_menu(self):
        ''' Define the context menu of the main table'''
        parent = self.parent

        parent.ui.reductionTable.horizontalHeader().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        parent.ui.reductionTable.horizontalHeader().customContextMenuRequested.connect(parent.handleReductionTableMenu)

    def set_stiching_table(self):
        ''' initialize the stiching table (labels, size...)'''
        parent = self.parent

        vertical_header = ["Data Run #","SF: auto","SF: manual","SF: 1"]
        parent.ui.dataStitchingTable.setHorizontalHeaderLabels(vertical_header)
        parent.ui.dataStitchingTable.resizeColumnsToContents()

        palette_green = QtGui.QPalette()
        palette_green.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
        parent.ui.sf_found_label.setPalette(palette_green)

        palette_red = QtGui.QPalette()
        palette_red.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        parent.ui.sf_not_found_label.setPalette(palette_red)

    def set_reduced_table(self):
        ''' initialize the reduced table from the stitching tabe '''
        parent = self.parent

        vertical_header = ["ASCII files", "Active"]
        parent.ui.reducedAsciiDataSetTable.setHorizontalHeaderLabels(vertical_header)
        parent.ui.reducedAsciiDataSetTable.setColumnWidth(0,249)
        parent.ui.reducedAsciiDataSetTable.setColumnWidth(1,49)

    def set_export_stitching_settings(self):
        ''' set up the export stitching settings '''
        parent = self.parent

        parent.exportStitchingAsciiSettings = ExportStitchingAsciiSettings()

    def set_default_path(self):
        ''' set up the default path when looking for nexus '''
        parent = self.parent

        if socket.gethostname() == 'lrac.sns.gov':
            from ..config.instrument import data_base
            parent.path_ascii = data_base
        elif socket.gethostname() == 'mac83978':
            from ..config.instrument import local_data_base			
            parent.path_ascii = local_data_base

    def init_file_menu(self):
        self.parent.fileMenuObject = InitFileMenu(self.parent)
        from ..config import refllastloadedfiles
        refllastloadedfiles.switch_config('config_files')
        if refllastloadedfiles.config_files_path != '':
            self.parent.path_config =  refllastloadedfiles.config_files_path
        self.parent.reducedFilesLoadedObject = ReducedConfigFilesHandler(self.parent)


    def init_error_label_widgets(self):
        ''' will hide the error label by default '''
        parent = self.parent
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        parent.ui.data_peak1_error.setVisible(False)
        parent.ui.data_peak1_error.setPalette(palette)
        parent.ui.data_peak2_error.setVisible(False)
        parent.ui.data_peak2_error.setPalette(palette)
        parent.ui.data_back1_error.setVisible(False)
        parent.ui.data_back1_error.setPalette(palette)
        parent.ui.data_back2_error.setVisible(False)
        parent.ui.data_back2_error.setPalette(palette)
        parent.ui.norm_peak1_error.setVisible(False)
        parent.ui.norm_peak1_error.setPalette(palette)
        parent.ui.norm_peak2_error.setVisible(False)
        parent.ui.norm_peak2_error.setPalette(palette)
        parent.ui.norm_back1_error.setVisible(False)
        parent.ui.norm_back1_error.setPalette(palette)
        parent.ui.norm_back2_error.setVisible(False)
        parent.ui.norm_back2_error.setPalette(palette)
        parent.ui.data_selection_error_label.setVisible(False)
        parent.ui.data_selection_error_label.setPalette(palette)
        parent.ui.norm_selection_error_label.setVisible(False)
        parent.ui.norm_selection_error_label.setPalette(palette)


    # NEW FEATURE COMING SOON !!!!
    def init_primary_fraction_range_widgets(self):
        ''' init the status of the new Prim1 and Prim2 widgets '''
        parent = self.parent

        parent.ui.dataPrimaryFractionFlag.setVisible(False)
        parent.ui.dataPrimToLabel.setVisible(False)
        parent.ui.dataPrimFromLabel.setVisible(False)
        parent.ui.dataPrimToValue.setVisible(False)
        parent.ui.dataPrimFromValue.setVisible(False)
        parent.ui.dataPrimToError.setVisible(False)
        parent.ui.dataPrimFromError.setVisible(False)
