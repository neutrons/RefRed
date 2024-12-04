# standard imports
from datetime import datetime
from unittest.mock import MagicMock, patch

# third party imports
import pytest

# RefRed imports
from RefRed.configuration.export_xml_config import ExportXMLConfig


class TestExportXMLConfig:
    @patch("RefRed.configuration.export_xml_config.RefRed")
    @patch("RefRed.configuration.export_xml_config.mantid")
    def test_header_part(self, mantid_mock, refred_mock):
        refred_mock.__version__ = "2.0.0"
        mantid_mock.__version__ = "1.0.0"
        config = ExportXMLConfig(MagicMock())
        config.header_part()
        assert len(config.str_array) == 7
        header = "".join(config.str_array)
        assert datetime.now().strftime("%A, %d. %B %Y %I:%M%p") in header
        assert '<mantid_version>1.0.0</mantid_version>' in header
        assert '<generator>RefRed-2.0.0</generator>' in header

    def test_main_part(self):
        config = ExportXMLConfig(MagicMock())
        config.main_part()
        assert len(config.str_array) == 55


if __name__ == "__main__":
    pytest.main()
