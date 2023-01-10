import pytest
from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker


def test_run_sequence_breaker():
    """Test  RefRed.calculations.run_sequence_breaker.RunSequenceBreaker

    Unit test data is from documented use case
    https://github.com/neutrons/RefRed/blob/next/docs/compute-scaling-factors.rst.
    Expected result is obtained by RefRed-production release (python 2.7 version)
    """
    # Test input
    test_run_sequence = '184975-184989'
    gold_run_list = [
        184975,
        184976,
        184977,
        184978,
        184979,
        184980,
        184981,
        184982,
        184983,
        184984,
        184985,
        184986,
        184987,
        184988,
        184989,
    ]

    # Init
    test_breaker = RunSequenceBreaker(test_run_sequence)
    assert test_breaker

    # Verify
    final_list = test_breaker.getFinalList()
    assert isinstance(final_list, list)
    assert final_list == gold_run_list


if __name__ == '__main__':
    pytest.main([__file__])
