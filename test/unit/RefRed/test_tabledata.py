# standard imports
from unittest.mock import patch

# third party imports
import pytest

# application imports
from RefRed.calculations.lr_data import LRData
from RefRed.lconfigdataset import LConfigDataset
from RefRed.tabledata import TableData, TableDataColumIndex


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
        with patch.object(LRData, '__init__', return_value=None):
            instance = LRData()
            self.table.set_data_by_column_enum(0, TableDataColumIndex.LR_DATA, instance)
            self.table.set_data_by_column_enum(0, TableDataColumIndex.LR_NORM, instance)
        self.table.set_data_by_column_enum(0, TableDataColumIndex.LR_CONFIG, LConfigDataset())

    def test_reflectometry_data(self):
        with patch.object(LRData, '__init__', return_value=None):
            self.table.set_reflectometry_data(0, LRData())
            assert isinstance(self.table.reflectometry_data(0), LRData)
            assert isinstance(self.table[0, int(TableDataColumIndex.LR_DATA)], LRData)

    def test_normalization_data(self):
        with patch.object(LRData, '__init__', return_value=None):
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


if __name__ == '__main__':
    pytest.main([__file__])
