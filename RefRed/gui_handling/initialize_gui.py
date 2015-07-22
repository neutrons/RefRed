from PyQt4 import QtGui, QtCore

from ..version import str_version, window_title

#from export_stitching_ascii_settings import ExportStitchingAsciiSettings
#from .gui_utils import DelayedTrigger
#from init_file_menu import InitFileMenu
#from reduced_config_files_handler import ReducedConfigFilesHandler
#from all_plot_axis import AllPlotAxis

class InitializeGui(object):
	
	parent = None
	
	def __init__(self, parent):
		
		self.parent = parent
		
		self.set_gui_title()
		self.set_statusbar()
		self.set_table_labels()
		
		##set up the header of the big table
		#verticalHeader = ["Data Run #",u'2\u03b8 (\u00B0)',u'\u03bbmin(\u00c5)',
			          #u'\u03bbmax (\u00c5)',u'Qmin (1/\u00c5)',u'Qmax (1/\u00c5)',
			          #'Norm. Run #']
		#parent.ui.reductionTable.setHorizontalHeaderLabels(verticalHeader)
		#parent.ui.reductionTable.resizeColumnsToContents()
		## define the context menu of the recap table
		##parent.ui.reductionTable.horizontalHeader().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
##		parent.ui.reductionTable.horizontalHeader().customContextMenuRequested.connect(parent.handleReductionTableMenu)
	    
		## set up the header of the scaling factor table
		#verticalHeader = ["Data Run #","SF: auto","SF: manual","SF: 1"]
		#parent.ui.dataStitchingTable.setHorizontalHeaderLabels(verticalHeader)
		#parent.ui.dataStitchingTable.resizeColumnsToContents()
		
		#palette_green = QtGui.QPalette()
		#palette_green.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
		#parent.ui.sf_found_label.setPalette(palette_green)
		
		#palette_red = QtGui.QPalette()
		#palette_red.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
		#parent.ui.sf_not_found_label.setPalette(palette_red)
	    
		## set up header for reduced ascii table
		#verticalHeader = ["ASCII files", "Active"]
		#parent.ui.reducedAsciiDataSetTable.setHorizontalHeaderLabels(verticalHeader)
		#parent.ui.reducedAsciiDataSetTable.setColumnWidth(0,249)
		#parent.ui.reducedAsciiDataSetTable.setColumnWidth(1,49)
	    
		#parent.exportStitchingAsciiSettings = ExportStitchingAsciiSettings()
	    
		#parent.ui.plotTab.setCurrentIndex(0)
		## start a separate thread for delayed actions
		#parent.trigger=DelayedTrigger()
		#parent.trigger.activate.connect(parent.processDelayedTrigger)
		#parent.trigger.start()
		
		#self.defineRightDefaultPath()
		#self.initFileMenu()
		#self.initAutoPeakBackFinderWidgets(parent)
		#self.initPrimaryFractionRangeWidgets(parent)
		#parent.reducedFilesLoadedObject = ReducedConfigFilesHandler(parent)
		#self.initConfigGui()
		#self.initErrorWidgets()
		#parent.allPlotAxis = AllPlotAxis()
		
		#parent.ui.numberSearchEntry.setFocus()

	#def 	initPrimaryFractionRangeWidgets(self, parent):
		#parent.ui.dataPrimaryFractionFlag.setVisible(False)
		#parent.ui.dataPrimToLabel.setVisible(False)
		#parent.ui.dataPrimFromLabel.setVisible(False)
		#parent.ui.dataPrimToValue.setVisible(False)
		#parent.ui.dataPrimFromValue.setVisible(False)
		#parent.ui.dataPrimToError.setVisible(False)
		#parent.ui.dataPrimFromError.setVisible(False)
		
	#def initAutoPeakBackFinderWidgets(self, parent):
		#parent.ui.actionAutomaticPeakFinder.setVisible(False)
		#parent.ui.label.setVisible(False)
		#parent.ui.label_10.setVisible(False)
		#parent.ui.label_11.setVisible(False)
		#parent.ui.autoBackSelectionWidth.setVisible(False)
		#parent.ui.findPeakBack.setVisible(False)
		#parent.ui.autoTofFlag.setVisible(False)
		#parent.ui.autoPeakBackSelectionFrame.setVisible(False)

	#def defineRightDefaultPath(self):
		#import socket
		#if socket.gethostname() == 'lrac.sns.gov': #TODO HARDCODED STRING
			#self.parent.path_config = '/SNS/REF_L/' #TODO HARDCODED INSTRUMENT
			#self.parent.path_ascii = '/SNS/REF_L' #TODO HARDCODED INSTRUMENT
		
	#def initFileMenu(self):
		#self.parent.fileMenuObject = InitFileMenu(self.parent)
		
	#def initConfigGui(self):
		#from quicknxs.config import refllastloadedfiles
		#refllastloadedfiles.switch_config('config_files')
		#if refllastloadedfiles.config_files_path != '':
			#self.parent.path_config =  refllastloadedfiles.config_files_path
		
	#def initErrorWidgets(self):  
		#parent = self.parent
		#palette = QtGui.QPalette()
		#palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
		#parent.ui.data_peak1_error.setVisible(False)
		#parent.ui.data_peak1_error.setPalette(palette)
		#parent.ui.data_peak2_error.setVisible(False)
		#parent.ui.data_peak2_error.setPalette(palette)
		#parent.ui.data_back1_error.setVisible(False)
		#parent.ui.data_back1_error.setPalette(palette)
		#parent.ui.data_back2_error.setVisible(False)
		#parent.ui.data_back2_error.setPalette(palette)
		#parent.ui.norm_peak1_error.setVisible(False)
		#parent.ui.norm_peak1_error.setPalette(palette)
		#parent.ui.norm_peak2_error.setVisible(False)
		#parent.ui.norm_peak2_error.setPalette(palette)
		#parent.ui.norm_back1_error.setVisible(False)
		#parent.ui.norm_back1_error.setPalette(palette)
		#parent.ui.norm_back2_error.setVisible(False)
		#parent.ui.norm_back2_error.setPalette(palette)
		#parent.ui.data_selection_error_label.setVisible(False)
		#parent.ui.data_selection_error_label.setPalette(palette)
		#parent.ui.norm_selection_error_label.setVisible(False)
		#parent.ui.norm_selection_error_label.setPalette(palette)
		
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

	def set_table_labels(self):
		''' Define the labels of the main reduction table '''
		parent = self.parent
		
		vertical_header = ["",
		                  "Data Run #",
		                  "Norm. Run #",
		                  u'2\u03b8 (\u00B0)',
		                  u'\u03bbmin(\u00c5)',
			          u'\u03bbmax (\u00c5)',
		                  u'Qmin (1/\u00c5)',
		                  u'Qmax (1/\u00c5)']

		parent.ui.reductionTable.setHorizontalHeaderLabels(vertical_header)
		parent.ui.reductionTable.resizeColumnsToContents()

		column_widths = [40, 120, 120, 80, 80, 80, 80, 80]
		for index, width in enumerate(column_widths):
			parent.ui.reductionTable.setColumnWidth(index, width)
