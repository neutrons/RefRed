# third party packages
import pytest

# standard packages
from pathlib2 import Path


def test_data_server(data_server):
    assert Path(data_server.path_to('easy_data_set.csv')).exists()


if __name__ == '__main__':
    pytest.main([__file__])
