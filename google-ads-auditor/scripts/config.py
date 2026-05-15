"""
Carrega e valida credenciais da Google Ads API.
Todas as mensagens são em português brasileiro para orientar o Karl.
"""
import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


VARIAVEIS_OBRIGATORIAS = [
    "GOOGLE_ADS_DEVELOPER_TOKEN",
    "GOOGLE_ADS_CLIENT_ID",
    "GOOGLE_ADS_CLIENT_SECRET",
    "GOOGLE_ADS_REFRESH_TOKEN",
    "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
    "GOOGLE_ADS_CUSTOMER_ID",
]


class ConfigError(Exception):
    """Erro de configuração amigável para credenciais ausentes."""


def _raiz_projeto() -> Path:
    # Resolve a pasta raiz subindo de scripts/ para google-ads-auditor/.
    return Path(__file__).resolve().parents[1]


def carregar_credenciais() -> Dict[str, str]:
    # Monta o caminho absoluto do arquivo .env na raiz do projeto.
    caminho_env = _raiz_projeto() / ".env"
    # Carrega as variáveis do .env para o ambiente atual.
    load_dotenv(caminho_env)
    # Cria uma lista para acumular variáveis faltantes.
    faltando = []
    # Percorre todas as variáveis obrigatórias definidas no topo.
    for nome in VARIAVEIS_OBRIGATORIAS:
        # Lê a variável e remove espaços acidentais.
        valor = os.getenv(nome, "").strip()
        # Se estiver vazia, registra a variável para mensagem final.
        if not valor:
            faltando.append(nome)
    # Se houver falhas, interrompe com instrução clara.
    if faltando:
        linhas = ", ".join(faltando)
        raise ConfigError(
            f"Credenciais faltando no .env: {linhas}. "
            "Copie templates/.env.template e siga references/setup_developer_token.md."
        )
    # Retorna o dict no formato aceito por GoogleAdsClient.load_from_dict().
    return {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "").strip(),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID", "").strip(),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET", "").strip(),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "").strip(),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "").strip(),
        "use_proto_plus": True,
    }


def carregar_customer_id_padrao() -> str:
    # Carrega o customer_id do .env quando o usuário não passa via CLI.
    return os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "").strip()
