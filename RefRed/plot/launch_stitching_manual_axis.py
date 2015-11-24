from PyQt4.QtGui import QDialog
from RefRed.interfaces.manual_x_axis_interface import Ui_Dialog as UiDialogXaxis
from RefRed.interfaces.manual_y_axis_interface import Ui_Dialog as UiDialogYaxis
from RefRed.reduction.reduced_data_handler import ReducedDataHandler
from RefRed.gui_handling.gui_utility import GuiUtility

class ChangeStitchingDataInterval(object):
    
    def __init__(self, parent=None,
                 x_min=None, x_max=None,
                 y_min=None, y_max=None):
        self.parent = parent
        
        _data = self.parent.big_table_data[0,0]
        
        [_x_min_view, _x_max_view] = self.parent.ui.data_stitching_plot.canvas.ax.xaxis.get_view_interval()
        if (x_min is None) and (x_max is None):
            x_min = _x_min_view
            x_max = _x_max_view
            
        [_y_min, _y_max] = self.parent.ui.data_stitching_plot.canvas.ax.yaxis.get_view_interval()
        if (y_min is None) and (y_max is None):
            y_min = _y_min
            y_max = _y_max
    
        _data.all_plot_axis.reduced_plot_stitching_tab_view_interval = [x_min, x_max, y_min, y_max]
#        _data.all_plot_axis.reduced_plot_stitching_tab_data_interval = [x_min, x_max, y_min, y_max]
        
        self.parent.big_table_data[0, 0] = _data

        o_reduced_handler = ReducedDataHandler(parent=self.parent)
        o_reduced_handler.plot()

class LaunchStitchingManualXAxis(QDialog):

    x_min = None
    x_max = None
    _lrdata = None

    def __init__(self, parent = None, mouse_x=0, mouse_y=0):
        QDialog.__init__(self, parent = parent)

        self.setWindowModality(False)
        self.ui = UiDialogXaxis()
        self.ui.setupUi(self)
        self.parent = parent
        
        big_table_data = self.parent.big_table_data
        self._lrdata = big_table_data[0, 0]
        
        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)
        
        pos_main_gui = self.parent.pos()
        plot_gui_pos = self.parent.ui.data_stitching_plot.pos()
        plot_gui_height = self.parent.ui.data_stitching_plot.frameGeometry().height()
        self.move(mouse_x + plot_gui_pos.x(),
                  plot_gui_pos.y() + plot_gui_height + mouse_y)
        
        self.init_widgets()
        
    def init_widgets(self):
        
        o_gui_utility = GuiUtility(parent = self.parent)
        axis_type = o_gui_utility.get_reduced_yaxis_type()
        
        if axis_type == 'RvsQ':
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ_view()
        else:
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ4Q_view()

        self.x_min = _x_min
        self.x_max = _x_max
        
        _x_min_str = "%.4f" % _x_min
        _x_max_str = "%.4f" % _x_max
        
        self.ui.x_min_value.setText(_x_min_str)
        self.ui.x_max_value.setText(_x_max_str)
        
    def closeEvent(self, event=None):
        self.parent.manual_x_axis_dialog = None
        
    def x_min_event(self):
        self.validate_changes()
        
    def x_max_event(self):
        self.validate_changes()

    def x_auto_rescale_event(self):
        print('x_auto_scale_event')

    def validate_changes(self):
        self.x_min = float(str(self.ui.x_min_value.text()))
        self.x_max = float(str(self.ui.x_max_value.text()))
        o_changes = ChangeStitchingDataInterval( parent= self.parent,
                                                 x_min = self.x_min,
                                                 x_max = self.x_max)
    

class LaunchStitchingManualYAxis(QDialog):

    y_min = None
    y_max = None
    _lrdata = None
    
    def __init__(self, parent=None, mouse_x=0, mouse_y=0):
        QDialog.__init__(self, parent = parent)
        self.setWindowModality(False)
        self.ui = UiDialogYaxis()
        self.ui.setupUi(self)
        self.parent = parent

        big_table_data = self.parent.big_table_data
        self._lrdata = big_table_data[0, 0]

        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)

        pos_main_gui = self.parent.pos()
        plot_gui_pos = self.parent.ui.data_stitching_plot.pos()
        plot_gui_height = self.parent.ui.data_stitching_plot.frameGeometry().height()        
        self.move(mouse_x + plot_gui_pos.x(),
                  plot_gui_height - mouse_y + plot_gui_pos.y())

        self.init_widgets()
        
    def init_widgets(self):
        o_gui_utility = GuiUtility(parent = self.parent)
        axis_type = o_gui_utility.get_reduced_yaxis_type()
        
        if axis_type == 'RvsQ':
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ_view()
        else:
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ4Q_view()

        self.y_min = _y_min
        self.y_max = _y_max
        
        _y_min_str = "%.4f" % _y_min
        _y_max_str = "%.4f" % _y_max
        
        self.ui.y_min_value.setText(_y_min_str)
        self.ui.y_max_value.setText(_y_max_str)

    def closeEvent(self, event=None):
        self.parent.manual_y_axis_dialog = None

    def y_min_event(self):
        self.validate_changes()
        
    def y_max_event(self):
        self.validate_changes()

    def y_auto_rescale_event(self):
        print('y_auto_scale_event')

    def validate_changes(self):
        self.y_min = float(str(self.ui.y_min_value.text()))
        self.y_max = float(str(self.ui.y_max_value.text()))
        o_changes = ChangeStitchingDataInterval( parent= self.parent,
                                                 y_min = self.y_min,
                                                 y_max = self.y_max)
        