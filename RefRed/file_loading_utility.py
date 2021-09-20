"""
    TODO: verify whether this is really needed
"""

# third party packages
import numpy as np

# standard packages
from typing import List


def loadCsvFile(filename: str) -> List[float]:
    r"""Loading CSV file created with Excel to test PeakFinderDerivation algorithm
    :param filename: Absolute path to CSV file
    :return:Three-item list, each item being one file column
    """
    return [column.tolist() for column in np.genfromtxt(filename, delimiter=',').transpose()]
