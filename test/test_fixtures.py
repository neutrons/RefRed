# third party packages
import pytest

# standard packages
from pathlib import Path


def test_data_server(data_server):
    assert Path(data_server.path_to('easy_data_set.csv')).exists()
    with pytest.raises(FileNotFoundError):
        Path(data_server.path_to('impossibe_to_find.dat')).exists()


if __name__ == '__main__':
    pytest.main([__file__])
