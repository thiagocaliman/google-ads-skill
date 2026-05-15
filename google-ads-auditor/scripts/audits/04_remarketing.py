"""
Auditoria de audiências e remarketing.
Detecta listas pequenas, janelas curtas e campanhas sem audiências associadas.
"""
from typing import Dict, List, Set

from ._base import AuditoriaBase


class AuditoriaRemarketing(AuditoriaBase):
    """Audita listas de usuário e uso em campanhas."""

    def executar(self) -> Dict[str, List[str]]:
        listas = self.executar_query(self._query_listas())
        associacoes = self.executar_query(self._query_associacoes())
        criticos, avisos, ok, recomendacoes = [], [], [], []
        campanhas_com_lista: Set[str] = set()
        for row in associacoes:
            campanhas_com_lista.add(row.campaign.name)
        if not campanhas_com_lista:
            criticos.append("Nenhuma campanha ENABLED possui audiência de remarketing associada.")
        for row in listas:
            lista = row.user_list
            if lista.size_for_display < 1000:
                avisos.append(f"{lista.name}: tamanho Display abaixo de 1000 usuários.")
            if lista.membership_life_span < 30:
                avisos.append(f"{lista.name}: janela menor que 30 dias.")
            if lista.size_for_search >= 1000 or lista.size_for_display >= 1000:
                ok.append(f"{lista.name}: lista com tamanho utilizável.")
        recomendacoes.append("Criar listas de visitantes, leads e compradores para remarketing.")
        return self.formatar_resultado("👥 Auditoria de Remarketing", criticos, avisos, ok, recomendacoes)

    def _query_listas(self) -> str:
        return """
SELECT
  user_list.id,
  user_list.name,
  user_list.size_for_display,
  user_list.size_for_search,
  user_list.membership_status,
  user_list.membership_life_span
FROM user_list
WHERE user_list.membership_status = 'OPEN'
"""

    def _query_associacoes(self) -> str:
        return """
SELECT
  campaign.id,
  campaign.name,
  campaign.advertising_channel_type,
  ad_group_criterion.user_list.user_list
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'USER_LIST'
  AND campaign.status = 'ENABLED'
"""
