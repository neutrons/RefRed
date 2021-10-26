import numpy as np
from typing import List


class AsciiLoader:
    def __init__(self, filename: str = "", nbr_col: int = 3):
        # error handling
        if nbr_col != 3:
            raise RuntimeError("only 3 supported for now!")

        if filename:
            self.filename = filename
        else:
            raise RuntimeError("filename is empty!")

    def data(self) -> List[np.ndarray]:
        data = np.genfromtxt(self.filename, dtype=float, comments="#")
        return [data[:, 0], data[:, 1], data[:, 2], []]
