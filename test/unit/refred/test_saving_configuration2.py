# from dataclasses import dataclass

# from refred.configuration import saving_configuration
# from refred.configuration.saving_configuration import SavingConfiguration


# @dataclass
# class DummyParent:
#     path_config: str

# def test_saving_configuration_good_path(tmp_path):
#     saving_config = SavingConfiguration(
#         parent=DummyParent(path_config="/tmp/original"), # type: ignore[arg-type]
#         filename=tmp_path / "config" / "my_session.xml",
#     )
