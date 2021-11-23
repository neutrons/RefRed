#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
  Small program for quick access to SNS liquids reflectometer raw data.
'''
import os
import sys

# import mantid once before qt, this fixes some issues with running in production
import mantid

# must be imported through qtpy before any other gui imports
from qtpy.QtWidgets import QApplication, QSplashScreen
from qtpy.QtGui import QPixmap
from qtpy.QtCore import Qt


def mantid_location(valid_versions, root_location='/opt'):
    r"""
    Find the location of mantid's installation. Locations under /opt are preferred over local installs.
    :param List[str] valid_versions: mantid versions. each with format 'Major.Minor.Patch', e.g. '6.0.0'
    :return str: absolute path to mantid installation
    :except ImportError: a valid version of Mantid is not found
    """

    mantid_path = None  # value to return by this function

    # Check for installed Mantid versions under /opt
    short_version = {'6.1.0': '61', '6.0.0': '60', '5.1.0': '51'}
    for _version in valid_versions:
        install_path = os.path.join(root_location, 'mantid' + short_version[_version])  # e.g "/opt/mantid51"
        if os.path.isdir(install_path):  # check only for the existence of the directory, but not its contents
            mantid_path = install_path
            break

    # Check location in the PYTHONPATH
    if not mantid_path:
        try:
            import mantid

            mantid_version = mantid.__version__
        except ImportError:
            raise ImportError('Could not find a version of Mantid')
        if mantid_version not in valid_versions:
            raise ImportError('Mantid version is not one of ' + str(valid_versions))
        mantid_path = os.path.dirname(mantid.__file__)

    return mantid_path


# TODO fetch the valid versions from a configuration file
# mantid_path = mantid_location(['5.1.0'], root_location='/opt')
# sys.path.insert(0, os.path.join(mantid_path, 'bin'))
# sys.path.insert(1, os.path.join(mantid_path, 'lib'))


# if script was run from commandline
try:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    if current_directory.endswith('RefRed/scripts'):
        sys.path.insert(0, os.path.dirname(current_directory))
except NameError:
    pass


def _run(argv=[]):
    app = QApplication(argv)
    splash = QSplashScreen(QPixmap(':/General/logo_refl_hq.png'))
    splash.showMessage(
        """<html>
                       <div style="margin-bottom: 420;"> &nbsp;</div>
                       <div style="font-size: 12pt; margin-bottom: 15;">
                       <b>RefRed</b> Version %s
                       </div>
                       <div>Starting up...</div>
                       </html>"""
        % version.str_version,
        alignment=Qt.AlignBottom | Qt.AlignHCenter,
    )
    splash.show()
    QApplication.processEvents()

    window = MainGui(argv)
    window.show()
    splash.finish(window)
    return app.exec_()


if __name__ == '__main__':
    # from RefRed import config
    from RefRed import version
    from RefRed.main import MainGui

    sys.exit(_run(sys.argv[1:]))
