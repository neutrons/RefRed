class GuiConnections(object):
    
    def __init__(self, parent = None):
        
        parent.ui.data_yt_plot.singleClick.connect(parent.single_click_data_yt_plot)
        #parent.ui.data_yt_plot.leaveFigure.connect(parent.leave_figure_yt_plot)
        #parent.ui.data_yt_plot.logtogy.connect(parent.logy_toggle_yt_plot)
        #parent.ui.data_yt_plot.toolbar.homeClicked.connect(parent.home_clicked_yt_plot)
        parent.ui.data_yt_plot.toolbar.exportClicked.connect(parent.export_yt)
    
        parent.ui.norm_yt_plot.singleClick.connect(parent.single_click_norm_yt_plot)
        #parent.ui.norm_yt_plot.leaveFigure.connect(parent.leave_figure_yt_plot)
        #parent.ui.norm_yt_plot.logtogy.connect(parent.logy_toggle_yt_plot)
        #parent.ui.norm_yt_plot.toolbar.homeClicked.connect(parent.home_clicked_yt_plot)
        parent.ui.norm_yt_plot.toolbar.exportClicked.connect(parent.export_yt)
    
        parent.ui.data_yi_plot.singleClick.connect(parent.single_click_data_yi_plot)
        #parent.ui.data_yi_plot.leaveFigure.connect(parent.leave_figure_yi_plot)
        #parent.ui.data_yi_plot.logtogx.connect(parent.logx_toggle_yi_plot)
        #parent.ui.data_yi_plot.toolbar.homeClicked.connect(parent.home_clicked_yi_plot)
        parent.ui.data_yi_plot.toolbar.exportClicked.connect(parent.export_yi)
    
        parent.ui.norm_yi_plot.singleClick.connect(parent.single_click_norm_yi_plot)
        #parent.ui.norm_yi_plot.leaveFigure.connect(parent.leave_figure_yi_plot)
        #parent.ui.norm_yi_plot.logtogx.connect(parent.logx_toggle_yi_plot)
        #parent.ui.norm_yi_plot.toolbar.homeClicked.connect(parent.home_clicked_yi_plot)
        parent.ui.norm_yi_plot.toolbar.exportClicked.connect(parent.export_yi)
        
        #parent.ui.data_it_plot.singleClick.connect(parent.single_click_data_it_plot)
        #parent.ui.data_it_plot.leaveFigure.connect(parent.leave_figure_it_plot)
        #parent.ui.data_it_plot.logtogy.connect(parent.logy_toggle_it_plot)
        #parent.ui.data_it_plot.toolbar.homeClicked.connect(parent.home_clicked_it_plot)
        parent.ui.data_it_plot.toolbar.exportClicked.connect(parent.export_it)
    
        #parent.ui.norm_it_plot.singleClick.connect(parent.single_click_norm_it_plot)
        #parent.ui.norm_it_plot.leaveFigure.connect(parent.leave_figure_it_plot)
        #parent.ui.norm_it_plot.logtogy.connect(parent.logy_toggle_it_plot)
        #parent.ui.norm_it_plot.toolbar.homeClicked.connect(parent.home_clicked_it_plot)
        parent.ui.norm_it_plot.toolbar.exportClicked.connect(parent.export_it)
    
        #parent.ui.data_ix_plot.singleClick.connect(parent.single_click_data_ix_plot)
        #parent.ui.data_ix_plot.leaveFigure.connect(parent.leave_figure_ix_plot)
        #parent.ui.data_ix_plot.logtogy.connect(parent.logy_toggle_ix_plot)
        #parent.ui.data_ix_plot.toolbar.homeClicked.connect(parent.home_clicked_ix_plot)
        parent.ui.data_ix_plot.toolbar.exportClicked.connect(parent.export_ix)
    
        #parent.ui.norm_ix_plot.singleClick.connect(parent.single_click_norm_ix_plot)
        #parent.ui.norm_ix_plot.leaveFigure.connect(parent.leave_figure_ix_plot)
        #parent.ui.norm_ix_plot.logtogy.connect(parent.logy_toggle_ix_plot)
        #parent.ui.norm_ix_plot.toolbar.homeClicked.connect(parent.home_clicked_ix_plot)
        parent.ui.norm_ix_plot.toolbar.exportClicked.connect(parent.export_ix)
    
        #parent.ui.data_stitching_plot.singleClick.connect(parent.single_click_data_stitching_plot)
        #parent.ui.data_stitching_plot.leaveFigure.connect(parent.leave_figure_data_stitching_plot)
        #parent.ui.data_stitching_plot.toolbar.homeClicked.connect(parent.home_clicked_data_stitching_plot)
        #parent.ui.data_stitching_plot.logtogx.connect(parent.logx_toggle_data_stitching)
        #parent.ui.data_stitching_plot.logtogy.connect(parent.logy_toggle_data_stitching)
        parent.ui.data_stitching_plot.toolbar.exportClicked.connect(parent.export_stitching_data)
        
        #parent.fileLoaded.connect(parent.updateLabels)
        #parent.fileLoaded.connect(parent.plotActiveTab)

        #parent.initiateProjectionPlot.connect(parent.plot_projections)
        #parent.initiateReflectivityPlot.connect(parent.plot_refl)
        #parent.initiateReflectivityPlot.connect(parent.updateStateFile)
        
        #for plot in [parent.ui.data_yt_plot, 
                     #parent.ui.data_it_plot,
                     #parent.ui.data_yi_plot,
                     #parent.ui.data_ix_plot,
                     #parent.ui.norm_yt_plot, 
                     #parent.ui.norm_it_plot,
                     #parent.ui.norm_yi_plot,
                     #parent.ui.norm_ix_plot]:
            #plot.canvas.mpl_connect('motion_notify_event', parent.plotMouseEvent)
            
        #for plot in [parent.ui.data_yt_plot, 
                     #parent.ui.data_it_plot,
                     #parent.ui.data_ix_plot,
                     #parent.ui.norm_yt_plot, 
                         #parent.ui.norm_it_plot,
                     #parent.ui.norm_ix_plot]:
          #plot.canvas.mpl_connect('scroll_event', parent.changeColorScale)
    
        #parent.ui.norm_yt_plot.canvas.mpl_connect('motion_notify_event', parent.mouseNormPlotyt)
        #parent.ui.norm_yt_plot.canvas.mpl_connect('button_press_event', parent.mouseNormPlotyt)
        #parent.ui.norm_yt_plot.canvas.mpl_connect('button_release_event', parent.mouseNormPlotyt)
                
