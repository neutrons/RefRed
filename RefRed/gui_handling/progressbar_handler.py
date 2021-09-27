from qtpy import QtCore
from qtpy.QtWidgets import QApplication
import time


class ProgressBarHandler(object):

    nbr_reduction = 0
    current_step = 0
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def setup(self, nbr_reduction=0, label='Reduction Process'):
        self.nbr_reduction = nbr_reduction

        self.parent.ui.reductionProcessProgressBar.setMinimum(0)
        self.parent.ui.reductionProcessProgressBar.setMaximum(nbr_reduction)
        self.parent.ui.reductionProcessProgressBar.setValue(0)
        self.parent.ui.frame_reduction.setVisible(True)
        self.parent.ui.mainProgressBarLabel.setText(label)

        self.parent.eventProgress.setMinimum(0)
        self.parent.eventProgress.setMaximum(nbr_reduction)
        self.parent.eventProgress.setValue(0)
        self.parent.eventProgress.setVisible(True)

        QApplication.processEvents()
    
    def next_step(self):
        self.current_step += 1
        self.parent.ui.reductionProcessProgressBar.setValue(self.current_step)
        self.parent.eventProgress.setValue(self.current_step)
        QApplication.processEvents()
        
    def end(self):
        time.sleep(0.5)
        self.parent.ui.frame_reduction.setVisible(False)
        self.parent.eventProgress.setVisible(False)
        QApplication.processEvents()
        
                
class DelayClosing(QtCore.QThread):
    
    def setup(self, parent=None, delay=3):
        self.parent = parent
        self.delay = delay
        
    def run(self):
        time.sleep(self.delay)
        self.parent.ui.frame_reduction.setVisible(False)
        QApplication.processEvents()
