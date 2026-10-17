from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

import requests

logger = logging.getLogger("misty_api")


class MistyAPIError(RuntimeError):
    """Erro de comunicacao ou resposta da API do Misty."""


class MistyClient:
    """Cliente pequeno para a API HTTP do Misty II, com modo simulado."""

    def __init__(self, ip: str, mode: str = "simulated", timeout: float = 5.0):
        if mode not in {"simulated", "real"}:
            raise ValueError("mode deve ser 'simulated' ou 'real'.")
        if timeout <= 0:
            raise ValueError("timeout deve ser maior que zero.")
        self.ip = ip
        self.mode = mode
        self.timeout = timeout
        self.base_url = f"http://{ip}/api/"
        self.session = requests.Session()

    def get(self, endpoint: str) -> dict[str, Any] | list[Any] | str:
        """Executa GET em endpoint documentado da API, ou simula a consulta."""
        endpoint = endpoint.lstrip("/")
        if self.mode == "simulated":
            logger.info("[SIMULADO] GET /api/%s", endpoint)
            if endpoint == "websockets":
                return {"result": [
                    {"class": "TimeOfFlight", "nestedProperties": [
                        "SensorPosition", "DistanceInMeters"
                    ]},
                    {"class": "LocomotionCommand", "nestedProperties": []},
                ]}
            return {"simulated": True, "method": "GET", "endpoint": endpoint}

        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            logger.info("GET %s -> HTTP %s", url, response.status_code)
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.RequestException as exc:
            logger.exception("Falha no GET %s", url)
            raise MistyAPIError(f"Falha na requisicao GET: {exc}") from exc

    def post(self, endpoint: str, payload: dict[str, Any] | None = None):
        """Executa POST. No modo simulado, nao envia nada ao robô."""
        endpoint = endpoint.lstrip("/")
        payload = payload or {}
        if self.mode == "simulated":
            logger.info("[SIMULADO] POST /api/%s payload=%s", endpoint, payload)
            return {
                "simulated": True,
                "method": "POST",
                "endpoint": endpoint,
                "payload": payload,
            }

        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            logger.info("POST %s -> HTTP %s", url, response.status_code)
            if not response.content:
                return {}
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.RequestException as exc:
            logger.exception("Falha no POST %s", url)
            raise MistyAPIError(f"Falha na requisicao POST: {exc}") from exc

    def get_websocket_catalog(self):
        """Consulta o catalogo de WebSockets no endpoint oficial do Misty."""
        return self.get("websockets")

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()
