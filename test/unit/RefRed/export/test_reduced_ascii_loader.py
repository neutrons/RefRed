import tempfile
import unittest.mock as mock
from pathlib import Path

import numpy as np
import pytest

from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader


class TestReducedAsciiLoader:
    def setup_class(self):
        # make a fake parent
        self.parent = mock.Mock()
        self.parent.big_table_data = "big_table_data"
        # data
        np.random.seed(42)
        self.header = "\t".join([f"{i}_header" for i in range(3)])
        self.refdata = np.random.random(10 * 3).reshape(10, 3)

    def teardown_class(self):
        pass

    def test_livereduction(self):
        # live reduction case
        ral = ReducedAsciiLoader(
            self.parent,
            ascii_file_name="doesnotMatter",
            is_live_reduction=True,
        )
        # check
        assert ral.ascii_file_name == "LAST REDUCED SET"
        assert ral.short_ascii_file_name == "LAST REDUCED SET"
        assert ral.big_table_data == "big_table_data"
        assert ral.isEnabled

    def test_reduction(self):
        # NOTE:
        # This is almost a duplicated test for ascii loader since this class is
        # almost a wrapper of a wrapper of a wrapper ...
        with tempfile.TemporaryDirectory() as tmpdir:
            # make the file
            fn = Path(tmpdir) / "test.txt"
            np.savetxt(str(fn), self.refdata, header=self.header)
            # load via ReducedAsciiLoader
            ral = ReducedAsciiLoader(
                self.parent,
                ascii_file_name=fn,
                is_live_reduction=False,
            )
            # check
            assert ral.ascii_file_name == fn
            assert ral.short_ascii_file_name == "test.txt"
            # verify data
            np.testing.assert_array_almost_equal(ral.col1, self.refdata[:, 0])
            np.testing.assert_array_almost_equal(ral.col2, self.refdata[:, 1])
            np.testing.assert_array_almost_equal(ral.col3, self.refdata[:, 2])
            assert ral.col4 == []


if __name__ == "__main__":
    pytest.main([__file__])
