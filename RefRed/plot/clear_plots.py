class ClearPlots(object):

    parent = None

    plot_yt = False
    plot_yi = False
    plot_it = False
    plot_ix = False
    stitched = False

    def __init__(
        self,
        parent,
        is_data=True,
        is_norm=False,
        plot_yt=False,
        plot_yi=False,
        plot_it=False,
        plot_ix=False,
        stitched=False,
        all_plots=False,
    ):
        self.parent = parent

        self.plot_yt = plot_yt
        self.plot_yi = plot_yi
        self.plot_it = plot_it
        self.plot_ix = plot_ix
        self.stitched = stitched

        if all_plots:
            self.plot_yt = True
            self.plot_yi = True
            self.plot_it = True
            self.plot_ix = True
            self.stitched = True

        if is_data:
            self.clear_data_plots()
            parent.ui.dataNameOfFile.setText('')

        if is_norm:
            self.clear_norm_plots()
            parent.ui.normNameOfFile.setText('')

        if self.stitched:
            self.clear_stitched()

        if self.plot_yt and self.plot_yi and self.plot_it and self.plot_ix:
            self.clear_metadata()

    def clear_metadata(self):
        parent = self.parent
        parent.ui.metadataProtonChargeValue.setText('N/A')
        parent.ui.metadataProtonChargeUnits.setText('units')
        parent.ui.metadataLambdaRequestedValue.setText('N/A')
        parent.ui.metadataLambdaRequestedUnits.setText('units')
        parent.ui.metadatathiValue.setText('N/A')
        parent.ui.metadatathiUnits.setText('units')
        parent.ui.metadatatthdValue.setText('N/A')
        parent.ui.metadatatthdUnits.setText('units')
        parent.ui.metadataS1WValue.setText('N/A')
        parent.ui.metadataS1HValue.setText('N/A')
        parent.ui.metadataS2WValue.setText('N/A')
        parent.ui.metadataS2HValue.setText('N/A')
        parent.ui.metadataRunNumber.setText('N/A')

    def clear_data_plots(self):
        parent = self.parent
        if self.plot_yt:
            parent.ui.data_yt_plot.clear()
            parent.ui.data_yt_plot.draw()

        if self.plot_yi:
            parent.ui.data_yi_plot.clear()
            parent.ui.data_yi_plot.draw()

        if self.plot_it:
            parent.ui.data_it_plot.clear()
            parent.ui.data_it_plot.draw()

        if self.plot_ix:
            parent.ui.data_ix_plot.clear()
            parent.ui.data_ix_plot.draw()

    def clear_norm_plots(self):
        parent = self.parent
        if self.plot_yt:
            parent.ui.norm_yt_plot.clear()
            parent.ui.norm_yt_plot.draw()

        if self.plot_yi:
            parent.ui.norm_yi_plot.clear()
            parent.ui.norm_yi_plot.draw()

        if self.plot_it:
            parent.ui.norm_it_plot.clear()
            parent.ui.norm_it_plot.draw()

        if self.plot_ix:
            parent.ui.norm_ix_plot.clear()
            parent.ui.norm_ix_plot.draw()

    def clear_stitched(self):
        self.parent.ui.data_stitching_plot.clear()
        self.parent.ui.data_stitching_plot.draw()
