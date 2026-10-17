# Misty API — Núcleo (Python)

Camada inicial de comunicação HTTP/WebSocket para Misty II. Inclui modo simulado
para desenvolvimento sem o robô. **Ainda é um protótipo**: valide endpoints e
payloads na documentação oficial e no firmware do robô antes de usar hardware.

## Requisitos
- Python 3.10+
- Git
- Acesso ao Misty II somente para testes reais posteriores

## Instalação

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -e ".[dev]"
cp .env.example .env
```

No Windows, copie `.env.example` para `.env` manualmente se `cp` não estiver disponível.

## Executar no modo simulado

O padrão é `MISTY_MODE=simulated`, portanto nada será enviado a um robô.

```bash
python examples/quickstart.py
pytest -q
```

## Quando tiverem acesso ao robô

1. Confirmem que o computador e o robô estão na mesma rede local.
2. Configurem `MISTY_IP` no `.env` com o IP real.
3. Alterem `MISTY_MODE=real`.
4. Comecem com consultas GET documentadas; só depois testem comandos POST não perigosos.
5. Confirmem cada endpoint e seus parâmetros na API Reference oficial. O método `stop_misty` é um ponto de partida e o endpoint de parada deve ser validado no firmware/API de vocês antes do teste físico.
6. Não exponham a API do Misty à internet: a documentação informa que a API HTTP não exige credenciais.

## Interface inicial para as outras duplas

```python
from misty_api import MistyClient, Settings

settings = Settings.from_env()
with MistyClient(settings.ip, settings.mode, settings.timeout) as misty:
    info = misty.get("websockets")
    # A equipe especializada implementa chamadas para endpoints confirmados.
```

Contrato de uso:
- `get(endpoint)` faz GET em `/api/{endpoint}`.
- `post(endpoint, payload)` faz POST em `/api/{endpoint}`.
- Falhas HTTP/rede são convertidas em `MistyAPIError`.
- `MistyEventClient` oferece um ponto inicial para receber eventos WebSocket.
- O modo simulado é para testes locais; não valida o comportamento físico do robô.

## Divisão sugerida
- David: configuração, WebSocket, testes de conectividade e integração.
- Gabriel: cliente HTTP, tratamento de respostas/erros, logging e documentação.
- Ambos: revisão de segurança, integração e validação com o robô.

## Fontes
- https://docs.mistyrobotics.com/misty-ii/web-api/overview
- https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/
- https://docs.mistyrobotics.com/misty-ii/web-api/tutorials/
