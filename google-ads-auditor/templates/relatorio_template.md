# AI PRO REVOLUTION | Auditoria Google Ads

**Conta auditada:** {{ customer_id }}
**Data:** {{ data_geracao }}

## Resumo executivo

- Críticos: {{ resumo.criticos }}
- Avisos: {{ resumo.avisos }}
- OK: {{ resumo.ok }}

{% for auditoria in resultados %}
## {{ auditoria.titulo }}

### Críticos
{% for item in auditoria.criticos %}- {{ item }}
{% else %}- Nenhum crítico encontrado.
{% endfor %}

### Avisos
{% for item in auditoria.avisos %}- {{ item }}
{% else %}- Nenhum aviso encontrado.
{% endfor %}

### OK
{% for item in auditoria.ok %}- {{ item }}
{% else %}- Nenhum item OK registrado.
{% endfor %}

### Recomendações
{% for item in auditoria.recomendacoes %}- {{ item }}
{% else %}- Nenhuma recomendação adicional.
{% endfor %}

{% endfor %}

## Galeria de criativos analisados

{% for criativo in analises_criativos %}
### {{ criativo.arquivo }}

- Copy principal: {{ criativo.copy_principal }}
- CTA identificado: {{ criativo.cta_identificado }}
- Legibilidade: {{ criativo.legibilidade }}/10
- Força visual: {{ criativo.forca_visual }}/10
- Problemas: {{ criativo.problemas | join("; ") }}
- Sugestões: {{ criativo.sugestoes_melhoria | join("; ") }}
{% else %}
Nenhum criativo visual foi analisado nesta auditoria.
{% endfor %}

## Recomendações priorizadas

1. Corrigir todos os itens críticos antes de aumentar orçamento.
2. Revisar tracking e conversões primárias antes de julgar performance.
3. Validar criativos e mensagens com base nos dados de conversão.

AI PRO Revolution → aiprorevolution.com.br
