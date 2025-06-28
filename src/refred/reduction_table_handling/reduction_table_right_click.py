from qtpy import QtGui, QtWidgets

from refred.reduction_table_handling.reduction_table_handler import ReductionTableHandler


class ReductionTableRightClick(object):
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

    def run(self):
        menu = QtWidgets.QMenu(self.parent)
        remove_row = menu.addAction("Remove Row(s)")
        clear_table = menu.addAction("Clear Table")
        action = menu.exec_(QtGui.QCursor.pos())

        if action == clear_table:
            self.clear_table()
        elif action == remove_row:
            self.remove_rows()

    def clear_table(self):
        o_reduction_table_handler = ReductionTableHandler(parent=self.parent)
        o_reduction_table_handler.full_clear()

    def remove_rows(self):
        o_reduction_table_handler = ReductionTableHandler(parent=self.parent)
        o_reduction_table_handler.clear_rows_selected()
