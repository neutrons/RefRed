import os
from RefRed.export.ascii_loader import AsciiLoader


class ReducedAsciiLoader(object):
    parent = None
    ascii_file_name = ''
    short_ascii_file_name = ''

    # used when data comes from ascii file
    col1 = []
    col2 = []
    col3 = []
    col4 = []

    # used when data comes from Live Reduced Set
    big_table_data = []
    isEnabled = True
    is_live_reduction = False

    def __init__(self, parent=None, ascii_file_name='', is_live_reduction=False):
        self.parent = parent
        self.is_live_reduction = is_live_reduction
        if is_live_reduction:
            self.ascii_file_name = 'LAST REDUCED SET'
            self.short_ascii_file_name = 'LAST REDUCED SET'
            self.big_table_data = self.parent.big_table_data
        else:
            self.ascii_file_name = ascii_file_name
            self.short_ascii_file_name = self.get_short_ascii_filename(ascii_file_name)
            self.retrieve_ascii_data()

    def get_short_ascii_filename(self, fullFilename):
        return os.path.basename(fullFilename)

    def retrieve_ascii_data(self):
        filename = self.ascii_file_name
        nbr_col = 3
        _asciiData = AsciiLoader(filename=filename, nbr_col=nbr_col)

        [self.col1, self.col2, self.col3, self.col4] = _asciiData.data()
