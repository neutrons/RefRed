import pytest
from mantid.simpleapi import mtd

from refred.calculations.load_nexus import LoadNexus


class TestLoadNexus(object):
    def test_load_nexus(self, data_server):
        wksp_name = "REF_L_188300"
        load_obj = LoadNexus(
            filename=data_server.path_to("REF_L_188300.nxs.h5"),
            output_wks=wksp_name,
            metadata_only=False,
        )
        assert load_obj.workspace
        # check that the workspace exists in mantid's ADS
        assert mtd.doesExist(wksp_name)
        # check the workspace name matches
        assert load_obj.workspace.name() == load_obj.output_wks == wksp_name
        # check that all the data was loaded
        assert load_obj.workspace.getNumberEvents() == 18203

    def test_load_nexus_metadata_only(self, data_server):
        load_obj = LoadNexus(filename=data_server.path_to("REF_L_188230.nxs.h5"), metadata_only=True)
        assert load_obj.workspace
        # check that the workspace exists in mantid's ADS
        assert mtd.doesExist(load_obj.workspace.name())
        # check the workspace name matches when no output name is specified
        assert load_obj.workspace.name() == load_obj.output_wks == "REF_L_188230.nxs.h5"
        # check that no events were loaded with metadata only
        assert load_obj.workspace.getNumberEvents() == 0


if __name__ == "__main__":
    pytest.main([__file__])
