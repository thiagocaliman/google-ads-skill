"""
Auditoria de palavras-chave.
Detecta qualidade ruim, broad amplo demais e keywords zumbis.
"""
from typing import Dict, List

from ._base import AuditoriaBase


class AuditoriaKeywords(AuditoriaBase):
    """Audita keywords ativas nos últimos 30 dias."""

    def executar(self) -> Dict[str, List[str]]:
        rows = self.executar_query(self._query_gaql())
        criticos, avisos, ok, recomendacoes = [], [], [], []
        keywords_vistas = set()
        for row in rows:
            criterio = row.ad_group_criterion
            keyword = criterio.keyword
            metricas = row.metrics
            texto = keyword.text
            chave = texto.strip().lower()
            if chave in keywords_vistas:
                continue
            keywords_vistas.add(chave)
            if criterio.quality_info.quality_score < 4 and metricas.cost_micros > 50_000_000:
                criticos.append(f"{texto}: Quality Score < 4 e gasto acima de R$50.")
            if str(keyword.match_type).endswith("BROAD"):
                avisos.append(f"{texto}: broad match exige acompanhamento de termos de pesquisa.")
            if metricas.impressions == 0:
                avisos.append(f"{texto}: zero impressões em 30 dias.")
            if metricas.clicks > 0:
                ok.append(f"{texto}: recebeu cliques no período.")
        recomendacoes.append("Revisar search terms report semanalmente.")
        return self.formatar_resultado("🔑 Auditoria de Keywords", criticos, avisos, ok, recomendacoes)

    def _query_gaql(self) -> str:
        return """
SELECT
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.status,
  ad_group_criterion.quality_info.quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM keyword_view
WHERE ad_group_criterion.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
"""
