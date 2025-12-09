from dataclasses import dataclass

from refred.configuration import saving_configuration


@dataclass
class DummyParent:
    path_config: str


def _patch_status_handler(monkeypatch):
    calls = []

    class _FakeStatusHandler:
        def __init__(self, parent, message, is_threaded):
            calls.append({"parent": parent, "message": message, "is_threaded": is_threaded})

    monkeypatch.setattr(saving_configuration, "StatusMessageHandler", _FakeStatusHandler)
    return calls


def test_run_with_filename_saves_and_updates_gui(monkeypatch, tmp_path):
    parent = DummyParent(path_config="/tmp/original")
    provided_path = tmp_path / "config" / "my_session"
    sanitized_path = f"{provided_path}.xml"

    status_calls = _patch_status_handler(monkeypatch)

    export_calls = {}

    class _FakeExportConfig:
        def __init__(self, parent):
            export_calls["parent"] = parent

        def save(self, filename):
            export_calls["saved_filename"] = filename

    gui_calls = []

    class _FakeGuiUtility:
        def __init__(self, parent):
            export_calls["gui_parent"] = parent

        def new_config_file_loaded(self, config_file_name):
            gui_calls.append(("new", config_file_name))

        def gui_not_modified(self):
            gui_calls.append(("not_modified", None))

    def _fake_extension(path):
        export_calls["extension_arg"] = path
        return sanitized_path

    monkeypatch.setattr(saving_configuration, "ExportXMLConfig", _FakeExportConfig)
    monkeypatch.setattr(saving_configuration, "GuiUtility", _FakeGuiUtility)
    monkeypatch.setattr(saving_configuration, "makeSureFileHasExtension", _fake_extension)

    saver = saving_configuration.SavingConfiguration(parent=parent, filename=str(provided_path))  # type: ignore[arg-type]
    saver.run()

    assert parent.path_config == str(provided_path.parent)
    assert export_calls["extension_arg"] == str(provided_path)
    assert export_calls["saved_filename"] == sanitized_path
    assert gui_calls == [("new", sanitized_path), ("not_modified", None)]
    assert [call["message"] for call in status_calls] == ["Saving config ...", "Done!"]
    assert status_calls[1]["is_threaded"] is True


def test_run_reports_permission_error_without_gui_updates(monkeypatch, tmp_path):
    parent = DummyParent(path_config="/tmp/original")
    provided_path = tmp_path / "config" / "fails"
    sanitized_path = f"{provided_path}.xml"
    error_text = "Cannot write file"

    status_calls = _patch_status_handler(monkeypatch)

    class _FakeExportConfig:
        def __init__(self, parent):
            self.parent = parent

        def save(self, filename):
            raise PermissionError(error_text)

    gui_instantiated = {"value": False}

    class _FakeGuiUtility:
        def __init__(self, parent):
            gui_instantiated["value"] = True

    def _fake_extension(path):
        return sanitized_path

    monkeypatch.setattr(saving_configuration, "ExportXMLConfig", _FakeExportConfig)
    monkeypatch.setattr(saving_configuration, "GuiUtility", _FakeGuiUtility)
    monkeypatch.setattr(saving_configuration, "makeSureFileHasExtension", _fake_extension)

    saver = saving_configuration.SavingConfiguration(parent=parent, filename=str(provided_path))  # type: ignore[arg-type]
    saver.run()

    assert parent.path_config == str(provided_path.parent)
    assert gui_instantiated["value"] is False
    assert [call["message"] for call in status_calls] == [
        "Saving config ...",
        f"Error: {error_text}",
    ]
    assert status_calls[1]["is_threaded"] is True
