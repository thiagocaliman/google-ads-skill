# Erros comuns Google Ads API

| Erro | Causa | Solução |
|------|-------|---------|
| `INVALID_DEVELOPER_TOKEN` | Token errado ou não aprovado | Verificar status no MCC → API Center |
| `USER_PERMISSION_DENIED` | Usuário OAuth sem acesso à conta | Adicionar email do OAuth como admin na conta |
| `CUSTOMER_NOT_ENABLED` | Conta suspensa ou cancelada | Reativar conta no painel Google Ads |
| `AUTHENTICATION_ERROR` | Refresh token inválido | Gerar novo refresh token |
| `RESOURCE_EXHAUSTED` | Rate limit atingido | Aguardar 60s e tentar novamente |
| `INVALID_CUSTOMER_ID` | Customer ID com formato errado | Usar 10 dígitos sem hífens |
| `LOGIN_CUSTOMER_ID_PARAMETER_MISSING` | MCC não informado | Preencher `GOOGLE_ADS_LOGIN_CUSTOMER_ID` |
| `QUERY_ERROR` | Campo GAQL inválido | Conferir `references/gaql_cheatsheet.md` |
| `FIELD_ERROR` | Campo incompatível com recurso | Remover campo ou trocar recurso |
| `DATE_RANGE_TOO_NARROW` | Janela de data inválida | Usar `LAST_30_DAYS` |
| `PERMISSION_DENIED` | API sem permissão | Conferir usuário e MCC |
| `OAUTH_TOKEN_REVOKED` | Token revogado pelo usuário | Rodar OAuth novamente |
| `DEVELOPER_TOKEN_NOT_APPROVED` | Token ainda pendente | Aguardar aprovação |
| `CUSTOMER_NOT_FOUND` | Conta não está no MCC | Vincular conta cliente ao MCC |
| `INTERNAL_ERROR` | Erro temporário da API | Tentar novamente depois |
