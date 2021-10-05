class AllPlotAxis(object):

    yt_view_interval = None
    yt_data_interval = None
    is_yt_ylog = False
    is_yt_xlog = False

    detector_view_interval = None
    detector_data_interval = None

    yi_view_interval = None
    yi_data_interval = None
    is_yi_ylog = False
    is_yi_xlog = True

    it_view_interval = None
    it_data_interval = None
    is_it_ylog = False
    is_it_xlog = False

    ix_view_interval = None
    ix_data_interval = None
    is_ix_ylog = False
    is_it_xlog = False

    reduced_plot_stitching_tab_view_interval = None
    reduced_plot_stitching_tab_data_interval = None
    is_reduced_plot_stitching_tab_ylog = True
    is_reduced_plot_stitching_tab_xlog = False

    reduced_plot_RQ4autoView_y = None
    reduced_plot_RQautoView_y = None
    reduced_plot_RQ4userView_y = None
    reduced_plot_RQuserView_y = None

    reduced_plot_RQQ4autoView_x = None
    reduced_plot_RQQ4userView_x = None

    def __init__(self):
        pass

    def save_all_reduced_view(self, xmin=-1, xmax=-1, ymin=-1, ymax=-1):
        self.reduced_plot_RQ4autoView_y = [ymin, ymax]
        self.reduced_plot_RQ4userView_y = [ymin, ymax]
        self.reduced_plot_RQuserView_y = [ymin, ymax]
        self.reduced_plot_RQautoView_y = [ymin, ymax]
        self.reduced_plot_RQQ4userView_x = [xmin, xmax]
        self.reduced_plot_RQQ4autoView_x = [xmi, xmax]

    def save_user_reduced_view(self, xmin=-1, xmax=-1, ymin=-1, ymax=-1):
        self.reduced_plot_RQ4userView_y = [ymin, ymax]
        self.reduced_plot_RQuserView_y = [ymin, ymax]
        self.reduced_plot_RQQ4userView_x = [xmin, xmax]

    def get_user_reduced_RQ_view(self):
        [xmin, xmax] = self.reduced_plot_RQQ4userView_x
        [ymin, ymax] = self.reduced_plot_RQuserView_y
        return [xmin, xmax, ymin, ymax]

    def get_user_reduced_RQ4Q_view(self):
        [xmin, xmax] = self.reduced_plot_RQQ4userView_x
        [ymin, ymax] = self.reduced_plot_RQ4userView_y
        return [xmin, xmax, ymin, ymax]
