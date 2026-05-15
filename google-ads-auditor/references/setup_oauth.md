# Setup OAuth e Refresh Token

## Passo a passo

1. Acesse Google Cloud Console.
2. Crie um projeto novo para a auditoria Google Ads.
3. Habilite a Google Ads API no projeto.
4. Configure a tela de consentimento OAuth.
5. Crie credenciais OAuth 2.0 do tipo Desktop App.
6. Copie Client ID e Client Secret para o `.env`.
7. Rode:

```bash
python scripts/gerar_refresh_token.py
```

8. Autorize com o usuário que tem acesso à conta Google Ads.
9. Cole o refresh token em `GOOGLE_ADS_REFRESH_TOKEN`.

## Observação importante

O script usa `google-auth-oauthlib`, que vem como dependência transitiva do pacote `google-ads`.

## Erros comuns

- `USER_PERMISSION_DENIED`: o usuário OAuth não tem acesso à conta cliente.
- Tela OAuth em modo teste: adicione seu email como usuário de teste.
- Redirect URI errado: use Desktop App.
