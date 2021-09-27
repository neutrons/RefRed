from qtpy.QtWidgets import QApplication


class StitchingYScaleOptionsRadioButtonHandler(object):

    def __init__(self, parent=None):
        self.parent = parent

    def set_index_button_clicked(self, index=0):
        self.index_button_clicked = index

        self.parent.ui.RvsQ.setChecked(False)
        self.parent.ui.RQ4vsQ.setChecked(False)

        if index == 0:
            self.parent.ui.RvsQ.setChecked(True)
        else:
            self.parent.ui.RQ4vsQ.setChecked(True)

        QApplication.processEvents()
