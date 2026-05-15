"""
Auditoria de estrutura de campanhas.
Detecta mistura de redes, estratégia inadequada e ausência de metas em automação.
"""
from typing import Dict, List

from ._base import AuditoriaBase


class AuditoriaEstrutura(AuditoriaBase):
    """Audita arquitetura e estratégia das campanhas ativas."""

    def executar(self) -> Dict[str, List[str]]:
        rows = self.executar_query(self._query_gaql())
        criticos, avisos, ok, recomendacoes = [], [], [], []
        for row in rows:
            campanha = row.campaign
            budget = row.campaign_budget
            nome = campanha.name
            canal = str(campanha.advertising_channel_type)
            estrategia = str(campanha.bidding_strategy_type)
            if canal.endswith("SEARCH") and estrategia.endswith("MAXIMIZE_CLICKS"):
                criticos.append(f"{nome}: Search usando Maximize Clicks; revisar para conversões ou CPA.")
            if canal.endswith("SEARCH") and campanha.network_settings.target_content_network:
                criticos.append(f"{nome}: Search com Display ativado na mesma campanha.")
            if campanha.network_settings.target_search_network:
                avisos.append(f"{nome}: Search Partners ativado; monitore diluição de performance.")
            if "MAXIMIZE" in estrategia and not campanha.target_cpa.target_cpa_micros and not campanha.target_roas.target_roas:
                avisos.append(f"{nome}: estratégia automática sem CPA ou ROAS alvo definido.")
            if budget.amount_micros > 0:
                ok.append(f"{nome}: orçamento configurado.")
        recomendacoes.append("Separar Search e Display para leitura limpa de performance.")
        return self.formatar_resultado("🏗️ Auditoria de Estrutura", criticos, avisos, ok, recomendacoes)

    def _query_gaql(self) -> str:
        return """
SELECT
  campaign.id,
  campaign.name,
  campaign.advertising_channel_type,
  campaign.advertising_channel_sub_type,
  campaign.bidding_strategy_type,
  campaign.network_settings.target_google_search,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign_budget.amount_micros,
  campaign.target_cpa.target_cpa_micros,
  campaign.target_roas.target_roas
FROM campaign
WHERE campaign.status = 'ENABLED'
"""
