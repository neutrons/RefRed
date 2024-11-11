# standard imports
import json
import logging
import os
import sys
import time

# third-party imports
from lr_reduction import template
from lr_reduction import reduction_template_reader
import numpy as np
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QApplication

# RefRed imports
from RefRed.gui_handling.progressbar_handler import ProgressBarHandler
from RefRed.lconfigdataset import LConfigDataset
from RefRed.mantid_utility import MantidUtility
from RefRed.reduction.global_reduction_settings_handler import GlobalReductionSettingsHandler
from RefRed.reduction.individual_reduction_settings_handler import IndividualReductionSettingsHandler
from RefRed.reduction.live_calculate_sf import LiveCalculateSF
from RefRed.reduction.live_reduced_data_handler import LiveReducedDataHandler
from RefRed.status_message_handler import StatusMessageHandler


class LiveReductionHandler(object):

    big_table_data = None
    list_reduced_workspace = []
    nbr_reduction_process = -1

    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data
        self.nbr_reduction_process = self.calculate_nbr_reduction_process()

    def recalculate(self, replot_only=False):
        for row_index in range(self.nbr_reduction_process):
            # scale
            if not replot_only:
                o_calculate_sf = LiveCalculateSF(
                    parent=self.parent, row_index=row_index, n_runs=self.nbr_reduction_process
                )
                o_calculate_sf.run()

            # plot
            o_reduced_plot = LiveReducedDataHandler(parent=self.parent, row_index=row_index)
            o_reduced_plot.populate_table()
            o_reduced_plot.live_plot()

        # Overplot loaded data files
        if self.parent.o_stitching_ascii_widget is not None:
            self.parent.o_stitching_ascii_widget.update_display()

        self.parent.ui.data_stitching_plot.canvas.draw_idle()

    def run(self):
        _big_table_data = self.big_table_data
        _data_0_0 = _big_table_data[0, 0]
        if _data_0_0 is None:
            return

        StatusMessageHandler(parent=self.parent, message='Running reduction ...', is_threaded=False)

        self.parent.ui.reduceButton.setEnabled(False)

        self.cleanup()

        o_reduction_progressbar_handler = ProgressBarHandler(parent=self.parent)
        o_reduction_progressbar_handler.setup(nbr_reduction=self.nbr_reduction_process, label='Reduction Process ')

        common_pars = GlobalReductionSettingsHandler(parent=self.parent).to_dict()

        for row_index in range(self.nbr_reduction_process):
            # Reduction options to pass as template data
            reduction_pars = IndividualReductionSettingsHandler(parent=self.parent, row_index=row_index).to_dict()
            reduction_pars.update(common_pars)

            # run reduction
            try:
                template_data = reduction_template_reader.ReductionParameters()
                template_data.from_dict(reduction_pars, permissible=True)
                q, r, dr, info = template.process_from_template(
                    reduction_pars['data_files'],
                    template_data,
                    q_summing=reduction_pars['const_q'],  # const Q binning
                    info=True,
                    normalize=reduction_pars['apply_normalization'],
                )
                self.save_reduction(row_index, refl=[q, r, dr], info=info)
            except:
                logging.error(sys.exc_info()[1])
                self.parent.ui.reduceButton.setEnabled(True)
                StatusMessageHandler(parent=self.parent, message='Failed!', is_threaded=True)
                return

            # scale
            o_calculate_sf = LiveCalculateSF(parent=self.parent, row_index=row_index)
            o_calculate_sf.run()

            # plot
            o_reduced_plot = LiveReducedDataHandler(parent=self.parent, row_index=row_index)
            o_reduced_plot.populate_table()
            o_reduced_plot.live_plot()
            self.parent.ui.data_stitching_plot.draw()
            QApplication.processEvents()

            o_reduction_progressbar_handler.next_step()

        self.parent.big_table_data = self.big_table_data
        o_reduction_progressbar_handler.end()
        self.parent.ui.reduceButton.setEnabled(True)

        # save size of view for home button
        self.save_stitching_plot_view()

        StatusMessageHandler(parent=self.parent, message='Done!', is_threaded=True)

    def export(self):
        """
        Export a basic script that will reduce every run
        """
        # Ask for the output file path
        run_number = self.parent.big_table_data[0, 0].run_number
        default_filename = os.path.join(self.parent.path_ascii, "REFL_%s_data_reduction_script.py" % run_number)
        filename, _ = QFileDialog.getSaveFileName(self.parent, "Python script", default_filename)

        # If the user hits the cancel button, just exit
        if not filename:
            return

        # Gather information and generate script
        common_pars = GlobalReductionSettingsHandler(parent=self.parent).to_dict()

        script = "# Reduction script generated by refred on %s\n" % time.ctime()
        script += "import json\n"
        script += "from lr_reduction import template\n"
        script += "from lr_reduction import reduction_template_reader\n\n"

        for row_index in range(self.nbr_reduction_process):
            reduction_pars = IndividualReductionSettingsHandler(parent=self.parent, row_index=row_index).to_dict()
            reduction_pars.update(common_pars)

            json_pars = json.dumps(reduction_pars)
            script += "reduction_pars = json.loads('%s')\n" % json_pars
            script += "template_data = reduction_template_reader.ReductionParameters()\n"
            script += "template_data.from_dict(reduction_pars)\n"
            script += "q, r, dr, info = template.process_from_template(reduction_pars['data_files'], template_data, q_summing=reduction_pars['const_q'], info=True, normalize=reduction_pars['apply_normalization'])\n\n"  # noqa: E501

        with open(filename, 'w') as fd:
            fd.write(script)

    def save_stitching_plot_view(self):
        big_table_data = self.parent.big_table_data
        data = big_table_data[0, 0]
        [xmin, xmax] = self.parent.ui.data_stitching_plot.canvas.ax.xaxis.get_view_interval()
        [ymin, ymax] = self.parent.ui.data_stitching_plot.canvas.ax.yaxis.get_view_interval()
        data.all_plot_axis.reduced_plot_stitching_tab_data_interval = [xmin, xmax, ymin, ymax]
        big_table_data[0, 0] = data
        self.parent.big_table_data = big_table_data

    def save_reduction(self, row=-1, refl=None, info=None):

        big_table_data = self.big_table_data
        _config = big_table_data[row, 2]
        if _config is None:
            _config = LConfigDataset()

        _config.reduce_q_axis = np.copy(refl[0])
        _config.reduce_y_axis = np.copy(refl[1])
        _config.reduce_e_axis = np.copy(refl[2])
        _config.meta_data = info
        _config.q_axis_for_display = refl[0]
        _config.y_axis_for_display = refl[1]
        _config.e_axis_for_display = refl[2]
        _config.sf_auto_found_match = True
        if info['scaling_factors']['a'] == 1 and info['scaling_factors']['err_a'] == 0:
            _config.sf_auto_found_match = False

        big_table_data[row, 2] = _config
        self.big_table_data = big_table_data

    def print_message(self, title, value):
        print('> %s ' % title)
        print('-> value: ', value, '-> type: ', type(value))

    def calculate_nbr_reduction_process(self):
        _big_table_data = self.big_table_data
        nbr_reduction = 0
        for row_index in range(self.parent.REDUCTIONTABLE_MAX_ROWCOUNT):
            if _big_table_data[row_index, 0] is None:
                return nbr_reduction
            nbr_reduction += 1
        return nbr_reduction

    def cleanup(self):
        o_mantid_utility = MantidUtility(parent=self.parent)
        o_mantid_utility.cleanup_workspaces()
