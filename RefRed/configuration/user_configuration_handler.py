from PyQt4.QtCore import QSettings
import os

class RetrieveUserConfiguration(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        settings = QSettings()
        self.parent.path_ascii = str(settings.value("path_ascii", 
                                                    os.path.expanduser('~')).toString())
        print('path_ascii: ' , self.parent.path_ascii)
        self.parent.path_config = str(settings.value("path_config", 
                                                    os.path.expanduser('~')).toString())
        
class SaveUserConfiguration(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        print('path_ascii: ', self.parent.path_ascii)
        settings = QSettings()
        settings.setValue('path_ascii', self.parent.path_ascii)
        settings.setValue('path_config', self.parent.path_config)
        
        