import numpy as np

Filepath = str


class AsciiLoader:
    def __init__(self, filename: Filepath = "", nbr_col: int = 3):
        # error handling
        if nbr_col != 3:
            raise RuntimeError("only 3 supported for now!")

        if filename:
            self.filename = filename
        else:
            raise RuntimeError("filename is empty!")

        self.__data = np.genfromtxt(self.filename, dtype=float, comments="#")

    def data(self):
        data = self.__data
        return [data[:, 0], data[:, 1], data[:, 2], []]
