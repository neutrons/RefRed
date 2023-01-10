import pytest
import numpy as np
from RefRed.utilities import convert_tof_values_unit


def test_convert_tof_list():
    """Unit test on RefRed.utilities"""
    # Gold input
    tof_list = [2000.0, 32100.0]

    # Test same unit
    same_list_micros = convert_tof_values_unit(tof_list, 'micros', 'micros')
    assert tof_list == same_list_micros

    # Test conversion
    to_list_micros = convert_tof_values_unit(tof_list, 'ms', 'micros')
    # the change will be changed in place
    assert to_list_micros[0] == tof_list[0]
    assert to_list_micros[1] == tof_list[1]
    # the value will be increased by 1000 from previous
    assert to_list_micros[0] == 2000.0 * 1000.0
    assert to_list_micros[1] == 32100.0 * 1000.0


def test_convert_tof_array():
    """Unit test on RefRed.utilities"""
    # Gold input
    tof_list = np.array([2000.0, 32100.0])

    # Test same unit
    same_list_ms = convert_tof_values_unit(tof_list, 'ms', 'ms')
    np.testing.assert_allclose(tof_list, same_list_ms)

    # Test conversion
    to_list_ms = convert_tof_values_unit(tof_list, 'micros', 'ms')
    # the change will be changed in place
    assert to_list_ms[0] == tof_list[0]
    assert to_list_ms[1] == tof_list[1]
    # the value will be decreased by 1000 times from previous
    assert to_list_ms[0] == 2.0
    assert to_list_ms[1] == 32.1


def test_convert_tof_none():
    """Unit test on RefRed.utilities"""
    # Input
    none_tofs = None

    # Output
    none_output = convert_tof_values_unit(none_tofs, 'ms', 'ms')
    assert none_output is None

    # assert throw
    with pytest.raises(NameError):
        convert_tof_values_unit(none_tofs, 'micro', 'ms')


if __name__ == '__main__':
    pytest.main([__file__])
