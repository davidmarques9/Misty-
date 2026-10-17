import pytest
import requests
from misty_api.client import MistyClient, MistyAPIError


def test_simulated_get_catalog():
    client = MistyClient("127.0.0.1", mode="simulated")
    result = client.get_websocket_catalog()
    assert "result" in result
    assert result["result"][0]["class"] == "TimeOfFlight"


def test_simulated_post_does_not_send():
    client = MistyClient("127.0.0.1", mode="simulated")
    result = client.post("example/endpoint", {"hello": "world"})
    assert result["simulated"] is True
    assert result["payload"] == {"hello": "world"}


def test_real_get_translates_request_error(monkeypatch):
    client = MistyClient("192.0.2.1", mode="real", timeout=0.1)

    def fail(*args, **kwargs):
        raise requests.Timeout("timed out")

    monkeypatch.setattr(client.session, "get", fail)
    with pytest.raises(MistyAPIError, match="Falha na requisicao GET"):
        client.get("websockets")
