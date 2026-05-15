"""
Auditoria de anúncios.
Detecta RSA fraco, RSA médio e baixa variedade de anúncios ativos.
"""
from collections import defaultdict
from typing import Dict, List

from ._base import AuditoriaBase


class AuditoriaAds(AuditoriaBase):
    """Audita anúncios ativos dos últimos 30 dias."""

    def executar(self) -> Dict[str, List[str]]:
        rows = self.executar_query(self._query_gaql())
        criticos, avisos, ok, recomendacoes = [], [], [], []
        ads_por_tipo = defaultdict(int)
        for row in rows:
            anuncio = row.ad_group_ad
            ad_id = anuncio.ad.id
            forca = str(anuncio.ad_strength)
            tipo = str(anuncio.ad.type)
            ads_por_tipo[tipo] += 1
            if forca.endswith("POOR"):
                criticos.append(f"Ad {ad_id}: RSA com força POOR.")
            if forca.endswith("AVERAGE"):
                avisos.append(f"Ad {ad_id}: RSA com força AVERAGE.")
            if row.metrics.impressions > 0:
                ok.append(f"Ad {ad_id}: ativo com impressões.")
        if sum(ads_por_tipo.values()) < 3:
            avisos.append("Conta/grupo analisado tem menos de 3 ads ativos no recorte retornado.")
        recomendacoes.append("Adicionar pelo menos 1 ad responsivo + 1 ad de chamada.")
        return self.formatar_resultado("📣 Auditoria de Anúncios", criticos, avisos, ok, recomendacoes)

    def _query_gaql(self) -> str:
        return """
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.type,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad_strength,
  ad_group_ad.status,
  metrics.impressions,
  metrics.clicks,
  metrics.conversions
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
"""
