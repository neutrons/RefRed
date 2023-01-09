from mantid.kernel import ConfigService


class MantidConfig(object):
    def __init__(self, parent=None):
        self.parent = parent
        ConfigService.Instance().setString("default.instrument", "REF_L")
        ConfigService.Instance().setString("default.facility", "SNS")
        ConfigService.Instance().setString("datasearch.searcharchive", "sns")
