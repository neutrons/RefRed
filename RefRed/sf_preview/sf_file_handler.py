import numpy as np

from RefRed.status_message_handler import StatusMessageHandler


class SFFileHandler(object):
    full_sf_factor_table = []
    full_sf_factor_labels = []
    nbr_row = -1
    nbr_column = -1

    def __init__(self, parent=None, filename=""):
        self.parent = parent
        self.filename = filename

    def retrieve_contain(self):
        self.parse_file()
        self.parse_lines()

    def parse_file(self):
        _filename = self.filename

        try:
            with open(_filename, "r") as f:
                sf_factor_table = []
                for line in f.read().split("\n"):
                    if (len(line) > 0) and (line[0] != "#"):
                        sf_factor_table.append(line.split(" "))
            self.sf_factor_table = sf_factor_table
        except:
            StatusMessageHandler(
                parent=self.parent,
                message="File Does Not Exist!",
                is_threaded=True,
                severity="bad",
            )
            raise ImportError

    def parse_lines(self):
        _sf_factor_table = self.sf_factor_table
        full_sf_factor_labels = []
        full_sf_factor_table = []
        [self.nbr_row, self.nbr_column] = np.shape(_sf_factor_table)
        for _row in range(self.nbr_row):
            _table_line = []
            for _col in range(self.nbr_column):
                _field = _sf_factor_table[_row][_col]
                _field_split = _field.split("=")
                if _row == 0:
                    full_sf_factor_labels.append(_field_split[0])
                _table_line.append(_field_split[1])
            full_sf_factor_table.append(_table_line)

        self.full_sf_factor_table = full_sf_factor_table
        self.full_sf_factor_labels = full_sf_factor_labels
