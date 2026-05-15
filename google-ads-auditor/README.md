# Google Ads Auditor | AI PRO Revolution

Skill executável para auditar contas Google Ads via API oficial, baixar criativos e gerar relatórios em Markdown e HTML brutalist.

## Passo a passo do Karl

1. Clone ou copie esta pasta `google-ads-auditor/`.
2. Entre na pasta:

```bash
cd google-ads-auditor
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Copie o template de ambiente:

```bash
copy templates\.env.template .env
```

5. Preencha o `.env` com Developer Token, Client ID, Client Secret, Refresh Token e Customer ID.
   Use `GOOGLE_ADS_LOGIN_CUSTOMER_ID` apenas quando houver uma conta administradora MCC gerenciando a conta auditada.
6. Se ainda não tiver Refresh Token, rode:

```bash
python scripts/gerar_refresh_token.py
```

7. Rode a auditoria:

```bash
python scripts/auditor.py --customer-id=123-456-7890
```

8. Abra os arquivos gerados em `relatorios/`.

## Saídas esperadas

- `relatorios/auditoria_1234567890_AAAA-MM-DD.md`
- `relatorios/auditoria_1234567890_AAAA-MM-DD.html`
- `criativos_baixados/*.png`

## Ajuda rápida

- Developer Token: veja `references/setup_developer_token.md`.
- OAuth e Refresh Token: veja `references/setup_oauth.md`.
- Erros comuns: veja `references/erros_comuns.md`.
- Termos técnicos: veja `references/glossario.md`.

AI PRO Revolution → aiprorevolution.com.br
