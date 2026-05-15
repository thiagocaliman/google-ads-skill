"""
Auditoria de tracking quebrado.
Detecta campanhas com cliques sem conversões e desalinhamento entre conversões primárias e todas.
"""
from collections import defaultdict
from typing import Dict, List

from ._base import AuditoriaBase


class AuditoriaTracking(AuditoriaBase):
    """Audita sinais de rastreamento quebrado."""

    def executar(self) -> Dict[str, List[str]]:
        rows = self.executar_query(self._query_gaql())
        criticos, avisos, ok, recomendacoes = [], [], [], []
        dias_sem_conversao = defaultdict(int)
        for row in rows:
            campanha = row.campaign
            metricas = row.metrics
            if metricas.clicks > 100 and metricas.conversions == 0:
                dias_sem_conversao[campanha.name] += 1
            if metricas.conversions > 0 and metricas.all_conversions > metricas.conversions * 3:
                criticos.append(f"{campanha.name}: all_conversions está mais de 3x acima de conversions.")
            if metricas.clicks > 0 and metricas.conversions > 0:
                ok.append(f"{campanha.name}: tracking registrou conversões.")
        for nome, dias in dias_sem_conversao.items():
            if dias >= 7:
                criticos.append(f"{nome}: mais de 7 dias com 100+ cliques e zero conversões.")
        if criticos:
            recomendacoes.append("Rodar Tag Assistant no site e validar eventos primários.")
        return self.formatar_resultado("📡 Auditoria de Tracking", criticos, avisos, ok, recomendacoes)

    def _query_gaql(self) -> str:
        return """
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.clicks,
  metrics.conversions,
  metrics.all_conversions,
  metrics.view_through_conversions,
  segments.date
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
"""
