import pytest
from RefRed.sf_calculator.reduction_sf_calculator import ReductionSfCalculator


def test_class_reduction_sf_calculator():
    """Test class ReductionSfCalculator
    """
    # Init
    test_reducer = ReductionSfCalculator(None, None)



if __name__ == '__main__':
    pytest.main([__file__])
