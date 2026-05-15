"""
Auditoria de orçamento.
Detecta perda por verba, perda por rank e cobertura baixa.
"""
from typing import Dict, List

from ._base import AuditoriaBase


class AuditoriaBudget(AuditoriaBase):
    """Audita limites de orçamento e share de impressão."""

    def executar(self) -> Dict[str, List[str]]:
        rows = self.executar_query(self._query_gaql())
        criticos, avisos, ok, recomendacoes = [], [], [], []
        for row in rows:
            campanha = row.campaign
            metricas = row.metrics
            nome = campanha.name
            if metricas.search_budget_lost_impression_share > 0.20:
                criticos.append(f"{nome}: perde mais de 20% de impressões por orçamento.")
            if metricas.search_rank_lost_impression_share > 0.30:
                avisos.append(f"{nome}: perde mais de 30% por rank/lance.")
            if metricas.search_impression_share < 0.40:
                avisos.append(f"{nome}: cobertura abaixo de 40%.")
            if metricas.cost_micros > 0:
                ok.append(f"{nome}: possui gasto no período.")
        recomendacoes.append("Só aumentar orçamento depois de corrigir tracking e estrutura.")
        return self.formatar_resultado("💰 Auditoria de Orçamento", criticos, avisos, ok, recomendacoes)

    def _query_gaql(self) -> str:
        return """
SELECT
  campaign.id,
  campaign.name,
  campaign_budget.amount_micros,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_impression_share,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
"""
