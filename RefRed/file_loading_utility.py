"""
TODO: verify whether this is really needed
"""

# third party packages
import numpy as np


def loadCsvFile(filename):
    r"""Loading CSV file created with Excel to test PeakFinderDerivation algorithm
    :param str filename: Absolute path to CSV file
    :return List[float]:Three-item list, each item being one file column
    """
    return [column.tolist() for column in np.genfromtxt(filename, delimiter=",").transpose()]
