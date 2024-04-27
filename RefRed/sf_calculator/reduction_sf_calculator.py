# standard-library imports
import logging
import time
from typing import Optional, Union

# third-party imports
import numpy as np
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QFileDialog

# RefRed imports
from RefRed.utilities import convertTOF


class ReductionSfCalculator(object):
    """
    Compute scaling factors
    """

    sf_gui = None
    export_script_file = ""
    export_script = []
    table_settings = []
    index_col = [0, 1, 5, 10, 11, 12, 13, 14, 15]
    nbr_row = -1
    nbr_scripts = 0
    new_sfcalculator_script = True

    def __init__(self, parent, export_script_flag: Union[str, bool] = False, test_mode: Optional[bool] = False):
        """Constructor and main execution body
        There is no need to call any methods other than initialize an object

        :parent SFCalculator: the main widget for calculation of structure factors
        :export_script_flag: if ``str`` then it is a script file name; if ``True``, then launch dialog for file name;
         otherwise, do nothing
        :test_mode: flag such that the class will be called in a non-GUI unit test mode
        """
        # Parse
        self.sf_gui = parent
        self.export_script_flag = True
        self._unit_test_mode = test_mode

        # FIXME TODO - is it good to mix presenter/model with view?
        if export_script_flag:
            filename, _ = QFileDialog.getSaveFileName(
                self.sf_gui,  # parent widget
                "Export Script File",  # dialog title
                self.sf_gui.save_directory,  # opening directory
                "Python (*.py);;All (*.*)",  # list of display-file filters
            )
            if filename:
                self.export_script_file = filename
            else:
                # No file is specified: user cancel the operation
                return
        else:
            # no file is given or required
            self.export_script_flag = False

        self.collect_table_information()
        # SF calculation or exporting script
        self._handle_request()

    def collect_table_information(self):
        nbr_row = self.sf_gui.tableWidget.rowCount()
        self.nbr_row = nbr_row
        nbr_column = len(self.index_col)
        _table_settings = np.zeros((nbr_row, nbr_column))

        for _row in range(nbr_row):
            for _col in range(nbr_column):
                if _col == 1:
                    _value = str(self.sf_gui.tableWidget.cellWidget(_row, self.index_col[_col]).value())
                else:
                    _value = str(self.sf_gui.tableWidget.item(_row, self.index_col[_col]).text())
                _table_settings[_row, _col] = _value

        self.table_settings = _table_settings

    def _handle_request(self):
        from_to_index_same_lambda = self.generateIndexSameLambda()

        if from_to_index_same_lambda is None:
            self.sf_gui.updateProgressBar(0.0)
            pass
        # # This is to expose for testing
        # self._from_to_index_same_lambda = from_to_index_same_lambda

        nbr_scripts = self.nbr_scripts

        incident_medium = self.sf_gui.incidentMediumComboBox.currentText()
        output_file_name = self.sf_gui.sfFileNameLabel.text()
        self.sf_gui.updateProgressBar(0.1)

        for i in range(nbr_scripts):
            from_index = int(from_to_index_same_lambda[i, 0])
            to_index = int(from_to_index_same_lambda[i, 1])

            if (to_index - from_index) <= 1:
                continue

            string_runs = self.getStringRuns(from_index, to_index)
            list_peak_back = self.getListPeakBack(from_index, to_index)
            tof_range = self.getTofRange(from_index)

            if not self.export_script_flag:
                self.launchScript(
                    string_runs=string_runs,
                    list_peak_back=list_peak_back,
                    incident_medium=incident_medium,
                    output_file_name=output_file_name,
                    tof_range=tof_range,
                )

                self.refreshOutputFileContainPreview(output_file_name)
            else:
                script = self.generate_script(
                    string_runs=string_runs,
                    list_peak_back=list_peak_back,
                    incident_medium=incident_medium,
                    output_file_name=output_file_name,
                    tof_range=tof_range,
                )

                with open(self.export_script_file, 'w') as fd:
                    fd.write(script)

            self.sf_gui.updateProgressBar(float(i + 1) / float(nbr_scripts))
            QApplication.processEvents()

    def _get_algorithm_params(self, run_string, list_peak_back):
        """
        Generate the LRScalingFactors algortihm parameters
        """
        peak_ranges = []
        bck_ranges = []
        low_res_ranges = []
        for item in list_peak_back:
            peak_ranges.append(int(item[0]))
            peak_ranges.append(int(item[1]))
            bck_ranges.append(int(item[2]))
            bck_ranges.append(int(item[3]))
            low_res_ranges.append(0)
            low_res_ranges.append(256)

        run_list = []
        toks = run_string.strip().split(",")
        for item in toks:
            pair = item.strip().split(":")
            run_list.append(int(pair[0]))

        return peak_ranges, bck_ranges, low_res_ranges, run_list

    def launchScript(
        self,
        string_runs="",
        list_peak_back=[],
        incident_medium="",
        output_file_name="",
        tof_range=[],
    ):
        """
        Create scaling factor file
        """
        peak_ranges, bck_ranges, low_res_ranges, run_list = self._get_algorithm_params(string_runs, list_peak_back)

        from lr_reduction.scaling_factors import LRScalingFactors
        from lr_reduction.utils import mantid_algorithm_exec

        mantid_algorithm_exec(
            LRScalingFactors.LRScalingFactors,
            DirectBeamRuns=run_list,
            IncidentMedium=str(incident_medium),
            TOFRange=tof_range,
            TOFSteps=self.sf_gui.deadtime_tof_step,
            SignalPeakPixelRange=peak_ranges,
            SignalBackgroundPixelRange=bck_ranges,
            LowResolutionPixelRange=low_res_ranges,
            ScalingFactorFile=str(output_file_name),
            UseDeadTimeCorrection=self.sf_gui.apply_deadtime,
            ParalyzableDeadTime=self.sf_gui.paralyzable_deadtime,
            DeadTime=self.sf_gui.deadtime_value,
            DeadTimeTOFStep=self.sf_gui.deadtime_tof_step,
        )

    def generate_script(
        self,
        string_runs="",
        list_peak_back=[],
        incident_medium="",
        output_file_name="",
        tof_range=[],
    ):
        """
        Generate a scaling factor calculation script
        """
        import lr_reduction

        peak_ranges, bck_ranges, low_res_ranges, run_list = self._get_algorithm_params(string_runs, list_peak_back)

        script = "# Scaling factor calculation\n"
        script += f"# lr_reduction {lr_reduction.__version__}\n"
        script += f"# Script automatically generated on {time.ctime()}\n\n"

        script += "from lr_reduction.scaling_factors import LRScalingFactors\n"
        script += "from lr_reduction.utils import mantid_algorithm_exec\n\n"

        mantid_call = [r"mantid_algorithm_exec(",
                       r"    LRScalingFactors.LRScalingFactors,",
                       r"    DirectBeamRuns={0},".format(run_list),
                       r"    IncidentMedium='{0}',".format(incident_medium),
                       r"    TOFRange={0},".format(tof_range),
                       r"    TOFSteps={0},".format(self.sf_gui.deadtime_tof_step),
                       r"    SignalPeakPixelRange={0},".format(peak_ranges),
                       r"    SignalBackgroundPixelRange={0},".format(bck_ranges),
                       r"    LowResolutionPixelRange={0},".format(low_res_ranges),
                       r"    ScalingFactorFile='{0}',".format(output_file_name),
                       r"    UseDeadTimeCorrection={0},".format(self.sf_gui.apply_deadtime),
                       r"    ParalyzableDeadTime={0},".format(self.sf_gui.paralyzable_deadtime),
                       r"    DeadTime={0},".format(self.sf_gui.deadtime_value),
                       r"    DeadTimeTOFStep={0},".format(self.sf_gui.deadtime_tof_step),
                       r")"
                       ]
        script += "\n".join(mantid_call) + "\n"
        return script

    def refreshOutputFileContainPreview(self, output_file_name):
        self.sf_gui.displayConfigFile(output_file_name)

    def getStringRuns(self, from_index, to_index):
        data = self.table_settings
        string_list = []
        for i in range(from_index, to_index + 1):
            string_list.append(str(int(data[i, 0])) + ":" + str(int(data[i, 1])))
        return ",".join(string_list)

    def getListPeakBack(self, from_index, to_index):
        data = self.table_settings
        return data[from_index : to_index + 1, 3:7]

    def getTofRange(self, from_index):
        data = self.table_settings
        from_tof_ms = data[from_index, 7]
        to_tof_ms = data[from_index, 8]
        tof_from_to_micros = convertTOF([from_tof_ms, to_tof_ms], from_units="ms", to_units="micros")
        return tof_from_to_micros

    def generateIndexSameLambda(self):
        """

        Returns
        -------
        numpy.ndarray
            2D array

        """
        _data = self.table_settings

        lambda_list = _data[:, 2]
        nbr_scripts = len(set(lambda_list))
        self.nbr_scripts = nbr_scripts

        from_to_index_same_lambda = np.zeros((nbr_scripts, 2))

        first_index_lambda = 0
        if len(lambda_list) > 0:
            ref_lambda = lambda_list[0]
            index_script = 0
            for i in range(1, self.nbr_row):
                live_lambda = lambda_list[i]
                if live_lambda != ref_lambda:
                    from_to_index_same_lambda[index_script, :] = [first_index_lambda, i - 1]
                    first_index_lambda = i
                    ref_lambda = live_lambda
                    index_script += 1
                if i == (self.nbr_row - 1):
                    from_to_index_same_lambda[index_script, :] = [first_index_lambda, i]
        else:
            logging.warning("empty lambda_list, skipping")
            return None

        return from_to_index_same_lambda
