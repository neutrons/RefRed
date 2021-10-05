import mantid.simpleapi as api


class LoadNexus(object):
    filename = None
    output_wks = None
    metadata_only = False
    workspace = None

    def __init__(self, filename=None, output_wks=None, metadata_only=False):
        self.filename = filename
        self.output_wks = output_wks
        self.metadata_only = metadata_only
        self.workspace = api.LoadEventNexus(
            Filename=self.filename, OutputWorkspace=self.output_wks, MetadataOnly=self.metadata_only
        )
