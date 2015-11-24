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
	
	reduced_plot_RQautoView = None
	reduced_plot_RQ4QautoView = None
	reduced_plot_RQuserView = None
	reduced_plot_RQ4QuserView = None
	
	def __init__(self):
		pass
	
	def save_all_reduced_view(self, xmin=-1, xmax=-1, ymin=-1, ymax=-1):
		self.reduced_plot_RQ4QautoView = [xmin, xmax, ymin, ymax]
		self.reduced_plot_RQautoView = [xmin, xmax, ymin, ymax]
		self.reduced_plot_RQ4QuserView = [xmin, xmax, ymin, ymax]
		self.reduced_plot_RQuserView = [xmin, xmax, ymin, ymax]
		
	def save_user_reduced_view(self, xmin=-1, xmax=-1, ymin=-1, ymax=-1):
		self.reduced_plot_RQ4QuserView = [xmin, xmax, ymin, ymax]
		self.reduced_plot_RQuserView = [xmin, xmax, ymin, ymax]
		
	def get_user_reduced_RQ_view(self):
		return self.reduced_plot_RQuserView
	
	def get_user_reduced_RQ4Q_view(self):
		return self.reduced_plot_RQ4QuserView	
	
	
	