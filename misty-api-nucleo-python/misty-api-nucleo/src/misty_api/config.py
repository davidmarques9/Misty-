from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    ip: str = "127.0.0.1"
    mode: str = "simulated"
    timeout: float = 5.0

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        mode = os.getenv("MISTY_MODE", "simulated").strip().lower()
        if mode not in {"simulated", "real"}:
            raise ValueError("MISTY_MODE deve ser 'simulated' ou 'real'.")

        ip = os.getenv("MISTY_IP", "127.0.0.1").strip()
        try:
            timeout = float(os.getenv("MISTY_TIMEOUT", "5"))
        except ValueError as exc:
            raise ValueError("MISTY_TIMEOUT deve ser um número.") from exc
        if timeout <= 0:
            raise ValueError("MISTY_TIMEOUT deve ser maior que zero.")
        if mode == "real" and (not ip or ip == "127.0.0.1"):
            raise ValueError("Configure MISTY_IP com o IP real do robô.")
        return cls(ip=ip, mode=mode, timeout=timeout)
