from qtpy import QtCore, QtGui, QtWidgets

import RefRed.colors


class FillSFGuiTable(object):
    tableData = None
    parent = None
    index_color = 0

    def __init__(self, parent=None, table=None, is_using_si_slits=False):
        self.parent = parent
        if is_using_si_slits:
            s2ih = "SiH"
            s2iw = "SiW"
        else:
            s2ih = "S2H"
            s2iw = "S2W"
        verticalHeader = [
            "Run #",
            "Nbr. Attenuator",
            "\u03bbmin (\u00c5)",
            "\u03bbmax (\u00c5)",
            "p Charge (mC)",
            "\u03bbrequested (\u00c5)",
            "S1W",
            "S1H",
            s2iw,
            s2ih,
            "Peak1",
            "Peak2",
            "Back1",
            "Back2",
            "TOF1 (ms)",
            "TOF2 (ms)",
        ]
        parent.tableWidget.setHorizontalHeaderLabels(verticalHeader)

        self.clearTable()
        _big_table = table
        if table is None or len(table) == 0:
            return
        parent.big_table = _big_table
        [nbr_row, nbr_column] = _big_table.shape
        _prev_lambda = "%.2f" % (float(-1))
        for r in range(nbr_row):
            _row = _big_table[r, :]
            is_any_red = False
            _new_lambda = "%.2f" % (float(_row[5]))
            if _prev_lambda != _new_lambda:
                back_color = self.newBackgroundColor()
                _prev_lambda = _new_lambda

            parent.tableWidget.insertRow(r)

            if r == 0:
                _item = QtWidgets.QTableWidgetItem("ACTIVE")
                parent.tableWidget.setVerticalHeaderItem(r, _item)

            _atte = int(_row[1])
            _widget = QtWidgets.QSpinBox()
            _widget.setMinimum(0)
            _widget.setMaximum(20)
            _widget.setValue(_atte)
            _widget.valueChanged.connect(self.parent.attenuatorValueChanged)
            parent.tableWidget.setCellWidget(r, 1, _widget)

            _lambda_min = str(float(_row[2]))
            _item = QtWidgets.QTableWidgetItem(_lambda_min)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 2, _item)

            _lambda_max = str(float(_row[3]))
            _item = QtWidgets.QTableWidgetItem(_lambda_max)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 3, _item)

            _proton_charge = "%.2e" % (float(_row[4]))
            _item = QtWidgets.QTableWidgetItem(_proton_charge)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 4, _item)

            _lambda_req = "%.2f" % (float(_row[5]))
            _item = QtWidgets.QTableWidgetItem(_lambda_req)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 5, _item)

            _s1w = "%.2f" % (float(_row[6]))
            _item = QtWidgets.QTableWidgetItem(_s1w)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 6, _item)

            _s1h = "%.2f" % (float(_row[7]))
            _item = QtWidgets.QTableWidgetItem(_s1h)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 7, _item)

            _s2iw = "%.2f" % (float(_row[8]))
            _item = QtWidgets.QTableWidgetItem(_s2iw)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 8, _item)

            _s2ih = "%.2f" % (float(_row[9]))
            _item = QtWidgets.QTableWidgetItem(_s2ih)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            parent.tableWidget.setItem(r, 9, _item)

            for k in range(10, 16):
                _value = _row[k]
                _brush = QtGui.QBrush()
                if _value == "0" or _value == "N/A" or _value == "":
                    _value = "N/A"
                    _brush.setColor(RefRed.colors.VALUE_BAD)
                    is_any_red = True
                else:
                    if k in [14, 15]:
                        if int(float(_value)) > 1000:
                            _value = float(_value) / 1000
                            _value = "%.2f" % _value
                        else:
                            _value = str(float(_value))
                    else:
                        _value = "%.d" % (int(float(_value)))
                    _brush.setColor(RefRed.colors.VALUE_OK)
                _item = QtWidgets.QTableWidgetItem(_value)
                _item.setForeground(_brush)
                _color = QtGui.QColor(back_color)
                _item.setBackground(_color)
                if k in [10, 11, 12, 13]:
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                else:
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                parent.tableWidget.setItem(r, k, _item)

            _run_number = str(int(_row[0]))
            _brush = QtGui.QBrush()
            if is_any_red:
                _brush.setColor(RefRed.colors.VALUE_BAD)
            else:
                _brush.setColor(RefRed.colors.VALUE_OK)
            QtGui.QBrush()  # TODO is this line necessary?
            _item = QtWidgets.QTableWidgetItem(_run_number)
            _item.setForeground(_brush)
            _color = QtGui.QColor(back_color)
            _item.setBackground(_color)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            parent.tableWidget.setItem(r, 0, _item)

    def newBackgroundColor(self):
        _index_color = self.index_color + 1
        sz_color_back_list = len(RefRed.colors.COLOR_BACKGROUND_LIST)
        if _index_color >= sz_color_back_list:
            _index_color = 0
        self.index_color = _index_color
        return RefRed.colors.COLOR_BACKGROUND_LIST[_index_color]

    def clearTable(self):
        nbrRow = self.parent.tableWidget.rowCount()
        if nbrRow > 0:
            for _row in range(nbrRow):
                self.parent.tableWidget.removeRow(0)
