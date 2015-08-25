from PyQt4.QtGui import QApplication
from PyQt4 import QtCore
import time

class AutoFillWidgetsHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        self.start()
        
    def start(self):
        self.parent.ui.frame_autofill_check_status.setVisible(True)
        QApplication.processEvents()
        
    def end(self):
        time.sleep(2)
        self.parent.ui.frame_autofill_check_status.setVisible(False)
#        self.parent.delay_closing_thread = DelayClosing()
#        self.parent.delay_closing_thread.setup(self.parent)
#        self.parent.delay_closing_thread.start()
        
    def step1(self):
        self.parent.ui.check1.setVisible(True)
        QApplication.processEvents()
        
    def step2(self):
        self.parent.ui.check2.setVisible(True)
        QApplication.processEvents()
        
    def step3(self):
        self.parent.ui.check3.setVisible(True)
        QApplication.processEvents()

    def step4(self):
        self.parent.ui.check4.setVisible(True)
        QApplication.processEvents()

    def step5(self):
        self.parent.ui.check5.setVisible(True)
        QApplication.processEvents()

class DelayClosing(QtCore.QThread):
    
    def setup(self, parent, delay=3):
        self.parent = parent
        self.delay = delay
        
    def run(self):
        time.sleep(self.delay)
        self.parent.ui.frame_autofill_check_status.setVisible(False)
        QApplication.processEvents()
        