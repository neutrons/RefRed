# -*- coding: utf-8 -*-
"""
REF_L specific values.
"""

from os.path import expanduser

config_file = ""

NAME = "REF_L"
BEAMLINE = "4B"

# for the search of files by number
data_base = "/SNS/REF_L"
BASE_SEARCH = "*/data/REF_L_%s_"
OLD_BASE_SEARCH = "*/*/%s/NeXus/REF_L_%s*"
LIVE_DATA = "/SNS/REF_L/shared/LiveData/meta_data.xml"
EXTENSION_SCRIPTS = "/SNS/REF_L/shared/quicknxs_scripts"

local_data_base = expanduser("~/")
