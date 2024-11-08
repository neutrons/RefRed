# standard imports
from enum import Enum

# third party imports
from qtpy import QtWidgets
from qtpy.QtCore import Qt  # type: ignore

# application imports
#


class MyTableWidget(QtWidgets.QTableWidget):

    parent = None
    ui = None

    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.parent.table_reduction_cell_enter_pressed()
        else:
            super(MyTableWidget, self).keyPressEvent(event)

    def setUI(self, ui_parent):
        self.parent = ui_parent


class ReductionTableColumIndex(Enum):
    """
    Enumeration class associating a column index to a word easy to understand what the column index is for
    """

    PLOTTED = 0
    DATA_RUN = 1
    NORM_RUN = 2
    TWO_THETA = 3
    LAMBDA_MIN = 4
    LAMBDA_MAX = 5
    Q_MIN = 6
    Q_MAX = 7
    CONST_Q_BINS = 8
    COMMENTS = 9

    def __int__(self):
        return self.value
