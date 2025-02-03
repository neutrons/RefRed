#!/usr/bin/env python
'''
Small program for quick access to SNS liquids reflectometer raw data.
'''
import os
import sys

# import mantid once before qt, this fixes some issues with running in production
import mantid  # noqa: F401

# must be imported through qtpy before any other gui imports
from qtpy.QtWidgets import QApplication, QSplashScreen
from qtpy.QtGui import QPixmap
from qtpy.QtCore import Qt  # type: ignore

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
        % version,
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
    from RefRed import __version__ as version
    from RefRed.main import MainGui

    sys.exit(_run(sys.argv[1:]))
