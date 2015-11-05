from PyQt4.QtGui import QDialog
from RefRed.interfaces.manual_x_axis_interface import Ui_Dialog as UiDialogXaxis
from RefRed.interfaces.manual_y_axis_interface import Ui_Dialog as UiDialogYaxis

class LaunchStitchingManualXAxis(QDialog):

    def __init__(self, parent = None,mouse_x=0, mouse_y=0):
        QDialog.__init__(self, parent = parent)

        self.setWindowModality(False)
        self.ui = UiDialogXaxis()
        self.ui.setupUi(self)
        self.parent = parent
        
        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)
        
        pos_main_gui = self.parent.pos()
        plot_gui_pos = self.parent.ui.data_stitching_plot.pos()
        plot_gui_height = self.parent.ui.data_stitching_plot.frameGeometry().height()
        self.move(mouse_x + plot_gui_pos.x(),
                  plot_gui_pos.y() + plot_gui_height + mouse_y)
        
    def closeEvent(self, event=None):
        self.parent.manual_x_axis_dialog = None
        
    def x_min_event(self):
        print("x min")
        
    def x_max_event(self):
        print("x max")

class LaunchStitchingManualYAxis(QDialog):

    def __init__(self, parent=None, mouse_x=0, mouse_y=0):
        QDialog.__init__(self, parent = parent)
        self.setWindowModality(False)
        self.ui = UiDialogYaxis()
        self.ui.setupUi(self)
        self.parent = parent

        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)

        pos_main_gui = self.parent.pos()
        plot_gui_pos = self.parent.ui.data_stitching_plot.pos()
        plot_gui_height = self.parent.ui.data_stitching_plot.frameGeometry().height()        
        self.move(mouse_x + plot_gui_pos.x(),
                  plot_gui_height - mouse_y + plot_gui_pos.y())

    def closeEvent(self, event=None):
        self.parent.manual_y_axis_dialog = None

    def y_min_event(self):
        print("y min")
        
    def y_max_event(self):
        print("y max")

        