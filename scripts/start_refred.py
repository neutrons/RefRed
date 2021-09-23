#!/usr/bin/env python
#-*- coding: utf8 -*-
'''
  Small program for quick access to SNS liquids reflectometer raw data.
'''
import os
import sys
# must be imported through qtpy before any other gui imports
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.QtCore import Qt

sys.path.insert(0, "/opt/mantid42/bin")
sys.path.insert(1, "/opt/mantid42/lib")

# if script was run from commandline
try:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    if current_directory.endswith('RefRed/scripts'):
        sys.path.insert(0, os.path.dirname(current_directory))
except NameError:
    pass

def _run(argv=[]):
    app=QApplication(argv)
    splash=QSplashScreen(QPixmap(':/General/logo_refl_hq.png'))
    splash.showMessage("""<html>
                       <div style="margin-bottom: 420;"> &nbsp;</div>
                       <div style="font-size: 12pt; margin-bottom: 15;">
                       <b>RefRed</b> Version %s
                       </div>
                       <div>Starting up...</div>
                       </html>"""%version.str_version,
                                 alignment=Qt.AlignBottom|Qt.AlignHCenter)
    splash.show()
    QApplication.processEvents()

    window=MainGui(argv)
    window.show()
    splash.finish(window)
    return app.exec_()

if __name__=='__main__':
    from RefRed import config
    from RefRed import version
    from RefRed.main import MainGui
    
    sys.exit(_run(sys.argv[1:]))
