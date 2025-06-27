from enum import Enum
from typing import Optional, Union

import numpy as np

from refred.calculations.lr_data import LRData
from refred.lconfigdataset import LConfigDataset


class TableDataColumIndex(Enum):
    r"""Enumeration to associate each column index of a TableData instance with a word"""

    LR_DATA = 0
    LR_NORM = 1
    LR_CONFIG = 2

    def __int__(self) -> int:
        return self.value


class TableData(np.ndarray):
    r"""A numpy ndarray with getter/setter methods named in the contexts of the application"""

    # Constructor, inheriting from numpy's ndarray
    def __new__(cls, max_row_count: int, dtype=object):
        # Create an empty array of given shape
        obj = np.empty((max_row_count, len(TableDataColumIndex)), dtype).view(cls)
        return obj

    @staticmethod
    def _validate_type(column: TableDataColumIndex, value: Optional[Union[LRData, LConfigDataset]]):
        valid_types = {
            TableDataColumIndex.LR_DATA: (type(None), LRData),
            TableDataColumIndex.LR_NORM: (type(None), LRData),
            TableDataColumIndex.LR_CONFIG: (type(None), LConfigDataset),
        }
        if not isinstance(value, valid_types[column]):
            raise TypeError(f"Wrong type for {value}. Valid types are {valid_types[column]}")

    def get_data_by_column_enum(self, row_index: int, column: TableDataColumIndex):
        return self[row_index, int(column)]

    def set_data_by_column_enum(
        self, row_index: int, column: TableDataColumIndex, value: Optional[Union[LRData, LConfigDataset]]
    ):
        self._validate_type(column, value)
        self[row_index, int(column)] = value

    def reflectometry_data(self, row_index: int) -> LRData:
        r"""Information about the reflectometry run

        Parameters
        ----------
        row_index
            row index of the table containing the reflectometry run of interest
        """
        return self.get_data_by_column_enum(row_index, TableDataColumIndex.LR_DATA)

    def set_reflectometry_data(self, row_index: int, value: Optional[LRData]):
        r"""Insert the information about the reflectometry run in the table at the given row

        Parameters
        ----------
        row_index
            row index of the table to insert the reflectometry run of interest
        value
            reflectometry information

        Raises
        ------
        TypeError
            value is neither `None` nor an instance of class LRData
        """
        self.set_data_by_column_enum(row_index, TableDataColumIndex.LR_DATA, value)

    def normalization_data(self, row_index: int) -> Optional[LRData]:
        r"""Information about the direct beam run

        Parameters
        ----------
        row_index
            row index of the table containing the direct beam run of interest
        """
        return self.get_data_by_column_enum(row_index, TableDataColumIndex.LR_NORM)

    def set_normalization_data(self, row_index: int, value: Optional[LRData]):
        r"""Insert the information about the direct beam run in the table at the given row.

        Parameters
        ----------
        row_index
            row index of the table to insert the direct beam run of interest
        value
            direct beam information

        Raises
        ------
        TypeError
            value is neither `None` nor an instance of class LRData
        """
        self.set_data_by_column_enum(row_index, TableDataColumIndex.LR_NORM, value)

    def reduction_config(self, row_index: int) -> LConfigDataset:
        r"""Information about all parameters pertaining to setting the reduction.

        Parameters
        ----------
        row_index
            row index of the table containing the reduction configuration of interest
        """
        return self.get_data_by_column_enum(row_index, TableDataColumIndex.LR_CONFIG)

    def set_reduction_config(self, row_index: int, value: Optional[LConfigDataset]):
        r"""Insert the information about all parameters pertaining to setting the reduction
        in the table at the given row.

        Parameters
        ----------
        row_index
            row index of the table containing the reduction configuration of interest
        value
            reduction configuration object

        Raises
        ------
        TypeError
            value is neither `None` nor an instance of class LConfigDataset
        """
        self.set_data_by_column_enum(row_index, TableDataColumIndex.LR_CONFIG, value)

    def expunge_rows(self, row_begin: int, row_end: int):
        r"""Delete rows with indexes in the range [row_begin, row_end)

        The table is appended with as many rows as deleted to keep the size unchanged. The
        elements of the appended rows are all `None`

        Parameters
        ----------
        row_begin : int
            The index of the row where the clearing process should begin.

        row_end : int
            The index of the row where the clearing process should end, this excluded

        Raises
        ------
            Parameter row_end matches or exceeds the length of the Table
        """
        if row_end >= len(self):
            raise ValueError("Row_end matches or exceeds the length of the Table")
        # Set the values of the rows in the range (begin, end) to "None"
        self[row_begin:row_end, :] = None
        # Move cleared rows to the end by first concatenating non-cleared rows with cleared ones
        self[:] = np.vstack((self[0:row_begin, :], self[row_end:, :], self[row_begin:row_end, :]))
