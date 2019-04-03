from PyQt4 import QtGui
import os
from RefRed.configuration.export_xml_config import ExportXMLConfig
from RefRed.utilities import makeSureFileHasExtension
from RefRed.status_message_handler import StatusMessageHandler
from RefRed.gui_handling.gui_utility import GuiUtility


class SavingConfiguration(object):
    
    parent = None
    
    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.filename = filename

        StatusMessageHandler(parent = self.parent, 
                             message = 'Saving config ...', 
                             is_threaded = False)
        
    def run(self):
        if self.filename == '':
            _path = self.parent.path_config
            _filter = ("XML (*.xml);; All Files (*.*)")            
            self.filename = str(QtGui.QFileDialog.getSaveFileName(self.parent,
                                                         'Save Configuration File',
                                                         _path,
                                                         _filter))
            
            if self.filename == '':
                return

        self.parent.path_config = os.path.dirname(self.filename)
        self.filename = makeSureFileHasExtension(self.filename)
        o_export = ExportXMLConfig(parent = self.parent,
                                   filename = self.filename)
        
        StatusMessageHandler(parent = self.parent, 
                             message = 'Done!', 
                             is_threaded = True)
        
        o_gui_utility = GuiUtility(parent = self.parent)
        o_gui_utility.new_config_file_loaded(config_file_name = self.filename)
        o_gui_utility.gui_not_modified()

    
            
        
            
