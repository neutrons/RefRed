import mantid.simpleapi as api


class LoadNexus(object):
    def __init__(self, filename, output_wks=None, metadata_only=False):
        self.filename = filename
        if output_wks is None:
            # default to filename if no name was given
            output_wks = filename.split("/")[-1]
        self.output_wks = output_wks
        self.metadata_only = metadata_only
        self.workspace = api.LoadEventNexus(
            Filename=self.filename,
            OutputWorkspace=self.output_wks,
            MetadataOnly=self.metadata_only,
        )
