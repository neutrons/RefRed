# standard imports
from xml.dom.minidom import parseString

# third party imports
import pytest

# RefRed imports
from RefRed.interfaces.deadtime_settings import DeadTimeSettingsModel


class TestDeadTimeSettingsModel:
    def test_initialization_with_defaults(self):
        model = DeadTimeSettingsModel()
        assert model.apply_deadtime is True
        assert model.paralyzable is True
        assert model.dead_time == 4.2
        assert model.tof_step == 150

    def test_initialization_with_custom_values(self):
        model = DeadTimeSettingsModel(apply_deadtime=False, paralyzable=False, dead_time=5.0, tof_step=200)
        assert model.apply_deadtime is False
        assert model.paralyzable is False
        assert model.dead_time == 5.0
        assert model.tof_step == 200

    def test_to_xml(self):
        expected_xml = (
            '<apply_deadtime>True</apply_deadtime>\n'
            '<paralyzable>True</paralyzable>\n'
            '<dead_time>4.2</dead_time>\n'
            '<tof_step>150</tof_step>'
        )
        model = DeadTimeSettingsModel(apply_deadtime=True, paralyzable=True, dead_time=4.2, tof_step=150)
        xml_output = model.to_xml()
        assert xml_output == expected_xml

    def test_from_xml(self):
        xml_input = (
            '<RefRed>'
            '<spurious>True</spurious>\n'
            '<apply_deadtime>False</apply_deadtime>\n'
            '<paralyzable>False</paralyzable>\n'
            '<dead_time>2.1</dead_time>\n'
            '<tof_step>100</tof_step>\n'
            '<another_spurious>True</another_spurious>\n'
            '</RefRed>'
        )
        dom = parseString(xml_input)
        model = DeadTimeSettingsModel().from_xml(dom.documentElement)
        assert model.apply_deadtime is False
        assert model.paralyzable is False
        assert model.dead_time == 2.1
        assert model.tof_step == 100


if __name__ == "__main__":
    pytest.main()
