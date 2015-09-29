from PyQt4 import QtGui, QtCore

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
        _item_min = QtGui.QTableWidgetItem(str(qmin))
        _item_min.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      
        _item_max = QtGui.QTableWidgetItem(str(qmax))
        _item_max.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      

        [lmin, lmax] = lambda_range
        _item_lmin = QtGui.QTableWidgetItem(str(lmin))
        _item_lmin.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      
        _item_lmax = QtGui.QTableWidgetItem(str(lmax))
        _item_lmax.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      

        incident_angle = incident_angle
        str_incident_angle = "%.2f" % incident_angle
        _item_incident = QtGui.QTableWidgetItem(str_incident_angle)
        _item_incident.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      
        
        parent.ui.reductionTable.setItem(row, 6, _item_min)
        parent.ui.reductionTable.setItem(row, 7, _item_max)
        parent.ui.reductionTable.setItem(row, 4, _item_lmin)
        parent.ui.reductionTable.setItem(row, 5, _item_lmax)
        parent.ui.reductionTable.setItem(row, 3, _item_incident)
        
    def sortIntArray(self, _array):
        [_element1, _element2] = _array
        _element1 = int(_element1)
        _element2 = int(_element2)
        _element_min = min([_element1, _element2])
        _element_max = max([_element1, _element2])
        return [_element_min, _element_max]
        