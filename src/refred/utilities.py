import math
import os
from random import randint
from typing import Union

import numpy as np

from refred import nexus_utilities


def convert_angle(angle=0, from_units="degree", to_units="rad"):
    """
    To convert angles from degree/rad to rad/degree
    """

    if from_units == to_units:
        return angle

    if from_units == "degree" and to_units == "rad":
        coeff = math.pi / float(180)
    elif from_units == "rad" and to_units == "degree":
        coeff = float(180) / math.pi
    else:
        coeff = 1
    return float(angle) * coeff


def arrayByValue(array, value):
    for [index, _ele] in enumerate(array):
        array[index] = float(array[index]) * value
    return array


def convertTOF(TOFarray=None, from_units="micros", to_units="ms"):
    try:
        if TOFarray is None:
            return None
        if from_units == to_units:
            return TOFarray
        if from_units == "micros":
            if to_units == "ms":
                return arrayByValue(TOFarray, 0.001)
            else:
                raise NameError(to_units)
        elif from_units == "ms":
            if to_units == "micros":
                return arrayByValue(TOFarray, 1000)
            else:
                raise NameError(to_units)
        else:
            raise NameError(from_units)
    except NameError:
        print("units not supported")
        return None


def convert_tof_values_unit(tof_array: Union[None, list, np.ndarray], from_units: str = "micros", to_units: str = "ms"):
    """Convert an array, supposed to be TOF values, from one unit to another

    Parameters
    ----------
    tof_array: None or list or numpy.array
        TOF array and it will be modified in place
    from_units: str
        current unit
    to_units: str
        target unit

    Returns
    -------
    None, list, numpy.ndarray
        array/list of TOF values

    """

    def multiply_by_value(array, value: Union[float, int]):
        """Multiply an array (list, numpy.array) by a value and return new array with same type"""
        for [index, _ele] in enumerate(array):
            array[index] = float(array[index]) * value
        return array

    # Check input and output units
    allowed_units = ["micros", "ms"]
    if from_units not in allowed_units or to_units not in allowed_units:
        raise NameError(f"Input and output units can be micros and ms only but not {from_units} or {to_units}")

    if tof_array is None or from_units == to_units:
        # case 1: None input or
        # case 2: to unit is equal to from unit
        return tof_array

    elif from_units == "micros":
        # convert from micros to ms
        return multiply_by_value(tof_array, 0.001)

    elif from_units == "ms":
        # convert from ms to micros
        return multiply_by_value(tof_array, 1000)

    raise RuntimeError("Impossible")


def output_2d_ascii_file(filename, image):
    with open(filename, "w") as f:
        sz = image.shape
        dim1 = sz[0]
        dim2 = sz[1]
        for px in range(dim1):
            _line = ""
            for t in range(dim2):
                _line += str(image[px, t])
                _line += " "
            _line += "\n"
            f.write(_line)


def import_ascii_file(filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
    except:
        data = []
    return data


def write_ascii_file(filename, text):
    """
    produce the output ascii file
    """
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        for _line in text:
            f.write(_line + "\n")


def generate_random_workspace_name():
    """
    This will generate a random workspace name to avoid conflict names
    """
    string = "abcdefghijklmnopqrstuvwxyz1234567890"
    stringList = list(string)
    nbrPara = len(stringList)

    listRand = []
    for i in range(5):
        _tmp = stringList[randint(0, nbrPara - 1)]
        listRand.append(_tmp)

    randomString = "".join(listRand)
    return randomString


def touch(full_file_name):
    with open(full_file_name, "a"):
        os.utime(full_file_name, None)


def makeSureFileHasExtension(filename, default_ext=".xml"):
    _, file_extension = os.path.splitext(filename)
    if file_extension == "":
        filename += default_ext
    return filename


def findFullFileName(run_number):
    try:
        full_file_name = nexus_utilities.findNeXusFullPath(run_number)
    except:
        full_file_name = ""
    return full_file_name


def str2bool(v):
    try:
        return v.lower() in ("yes", "true", "t", "1")
    except:
        if float(v) == 0:
            return False
        else:
            return True


def removeEmptyStrElementAndUpdateIndexSelected(str_list, index_selected):
    sz = len(str_list)
    final_list = []
    final_index = index_selected
    for i in range(sz):
        _element = str_list[i]
        if _element.strip() != "":
            final_list.append(_element)
        else:
            if final_index >= i:
                final_index -= 1
    return [final_list, final_index]


def format_to_list(values):
    if isinstance(values, list):
        return values
    else:
        return [values]


def get_index_free_thread(parent=None):
    nbr_max_thread = len(parent.loading_nxs_thread)
    index_free_thread = parent.index_free_thread
    new_index = index_free_thread + 1
    if new_index == nbr_max_thread:
        new_index = 0
    parent.index_free_thread = new_index
    return new_index
