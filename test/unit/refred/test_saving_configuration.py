from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pytest

from refred.configuration import saving_configuration


### Helpers to fake the MainGui
@dataclass
class DummyParent:
    path_config: str
    config_saved: bool = False


def fake_extension_factory(expected_input: Path, sanitized_output: str) -> Callable[[str], str]:
    def _fake_extension(path: str) -> str:
        assert path == str(expected_input)
        return sanitized_output

    return _fake_extension


def fake_status_handler_factory(call_collector: list[tuple[str, bool]]):
    class _FakeStatusMessageHandler:
        def __init__(self, parent: DummyParent, message: str, is_threaded: bool):
            call_collector.append((message, is_threaded))

    return _FakeStatusMessageHandler


def fake_export_config_factory() -> type:
    class _FakeExportXMLConfig:
        def __init__(self, parent: DummyParent):
            self.parent: DummyParent = parent

        def save(self, filename: str):
            path = Path(filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            _ = path.write_text("<Reduction />", encoding="utf-8")

    return _FakeExportXMLConfig


def fake_gui_utility_factory(sanitized_path: str) -> type:
    class _FakeGuiUtility:
        def __init__(self, parent: DummyParent):
            self.parent: DummyParent = parent

        def new_config_file_loaded(self, config_file_name: str):
            assert config_file_name == sanitized_path
            self.parent.config_saved = True

        def gui_not_modified(self):
            pass

    return _FakeGuiUtility


### Tests


def test_saving_configuration_good_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    parent = DummyParent(path_config=str(tmp_path))
    provided_path = tmp_path / "test_config"
    sanitized_path = f"{provided_path}.xml"

    monkeypatch.setattr(
        saving_configuration,
        "makeSureFileHasExtension",
        fake_extension_factory(provided_path, sanitized_path),
    )

    status_messages: list[tuple[str, bool]] = []
    monkeypatch.setattr(
        saving_configuration,
        "StatusMessageHandler",
        fake_status_handler_factory(status_messages),
    )

    monkeypatch.setattr(
        saving_configuration,
        "ExportXMLConfig",
        fake_export_config_factory(),
    )

    monkeypatch.setattr(
        saving_configuration,
        "GuiUtility",
        fake_gui_utility_factory(sanitized_path),
    )

    saver = saving_configuration.SavingConfiguration(parent=parent, filename=str(provided_path))  # type: ignore[arg-type]
    saver.run()

    saved_file = Path(sanitized_path)
    assert saved_file.exists()
    assert parent.path_config == str(provided_path.parent)
    assert parent.config_saved is True
    assert status_messages == [("Saving config ...", False), ("Done!", True)]


def test_saving_configuration_permission_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    parent = DummyParent(path_config=str(tmp_path))
    provided_path = tmp_path / "forbidden" / "config"
    sanitized_path = f"{provided_path}.xml"

    monkeypatch.setattr(
        saving_configuration,
        "makeSureFileHasExtension",
        fake_extension_factory(provided_path, sanitized_path),
    )

    status_messages: list[tuple[str, bool]] = []
    monkeypatch.setattr(
        saving_configuration,
        "StatusMessageHandler",
        fake_status_handler_factory(status_messages),
    )

    class _PermissionErrorExportXMLConfig:
        def __init__(self, parent: DummyParent):
            self.parent: DummyParent = parent

        def save(self, filename: str):
            raise PermissionError("No permission to write file.")

    monkeypatch.setattr(
        saving_configuration,
        "ExportXMLConfig",
        _PermissionErrorExportXMLConfig,
    )

    monkeypatch.setattr(
        saving_configuration,
        "GuiUtility",
        fake_gui_utility_factory(sanitized_path),
    )

    saver = saving_configuration.SavingConfiguration(parent=parent, filename=str(provided_path))  # type: ignore[arg-type]
    saver.run()

    assert parent.path_config == str(provided_path.parent)
    assert parent.config_saved is False
    assert status_messages == [
        ("Saving config ...", False),
        ("Error: No permission to write file.", True),
    ]
