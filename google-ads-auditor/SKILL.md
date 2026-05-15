---
name: google-ads-auditor
description: Audita contas Google Ads via API oficial detectando falhas de setup (conversões, tracking, estrutura, remarketing, keywords, ads, budget). Baixa criativos para análise visual com IA. Gera relatórios em Markdown e HTML brutalist. Use quando o usuário pedir auditoria de Google Ads, diagnóstico de campanha, análise de conta Google Ads, revisão de setup, verificação de tracking, ou auditoria de tráfego pago Google.
version: 1.0.0
author: Thiago Caliman — AI PRO Revolution
---

# Google Ads Auditor

## Quando ativar

Use esta skill quando o usuário pedir:

- Auditoria de conta Google Ads.
- Diagnóstico de campanha Google Ads.
- Revisão de setup, conversões, tracking ou orçamento.
- Verificação de remarketing, keywords, anúncios ou criativos.
- Relatório educacional para gestor de tráfego iniciante ou intermediário.

## Workflow de 4 passos

1. Validar credenciais no `.env` usando `scripts/config.py`.
2. Rodar as 7 auditorias em `scripts/audits/`.
3. Baixar criativos e analisar imagens com IA quando houver anúncios visuais.
4. Gerar relatórios Markdown e HTML brutalist com branding AI PRO Revolution.

## Pré-requisitos

- Configurar Developer Token seguindo `references/setup_developer_token.md`.
- Configurar OAuth e Refresh Token seguindo `references/setup_oauth.md`.
- Copiar `templates/.env.template` para `.env` e preencher todas as variáveis.

## Como usar

```bash
pip install -r requirements.txt
python scripts/auditor.py --customer-id=123-456-7890
```

Comunidade AI PRO Revolution → aiprorevolution.com.br
