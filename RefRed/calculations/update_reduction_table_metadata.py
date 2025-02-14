from RefRed.interfaces.mytablewidget import ReductionTableColumnIndex
from RefRed.reduction_table_handling.reduction_table_handler import ReductionTableHandler


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
        incident_angle = lrdata.incident_angle / 2.0
        const_q = lrdata.const_q

        [qmin, qmax] = q_range
        str_qmin = "%.4f" % qmin
        str_qmax = "%.4f" % qmax
        [lmin, lmax] = lambda_range
        str_incident_angle = "%.2f" % incident_angle

        handler = ReductionTableHandler(parent)
        handler.set_table_item_text(row, ReductionTableColumnIndex.Q_MIN, str_qmin)
        handler.set_table_item_text(row, ReductionTableColumnIndex.Q_MAX, str_qmax)
        handler.set_table_item_text(row, ReductionTableColumnIndex.LAMBDA_MIN, str(lmin))
        handler.set_table_item_text(row, ReductionTableColumnIndex.LAMBDA_MAX, str(lmax))
        handler.set_table_item_text(row, ReductionTableColumnIndex.TWO_THETA, str_incident_angle)
        handler.set_checkbox_state(row, ReductionTableColumnIndex.CONST_Q_BINS, const_q)
