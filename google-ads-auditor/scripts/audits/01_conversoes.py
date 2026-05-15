"""
Auditoria de conversões mal configuradas.
Detecta conversões zumbis, contagem errada, atribuição antiga e conversão não primária.
"""
from typing import Dict, List

from ._base import AuditoriaBase


class AuditoriaConversoes(AuditoriaBase):
    """Audita configuração de conversões da conta."""

    def executar(self) -> Dict[str, List[str]]:
        # Roda a query GAQL definida na especificação.
        rows = self.executar_query(self._query_gaql())
        # Prepara listas de saída do relatório.
        criticos, avisos, ok, recomendacoes = [], [], [], []
        # Percorre cada ação de conversão retornada.
        for row in rows:
            conversao = row.conversion_action
            nome = conversao.name
            if str(conversao.category).endswith("PURCHASE") and str(conversao.counting_type).endswith("MANY_PER_CLICK"):
                criticos.append(f"{nome}: venda contando MANY_PER_CLICK; use ONE.")
            if not conversao.primary_for_goal:
                avisos.append(f"{nome}: não está marcada como conversão primária.")
            if str(conversao.attribution_model_settings.attribution_model).endswith("LAST_CLICK"):
                avisos.append(f"{nome}: usa Last Click; avalie Data-Driven.")
            if str(conversao.category).endswith("OTHER"):
                recomendacoes.append(f"{nome}: categoria OTHER; classifique corretamente.")
            if str(conversao.status).endswith("ENABLED"):
                ok.append(f"{nome}: conversão ativa encontrada.")
        recomendacoes.append("Na API v24, valide volume por campanha e evento no painel de conversões.")
        return self.formatar_resultado("🔄 Auditoria de Conversões", criticos, avisos, ok, recomendacoes)

    def _query_gaql(self) -> str:
        return """
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.type,
  conversion_action.category,
  conversion_action.counting_type,
  conversion_action.primary_for_goal,
  conversion_action.attribution_model_settings.attribution_model,
  conversion_action.click_through_lookback_window_days
FROM conversion_action
WHERE conversion_action.status != 'REMOVED'
"""
