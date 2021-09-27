from qtpy import QtGui

from RefRed.sf_calculator.sf_calculator_table_handler import SFCalculatorTableHandler

class SFCalculatorRightClick(object):

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

    def run(self):
        menu = QtWidgets.QMenu(self.parent)
        clear_table = menu.addAction("Clear Table")
        action = menu.exec_(QtGui.QCursor.pos())

        if action == clear_table:
            self.clear_table()

    def clear_table(self):
        o_sf_calculator_table_handler = SFCalculatorTableHandler(parent = self.parent)
        o_sf_calculator_table_handler.full_clear()
