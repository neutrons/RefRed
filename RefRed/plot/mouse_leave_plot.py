from RefRed.gui_handling.gui_utility import GuiUtility


class MouseLeavePlot(object):
	
	parent = None
	
	def __init__(self, parent=None, plot_type=None):
		if plot_type is None:
			return
		self.parent = parent

		if plot_type == 'stitching':
			self.leave_figure_plot(plot_type = plot_type, 
			                       row = 0, column = 0)
		#elif retain_all:
			#self.leave_all_figure_plot(plot_type = plot_type)
		else:
			self.leave_figure_plot(plot_type)

	def leave_all_figure_plot(self, plot_type, row=-1, column=-1):
		parent = self.parent
		
		if column == -1 and row == -1:
			o_gui_utility = GuiUtility(parent = self.parent)
			row = o_gui_utility.get_current_table_reduction_check_box_checked()
			column = 0 if o_gui_utility.is_data_tab_selected() else 1
			
		if row == -1:
			return
		
		big_table_data = parent.big_table_data
		data = big_table_data[row, column]
		if data is None:
			return
		
		if plot_type == 'yi':
			if c==0:
				plot_ui = parent.ui.data_yi_plot
			else:
				plot_ui = parent.ui.norm_yi_plot
		elif plot_type == 'yt':
			if c==0:
				plot_ui = parent.ui.data_yt_plot
			else:
				plot_ui = parent.ui.norm_yt_plot
		elif plot_type =='it':
			if c==0:
				plot_ui = parent.ui.data_it_plot
			else:
				plot_ui = parent.ui.norm_it_plot
		elif plot_type =='ix':
			if c==0:
				plot_ui = parent.ui.data_ix_plot
			else:
				plot_ui = parent.ui.norm_ix_plot
		
		[xmin, xmax] = plot_ui.canvas.ax.xaxis.get_view_interval()
		[ymin, ymax] = plot_ui.canvas.ax.yaxis.get_view_interval()
		plot_ui.canvas.ax.xaxis.set_data_interval(xmin, xmax)
		plot_ui.canvas.ax.yaxis.set_data_interval(ymin,ymax)
		plot_ui.draw()
			
		if plot_type == 'yi':
			data.all_plot_axis.yi_view_interval = [xmin,xmax,ymin,ymax]
			parent.global_yi_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type == 'yt':
			data.all_plot_axis.yt_view_interval = [xmin,xmax,ymin,ymax]
			parent.global_yt_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type =='it':
			data.all_plot_axis.it_view_interval = [xmin,xmax,ymin,ymax]
			parent.global_it_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type =='ix':
			data.all_plot_axis.ix_view_interval = [xmin,xmax,ymin,ymax]
			parent.global_ix_view_interval = [xmin,xmax,ymin,ymax]

	def leave_figure_plot(self, plot_type=None, row=-1, column=-1):
		parent = self.parent		
		
		if row == -1 and column == -1:
			o_gui_utility = GuiUtility(parent = self.parent)
			row = o_gui_utility.get_current_table_reduction_check_box_checked()
			column = 0 if o_gui_utility.is_data_tab_selected() else 1
		big_table_data = parent.big_table_data
		if big_table_data is None:
			return

		data = big_table_data[row, column]
		if data is None:
			return

		if plot_type == 'yi':
			#view_interval = data.all_plot_axis.yi_view_interval
			if column == 0:
				plot_ui = parent.ui.data_yi_plot
			else:
				plot_ui = parent.ui.norm_yi_plot
		elif plot_type == 'yt':
			#view_interval = data.all_plot_axis.yt_view_interval
			if column == 0:
				plot_ui = parent.ui.data_yt_plot
			else:
				plot_ui = parent.ui.norm_yt_plot
		elif plot_type == 'it':
			#view_interval = data.all_plot_axis.it_view_interval
			if column == 0:
				plot_ui = parent.ui.data_it_plot
			else:
				plot_ui = parent.ui.norm_it_plot
		elif plot_type == 'ix':
			#view_interval = data.all_plot_axis.ix_view_interval
			if column == 0:
				plot_ui = parent.ui.data_ix_plot
			else:
				plot_ui = parent.ui.norm_ix_plot
		elif plot_type == 'stitching':
			#view_interval = data.all_plot_axis.reduced_plot_stitching_tab_view_interval
			plot_ui = parent.ui.data_stitching_plot
		    
		[xmin, xmax] = plot_ui.canvas.ax.xaxis.get_view_interval()
		[ymin, ymax] = plot_ui.canvas.ax.yaxis.get_view_interval()
		plot_ui.canvas.ax.xaxis.set_data_interval(xmin, xmax)
		plot_ui.canvas.ax.yaxis.set_data_interval(ymin,ymax)
		plot_ui.draw()
		
		if plot_type == 'yi':
			data.all_plot_axis.yi_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type == 'yt':
			data.all_plot_axis.yt_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type == 'it':
			data.all_plot_axis.it_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type == 'ix':
			data.all_plot_axis.ix_view_interval = [xmin,xmax,ymin,ymax]
		elif plot_type == 'stitching':
			data.all_plot_axis.reduced_plot_stitching_tab_view_interval = [xmin,xmax,ymin,ymax]
	    
		parent.big_table_data[row, column] = data
		