
# third party packages
from numpy.testing import assert_allclose
import pytest  # PYTEST documentation at https://docs.pytest.org/

# standard packages
from typing import List


# Helper functions to showcase some features of pytest
def example_function() -> List[float]:
    r"""Serve three floating-point numbers"""
    return [1.005, 1.999, 3.009]


def raises_exception(a: float, b: float) -> float:
    r"""A function that for throws a custom message when dividing by zero

    Docstrings style follows the
    `Numpy style <https://numpydoc.readthedocs.io/en/latest/format.html>`_

    :param a: numerator
    :param b: denominator

    :return: Division of the numerator and denominator
    :raise ZeroDivisionError: When the denominator is zero
    """
    try:
        c = a / b  # will raise an exception if b == 0.0
    except ZeroDivisionError:
        raise ZeroDivisionError('Do not divide by zero, please')  # custom message
    return c


def read_file(input_file: str) -> str:
    r"""Returns the contents of a file"""
    return open(input_file).read()


# Encapsulate all your tests for your script under a test-suite class
class TestExampleScript:

    def test_my_function(self):
        r"""Compare some expected value to the obtained value after running your script"""
        expected = [1, 2, 3]
        obtained = example_function()
        assert_allclose(expected, obtained, atol=0.01)  # numpy.testing functionality
        assert obtained == pytest.approx(obtained, abs=0.01)  # pytest testing functionality

    def test_raises_exception(self):
        r"""How to test when your code is throwing an exception"""
        with pytest.raises(ZeroDivisionError) as exception_info:
            raises_exception(1.0, 0.0)  # divide by zero raises exception
        assert 'Do not divide by zero' in str(exception_info.value)  # checks part of the error message

    def test_read_file(self, data_server):  # 'data_server' is a magic pytest fixture. See file conftest.py
        r"""Using data files located within directory tests/data/"""
        # read file tests/data/test_file_1.dat
        path_to_file = data_server.path_to('easy_data_set.csv')
        assert '285,3,1.732050808' in read_file(path_to_file)
        # read file tests/data/examples/test_file_2.dat
        #path_to_file = data_server.path_to('examples/test_file_2.dat')
        #assert 'Bye World!' in read_file(path_to_file)


if __name__ == '__main__':
    pytest.main([__file__])
