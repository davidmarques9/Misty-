from misty_api import MistyClient, Settings
from misty_api.logging_setup import configure_logging


def main():
    configure_logging()
    settings = Settings.from_env()

    with MistyClient(settings.ip, settings.mode, settings.timeout) as misty:
        print("Modo:", settings.mode)
        print("Catalogo de eventos:", misty.get_websocket_catalog())
        # As equipes podem usar misty.get(...) e misty.post(...)
        # depois de confirmar o endpoint e o payload na documentacao oficial.


if __name__ == "__main__":
    main()
