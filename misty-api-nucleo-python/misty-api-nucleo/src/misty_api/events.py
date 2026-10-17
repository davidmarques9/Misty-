from __future__ import annotations

import json
import logging
from typing import Callable, Any

import websocket

logger = logging.getLogger("misty_api.websocket")


class MistyEventClient:
    """Cliente WebSocket basico para eventos do Misty II.

    O protocolo de inscricao deve ser confirmado com o catalogo e firmware
    do robô. Este exemplo deixa o nome do evento configuravel.
    """

    def __init__(self, ip: str, timeout: float = 5.0):
        self.url = f"ws://{ip}/pubsub"
        self.timeout = timeout
        self.socket = None

    def listen(
        self,
        event_type: str,
        event_name: str,
        on_event: Callable[[dict[str, Any]], None],
        max_messages: int | None = 10,
    ) -> None:
        count = 0
        try:
            self.socket = websocket.create_connection(self.url, timeout=self.timeout)
            subscription = {
                "Operation": "subscribe",
                "Type": event_type,
                "DebounceMs": 250,
                "EventName": event_name,
                "ReturnProperty": None,
            }
            self.socket.send(json.dumps(subscription))
            logger.info("Inscricao solicitada: %s (%s)", event_name, event_type)

            while max_messages is None or count < max_messages:
                raw = self.socket.recv()
                message = json.loads(raw)
                on_event(message)
                count += 1
        except (websocket.WebSocketException, OSError, json.JSONDecodeError) as exc:
            logger.exception("Erro ao receber eventos WebSocket")
            raise RuntimeError(f"Falha no WebSocket: {exc}") from exc
        finally:
            if self.socket is not None:
                try:
                    self.socket.send(json.dumps({
                        "Operation": "unsubscribe",
                        "EventName": event_name,
                    }))
                except Exception:
                    pass
                self.socket.close()
                self.socket = None
