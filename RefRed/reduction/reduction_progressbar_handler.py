from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
import time


class ReductionProgressBarHandler(object):

    nbr_reduction = 0
    current_step = 0
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def setup(self, nbr_reduction=0):
        self.nbr_reduction = nbr_reduction
        
        self.parent.ui.reductionProcessProgressBar.setMinimum(0)
        self.parent.ui.reductionProcessProgressBar.setMaximum(nbr_reduction)
        self.parent.ui.reductionProcessProgressBar.setValue(0)
        self.parent.ui.frame_reduction.setVisible(True)
        QApplication.processEvents()
    
    def next_step(self):
        self.current_step += 1
        self.parent.ui.reductionProcessProgressBar.setValue(self.current_step)
        QApplication.processEvents()
        
    def end(self):
        time.sleep(0.5)
        self.parent.ui.frame_reduction.setVisible(False)
        QApplication.processEvents()
        
                
class DelayClosing(QtCore.QThread):
    
    def setup(self, parent=None, delay=3):
        self.parent = parent
        self.delay = delay
        
    def run(self):
        time.sleep(self.delay)
        self.parent.ui.frame_reduction.setVisible(False)
        QApplication.processEvents()
