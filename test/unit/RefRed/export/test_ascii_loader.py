import tempfile
from pathlib import Path

import numpy as np
import pytest

from RefRed.export import ascii_loader


class TestAsciiLoader:
    def setup_class(self):
        # create a temp file to load and verify
        np.random.seed(42)
        # NOTE: numpy.savetxt will prepend # for the header
        self.header = "\t".join([f"{i}_header" for i in range(3)])
        self.refdata = np.random.random(10 * 3).reshape(10, 3)

    def teardown_class(self):
        print(f"Test tear down for {self}")

    def test_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # make the file
            fn = Path(tmpdir) / "test.txt"
            np.savetxt(str(fn), self.refdata, header=self.header)
            # load the file
            loader = ascii_loader.AsciiLoader(str(fn))
            data = loader.data()
            # verify
            for i in range(3):
                np.testing.assert_array_almost_equal(data[i], self.refdata[:, i])


if __name__ == "__main__":
    pytest.main([__file__])
