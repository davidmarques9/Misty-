from __future__ import annotations

from .client import MistyClient


def stop_misty(client: MistyClient):
    """Solicita parada do movimento. Endpoint conforme API oficial: /api/drive/stop."""
    return client.post("drive/stop", {})
