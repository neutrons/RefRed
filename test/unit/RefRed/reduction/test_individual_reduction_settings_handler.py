from unittest.mock import Mock

import pytest

from RefRed.reduction.individual_reduction_settings_handler import IndividualReductionSettingsHandler


class TestIndividualReductionSettingsHandler:
    def test_get_back_range(self):
        # Mock class to customize __init__
        class MockHandler(IndividualReductionSettingsHandler):
            def __init__(self, **kwargs):
                pass

        handler = MockHandler()
        data = Mock(back=[3, 2], back2=[1, 0])
        assert handler.get_back_range(data, is_data=True) == [2, 3, 0, 1]


if __name__ == "__main__":
    pytest.main([__file__])
