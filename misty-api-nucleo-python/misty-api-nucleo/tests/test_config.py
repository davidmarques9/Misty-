import pytest
from misty_api.config import Settings


def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("MISTY_IP", raising=False)
    monkeypatch.delenv("MISTY_MODE", raising=False)
    monkeypatch.delenv("MISTY_TIMEOUT", raising=False)
    settings = Settings.from_env()
    assert settings.mode == "simulated"
    assert settings.timeout == 5.0


def test_invalid_mode(monkeypatch):
    monkeypatch.setenv("MISTY_MODE", "maybe")
    with pytest.raises(ValueError):
        Settings.from_env()


def test_real_mode_requires_ip(monkeypatch):
    monkeypatch.setenv("MISTY_MODE", "real")
    monkeypatch.setenv("MISTY_IP", "127.0.0.1")
    with pytest.raises(ValueError):
        Settings.from_env()
