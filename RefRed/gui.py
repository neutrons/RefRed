#!/usr/bin/env python
"""Start script for RefRed GUI."""

import sys

import lr_reduction
import mantid  # noqa: F401
from qtpy.QtCore import Qt  # type: ignore
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QApplication, QSplashScreen

from RefRed import __version__ as version

print(f"""##################################################
# RefRed {version}
#    with lr_reduction: {lr_reduction.__version__}
#    with Mantid:       {mantid.__version__}
##################################################
""")

from RefRed.main import MainGui


def main(argv=[]):
    app = QApplication(argv or [])
    splash = QSplashScreen(QPixmap(":/General/logo_refl_hq.png"))
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

    window = MainGui()
    window.show()
    splash.finish(window)
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
