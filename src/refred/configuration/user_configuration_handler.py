import os

from qtpy.QtCore import QSettings  # type: ignore

from refred import APPNAME, ORGANIZATION
from refred.configuration.user_configuration import UserConfiguration
from refred.utilities import str2bool


class RetrieveUserConfiguration(object):
    def __init__(self, parent=None):
        self.parent = parent

        settings = QSettings(ORGANIZATION, APPNAME)
        self.parent.path_ascii = str(settings.value("path_ascii", os.path.expanduser("~")))

        self.parent.path_config = str(settings.value("path_config", os.path.expanduser("~")))

        o_user_config = UserConfiguration()
        ylog_value = str(settings.value("is_reduced_plot_stitching_tab_ylog"))
        if ylog_value != "":
            o_user_config.is_reduced_plot_stitching_tab_ylog = str2bool(ylog_value)
        xlog_value = str(settings.value("is_reduced_plot_stitching_tab_xlog"))
        if xlog_value != "":
            o_user_config.is_reduced_plot_stitching_tab_xlog = str2bool(xlog_value)
        self.parent.o_user_configuration = o_user_config


class SaveUserConfiguration(object):
    def __init__(self, parent=None):
        self.parent = parent

        settings = QSettings(ORGANIZATION, APPNAME)
        settings.setValue("path_ascii", self.parent.path_ascii)
        settings.setValue("path_config", self.parent.path_config)

        o_user_config = self.parent.o_user_configuration
        settings.setValue("is_reduced_plot_stitching_tab_xlog", str(o_user_config.is_reduced_plot_stitching_tab_xlog))
        settings.setValue("is_reduced_plot_stitching_tab_ylog", str(o_user_config.is_reduced_plot_stitching_tab_ylog))
