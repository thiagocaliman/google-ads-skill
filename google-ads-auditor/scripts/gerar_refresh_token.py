"""
Gera refresh_token OAuth para Google Ads API.
Abre o navegador, executa o fluxo OAuth e imprime o token para colar no .env.
"""
from google_auth_oauthlib.flow import InstalledAppFlow


ESCOPO_GOOGLE_ADS = "https://www.googleapis.com/auth/adwords"


def main() -> None:
    # Solicita Client ID criado no Google Cloud Console.
    client_id = input("Cole o GOOGLE_ADS_CLIENT_ID: ").strip()
    # Solicita Client Secret criado no Google Cloud Console.
    client_secret = input("Cole o GOOGLE_ADS_CLIENT_SECRET: ").strip()
    # Monta a configuração OAuth no formato esperado pela biblioteca do Google.
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    # Cria o fluxo OAuth com escopo da Google Ads API.
    flow = InstalledAppFlow.from_client_config(client_config, scopes=[ESCOPO_GOOGLE_ADS])
    # Abre navegador local e força consentimento para retornar refresh_token.
    credenciais = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    # Mostra o refresh token para copiar no .env.
    print("\nGOOGLE_ADS_REFRESH_TOKEN=")
    print(credenciais.refresh_token)
    # Fecha com orientação direta.
    print("\nCole esse valor no arquivo .env.")


if __name__ == "__main__":
    main()
