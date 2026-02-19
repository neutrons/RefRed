from unittest.mock import MagicMock

import numpy as np
import pytest

from refred.gui_handling.fill_stitching_table import FillStitchingTable
from refred.lconfigdataset import LConfigDataset
from refred.tabledata import TableData


def _make_config(q_values, sf_auto=1.0, sf_auto_found_match=True):
    """Create an LConfigDataset with given q values and scaling factor."""
    config = LConfigDataset()
    config.q_axis_for_display = np.array(q_values, dtype=float)
    config.sf_auto = sf_auto
    config.sf_abs_normalization = 1.0
    config.sf_manual = 1.0
    config.sf_auto_found_match = sf_auto_found_match
    return config


def _make_mock_parent(big_table_data, run_numbers, stitching_type="auto"):
    """Build a mock parent with the required UI widgets.

    Parameters
    ----------
    big_table_data : TableData
        The populated table data.
    run_numbers : list[str]
        Run number strings, one per populated row.
    stitching_type : str
        One of "auto", "absolute", "manual".
    """
    parent = MagicMock()
    parent.big_table_data = big_table_data

    # Mock reductionTable items — maps (row, col=1) to run number text
    def reduction_table_item(row, col):
        item = MagicMock()
        if col == 1 and row < len(run_numbers):
            item.text.return_value = run_numbers[row]
        else:
            item.text.return_value = ""
        return item

    parent.ui.reductionTable.item = reduction_table_item

    # Mock dataStitchingTable with a real dict to capture setItem calls
    stitching_items = {}

    def set_stitching_item(row, col, item):
        stitching_items[(row, col)] = item

    parent.ui.dataStitchingTable.setItem = set_stitching_item
    parent.ui.dataStitchingTable.setCellWidget = MagicMock()
    parent._stitching_items = stitching_items

    # Mock the stitching type radio buttons
    parent.ui.absolute_normalization_button.isChecked.return_value = stitching_type == "absolute"
    parent.ui.auto_stitching_button.isChecked.return_value = stitching_type == "auto"
    parent.ui.manual_stitching_button.isChecked.return_value = stitching_type == "manual"

    return parent


class TestDataStitchingTable:
    """Tests that the data stitching table fills the rows in the correct order."""

    def test_runs_listed_in_ascending_q_order(self):
        """Runs stored out of q-order in big_table_data appear sorted in the stitching table."""
        table = TableData(5)
        # Row 0: highest q (run 333)
        table.set_reduction_config(0, _make_config([0.07, 0.08, 0.09]))
        # Row 1: lowest q (run 111)
        table.set_reduction_config(1, _make_config([0.01, 0.02, 0.03]))
        # Row 2: middle q (run 222)
        table.set_reduction_config(2, _make_config([0.04, 0.05, 0.06]))

        run_numbers = ["333", "111", "222"]
        parent = _make_mock_parent(table, run_numbers, stitching_type="auto")

        sorted_indices = table.get_q_sorted_indices()
        assert sorted_indices == [1, 2, 0]

        o_fill = FillStitchingTable(parent=parent)
        for stitching_row, original_row in enumerate(sorted_indices):
            o_fill.fillRow(row_index=original_row, stitching_row=stitching_row)

        items = parent._stitching_items
        # Stitching table row 0 should have run "111" (lowest q)
        assert items[(0, 0)].text() == "111"
        # Stitching table row 1 should have run "222" (middle q)
        assert items[(1, 0)].text() == "222"
        # Stitching table row 2 should have run "333" (highest q)
        assert items[(2, 0)].text() == "333"

    def test_already_sorted_rows_preserve_order(self):
        """When big_table_data rows are already in q order, stitching table matches."""
        table = TableData(5)
        table.set_reduction_config(0, _make_config([0.01, 0.02]))
        table.set_reduction_config(1, _make_config([0.03, 0.04]))

        run_numbers = ["100", "200"]
        parent = _make_mock_parent(table, run_numbers, stitching_type="auto")

        sorted_indices = table.get_q_sorted_indices()
        assert sorted_indices == [0, 1]

        o_fill = FillStitchingTable(parent=parent)
        for stitching_row, original_row in enumerate(sorted_indices):
            o_fill.fillRow(row_index=original_row, stitching_row=stitching_row)

        items = parent._stitching_items
        assert items[(0, 0)].text() == "100"
        assert items[(1, 0)].text() == "200"

    def test_single_row(self):
        """A single row should appear at stitching row 0."""
        table = TableData(5)
        table.set_reduction_config(0, _make_config([0.05, 0.06]))

        run_numbers = ["999"]
        parent = _make_mock_parent(table, run_numbers, stitching_type="absolute")

        sorted_indices = table.get_q_sorted_indices()
        assert sorted_indices == [0]

        o_fill = FillStitchingTable(parent=parent)
        for stitching_row, original_row in enumerate(sorted_indices):
            o_fill.fillRow(row_index=original_row, stitching_row=stitching_row)

        items = parent._stitching_items
        assert items[(0, 0)].text() == "999"

    def test_four_runs_scrambled(self):
        """Four runs in scrambled q-order should appear sorted in the stitching table."""
        table = TableData(6)
        table.set_reduction_config(0, _make_config([0.05, 0.06]))  # 3rd
        table.set_reduction_config(1, _make_config([0.09, 0.10]))  # 4th
        table.set_reduction_config(2, _make_config([0.01, 0.02]))  # 1st
        table.set_reduction_config(3, _make_config([0.03, 0.04]))  # 2nd

        run_numbers = ["AAA", "BBB", "CCC", "DDD"]
        parent = _make_mock_parent(table, run_numbers, stitching_type="auto")

        sorted_indices = table.get_q_sorted_indices()
        assert sorted_indices == [2, 3, 0, 1]

        o_fill = FillStitchingTable(parent=parent)
        for stitching_row, original_row in enumerate(sorted_indices):
            o_fill.fillRow(row_index=original_row, stitching_row=stitching_row)

        items = parent._stitching_items
        assert items[(0, 0)].text() == "CCC"
        assert items[(1, 0)].text() == "DDD"
        assert items[(2, 0)].text() == "AAA"
        assert items[(3, 0)].text() == "BBB"


if __name__ == "__main__":
    pytest.main([__file__])
