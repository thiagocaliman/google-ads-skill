# Setup do Developer Token Google Ads

## Passo a passo

1. Acesse https://ads.google.com usando a conta MCC.
2. Clique no ícone de chave inglesa no topo direito. Vai abrir um menu. Procure por "API Center" na coluna "Setup".
3. Abra o API Center e solicite um Developer Token.
4. Escolha Basic Access para começar.
5. Explique que você vai auditar contas próprias ou de clientes com permissão.
6. Aguarde aprovação. Normalmente leva 1 a 3 dias úteis.
7. Copie o token aprovado para `GOOGLE_ADS_DEVELOPER_TOKEN` no `.env`.

## Screenshots descritos

- Tela inicial: ícone de chave inglesa no topo direito.
- Menu aberto: coluna "Setup" com opção "API Center".
- API Center: campo "Developer token" e status do acesso.

## Erros comuns

- Token negado por falta de histórico: rode campanhas reais antes de solicitar novamente.
- Conta sem MCC: crie uma conta administradora Google Ads.
- Token pendente: aguarde aprovação antes de testar a API.
- Token copiado com espaço: remova espaços no começo e fim.
