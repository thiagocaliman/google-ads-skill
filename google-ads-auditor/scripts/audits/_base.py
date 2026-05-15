"""
Classe base para auditorias Google Ads.
Centraliza execução GAQL, tratamento de erros e formato de resultado.
"""
from abc import ABC, abstractmethod
from time import sleep
from typing import Any, Dict, List

from google.ads.googleads.errors import GoogleAdsException


class AuditoriaBase(ABC):
    """Base compartilhada por todas as auditorias."""

    def __init__(self, google_ads_client: Any, customer_id: str) -> None:
        # Guarda o client oficial já autenticado.
        self.client = google_ads_client
        # Normaliza o Customer ID removendo hífens.
        self.customer_id = customer_id.replace("-", "")

    @abstractmethod
    def executar(self) -> Dict[str, List[str]]:
        # Cada auditoria filha implementa sua própria lógica.
        raise NotImplementedError

    def executar_query(self, gaql: str) -> List[Any]:
        # Obtém o serviço GoogleAdsService para rodar GAQL.
        servico = self.client.get_service("GoogleAdsService")
        # Tenta duas vezes para cobrir rate limit temporário.
        for tentativa in range(2):
            try:
                # Executa a busca em streaming para suportar contas maiores.
                stream = servico.search_stream(customer_id=self.customer_id, query=gaql)
                # Achata batches em uma lista simples de rows.
                return [row for batch in stream for row in batch.results]
            except GoogleAdsException as erro:
                # Extrai a mensagem principal da API quando disponível.
                mensagem = self._mensagem_google_ads(erro)
                # ⚠️ ERRO COMUM: RESOURCE_EXHAUSTED indica rate limit temporário.
                if "RESOURCE_EXHAUSTED" in mensagem and tentativa == 0:
                    sleep(60)
                    continue
                raise RuntimeError(
                    f"Erro Google Ads API: {mensagem}. Veja references/erros_comuns.md."
                ) from erro
        return []

    def formatar_resultado(
        self,
        titulo: str,
        criticos: List[str],
        avisos: List[str],
        ok: List[str],
        recomendacoes: List[str],
    ) -> Dict[str, List[str]]:
        # Padroniza o retorno usado pelos relatórios.
        return {
            "titulo": titulo,
            "criticos": criticos,
            "avisos": avisos,
            "ok": ok,
            "recomendacoes": recomendacoes,
        }

    def _mensagem_google_ads(self, erro: GoogleAdsException) -> str:
        # Junta códigos e mensagens detalhadas para facilitar diagnóstico.
        partes = []
        # Percorre falhas retornadas pela API.
        for item in erro.failure.errors:
            partes.append(f"{item.error_code}: {item.message}")
        # Retorna fallback caso a resposta venha incompleta.
        return " | ".join(partes) or str(erro)
