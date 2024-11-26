from qtpy import QtWidgets, QtCore

from RefRed.interfaces.mytablewidget import ReductionTableColumnIndex


class UpdateReductionTableMetadata(object):
    def __init__(self, parent=None, lrdata=None, row=-1):
        self.parent = parent
        self.lrdata = lrdata
        self.row = row

        self.update()

    def update(self):

        lrdata = self.lrdata
        row = self.row
        parent = self.parent

        q_range = lrdata.q_range
        lambda_range = lrdata.lambda_range
        incident_angle = lrdata.incident_angle

        [qmin, qmax] = q_range
        str_qmin = "%.4f" % qmin
        _item_min = QtWidgets.QTableWidgetItem(str_qmin)
        _item_min.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        str_qmax = "%.4f" % qmax
        _item_max = QtWidgets.QTableWidgetItem(str_qmax)
        _item_max.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        [lmin, lmax] = lambda_range
        _item_lmin = QtWidgets.QTableWidgetItem(str(lmin))
        _item_lmin.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        _item_lmax = QtWidgets.QTableWidgetItem(str(lmax))
        _item_lmax.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        incident_angle = incident_angle
        str_incident_angle = "%.2f" % incident_angle
        _item_incident = QtWidgets.QTableWidgetItem(str_incident_angle)
        _item_incident.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        parent.ui.reductionTable.setItem(row, ReductionTableColumnIndex.Q_MIN, _item_min)
        parent.ui.reductionTable.setItem(row, ReductionTableColumnIndex.Q_MAX, _item_max)
        parent.ui.reductionTable.setItem(row, ReductionTableColumnIndex.LAMBDA_MIN, _item_lmin)
        parent.ui.reductionTable.setItem(row, ReductionTableColumnIndex.LAMBDA_MAX, _item_lmax)
        parent.ui.reductionTable.setItem(row, ReductionTableColumnIndex.TWO_THETA, _item_incident)

        const_q = lrdata.const_q
        const_q_col = ReductionTableColumnIndex.CONST_Q_BINS
        const_q_checkbox = parent.ui.reductionTable.cellWidget(row, const_q_col).findChild(QtWidgets.QCheckBox)
        const_q_checkbox.setChecked(const_q)

    def sortIntArray(self, _array):
        [_element1, _element2] = _array
        _element1 = int(_element1)
        _element2 = int(_element2)
        _element_min = min([_element1, _element2])
        _element_max = max([_element1, _element2])
        return [_element_min, _element_max]
