import os

from qtpy.QtWidgets import QWidget
from qtpy.uic import loadUi


def load_ui(ui_filename: str, baseinstance: QWidget):
    ui_filename = os.path.split(ui_filename)[-1]
    ui_path = os.path.dirname(__file__)

    # get the location of the ui directory
    # this function assumes that all ui files are there
    filename = os.path.join(ui_path, ui_filename)

    return loadUi(filename, baseinstance=baseinstance)
