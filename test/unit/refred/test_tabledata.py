from unittest.mock import patch

import numpy as np
import pytest

from refred.calculations.lr_data import LRData
from refred.lconfigdataset import LConfigDataset
from refred.tabledata import TableData, TableDataColumIndex


class TestTableData:
    ROW_COUNT = 42

    def setup_method(self):
        self.table = TableData(42)

    def test_init(self):
        assert self.table.shape == (self.ROW_COUNT, len(TableDataColumIndex))

    def test_set_data_by_column_enum_raises(self):
        for column in TableDataColumIndex:
            with pytest.raises(TypeError) as exception:
                self.table.set_data_by_column_enum(0, column, "wrong_type")
            assert "Wrong type for wrong_type" in str(exception.value)

    def test_set_data_by_column_enum(self):
        with patch.object(LRData, "__init__", return_value=None):
            instance = LRData()
            self.table.set_data_by_column_enum(0, TableDataColumIndex.LR_DATA, instance)
            self.table.set_data_by_column_enum(0, TableDataColumIndex.LR_NORM, instance)
        self.table.set_data_by_column_enum(0, TableDataColumIndex.LR_CONFIG, LConfigDataset())

    def test_reflectometry_data(self):
        with patch.object(LRData, "__init__", return_value=None):
            self.table.set_reflectometry_data(0, LRData())
            assert isinstance(self.table.reflectometry_data(0), LRData)
            assert isinstance(self.table[0, int(TableDataColumIndex.LR_DATA)], LRData)

    def test_normalization_data(self):
        with patch.object(LRData, "__init__", return_value=None):
            self.table.set_normalization_data(0, LRData())
            assert isinstance(self.table.normalization_data(0), LRData)
            assert isinstance(self.table[0, int(TableDataColumIndex.LR_NORM)], LRData)

    def test_reduction_config(self):
        self.table.set_reduction_config(0, LConfigDataset())
        assert isinstance(self.table.reduction_config(0), LConfigDataset)
        assert isinstance(self.table[0, int(TableDataColumIndex.LR_CONFIG)], LConfigDataset)

    def test_expunge_rows(self):
        # populate the table with very simple reduction-configuration objects
        for row_index in range(len(self.table)):
            config = LConfigDataset()
            config.counter = row_index
            self.table.set_reduction_config(row_index, config)
        # check the counter for each row
        counters = list()
        for row_index in range(len(self.table)):
            config = self.table.reduction_config(row_index)
            counters.append(config.counter)
        assert counters == list(range(len(self.table)))
        # remove rows with indexes 4 to 9, then collect the counters
        row_begin, row_end = 4, 10
        self.table.expunge_rows(row_begin, row_end)
        # check the size of the table is preserved
        assert len(self.table) == self.ROW_COUNT
        # check the last items in the table are None
        first_index = self.ROW_COUNT - (row_end - row_begin)
        for row_index in range(first_index, self.ROW_COUNT):
            assert self.table.reduction_config(row_index) is None
        new_counters = list()
        for row_index in range(len(self.table)):
            config = self.table.reduction_config(row_index)
            if config:
                new_counters.append(config.counter)
        assert len(new_counters) == len(counters) - (row_end - row_begin)
        # remove the expunged counters from list `counters`
        for row_index in range(row_begin, row_end):
            del counters[row_begin]
        assert new_counters == counters

    def _make_config_with_q(self, q_values):
        """Helper to create an LConfigDataset with the given q_axis_for_display."""
        config = LConfigDataset()
        config.q_axis_for_display = np.array(q_values, dtype=float)
        return config

    def test_get_q_sorted_indices_already_sorted(self):
        """Rows already in ascending q order should be returned as-is."""
        self.table.set_reduction_config(0, self._make_config_with_q([0.01, 0.02, 0.03]))
        self.table.set_reduction_config(1, self._make_config_with_q([0.04, 0.05, 0.06]))
        self.table.set_reduction_config(2, self._make_config_with_q([0.07, 0.08, 0.09]))
        assert self.table.get_q_sorted_indices() == [0, 1, 2]

    def test_get_q_sorted_indices_reverse_order(self):
        """Rows in descending q order should be reversed."""
        self.table.set_reduction_config(0, self._make_config_with_q([0.07, 0.08, 0.09]))
        self.table.set_reduction_config(1, self._make_config_with_q([0.04, 0.05, 0.06]))
        self.table.set_reduction_config(2, self._make_config_with_q([0.01, 0.02, 0.03]))
        assert self.table.get_q_sorted_indices() == [2, 1, 0]

    def test_get_q_sorted_indices_scrambled(self):
        """Rows in arbitrary order should be sorted by ascending min(q)."""
        self.table.set_reduction_config(0, self._make_config_with_q([0.04, 0.05, 0.06]))
        self.table.set_reduction_config(1, self._make_config_with_q([0.01, 0.02, 0.03]))
        self.table.set_reduction_config(2, self._make_config_with_q([0.07, 0.08, 0.09]))
        assert self.table.get_q_sorted_indices() == [1, 0, 2]

    def test_get_q_sorted_indices_single_row(self):
        """A single populated row should return a single-element list."""
        self.table.set_reduction_config(0, self._make_config_with_q([0.05, 0.06]))
        assert self.table.get_q_sorted_indices() == [0]

    def test_get_q_sorted_indices_empty_table(self):
        """A table with no reduction configs should return an empty list."""
        assert self.table.get_q_sorted_indices() == []

    def test_get_q_sorted_indices_overlapping_q_ranges(self):
        """Rows with overlapping q ranges should sort by their minimum q value."""
        self.table.set_reduction_config(0, self._make_config_with_q([0.03, 0.05, 0.07]))
        self.table.set_reduction_config(1, self._make_config_with_q([0.01, 0.04, 0.06]))
        self.table.set_reduction_config(2, self._make_config_with_q([0.02, 0.03, 0.08]))
        assert self.table.get_q_sorted_indices() == [1, 2, 0]


if __name__ == "__main__":
    pytest.main([__file__])
