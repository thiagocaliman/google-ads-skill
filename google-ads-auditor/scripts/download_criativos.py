"""
Baixa criativos visuais de anúncios Google Ads.
Salva imagens em criativos_baixados/ e links de vídeo em videos.txt.
"""
from pathlib import Path
from time import sleep
from typing import Any, List

import requests


QUERY_CRIATIVOS = """
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.image_ad.image_url,
  ad_group_ad.ad.responsive_display_ad.marketing_images
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED'
"""


def baixar_imagens_ads(client: Any, customer_id: str, output_dir: str) -> List[str]:
    # Cria o diretório de saída caso ele ainda não exista.
    pasta = Path(output_dir)
    pasta.mkdir(parents=True, exist_ok=True)
    # Prepara lista de imagens baixadas.
    imagens = []
    # Obtém o serviço oficial de busca.
    servico = client.get_service("GoogleAdsService")
    # Executa a query para buscar URLs de criativos.
    stream = servico.search_stream(customer_id=customer_id.replace("-", ""), query=QUERY_CRIATIVOS)
    # Percorre batches e linhas.
    for batch in stream:
        for row in batch.results:
            # Extrai o ID do anúncio para nomear o arquivo.
            ad_id = str(row.ad_group_ad.ad.id)
            # Baixa image_ad quando a URL está disponível.
            url = getattr(row.ad_group_ad.ad.image_ad, "image_url", "")
            if url:
                caminho = _baixar_url(url, pasta / f"{ad_id}.png")
                if caminho:
                    imagens.append(str(caminho))
            # Registra vídeos ou assets sem URL direta quando necessário.
            _registrar_video_se_precisar(pasta, ad_id, url)
    return imagens


def _baixar_url(url: str, destino: Path) -> Path | None:
    # Tenta três vezes para contornar timeout temporário.
    for tentativa in range(3):
        try:
            # Faz o download com timeout explícito.
            resposta = requests.get(url, timeout=20)
            # Se for 404, não adianta retentar.
            if resposta.status_code == 404:
                return None
            # Levanta erro HTTP para status inválido.
            resposta.raise_for_status()
            # Confere se o conteúdo parece imagem.
            if "image" not in resposta.headers.get("content-type", ""):
                return None
            # Salva bytes no arquivo final.
            destino.write_bytes(resposta.content)
            return destino
        except requests.exceptions.Timeout:
            # Aplica backoff exponencial simples.
            sleep(2**tentativa)
    return None


def _registrar_video_se_precisar(pasta: Path, ad_id: str, url: str) -> None:
    # Se a URL aparenta ser YouTube, guarda só o link.
    if "youtube" in url.lower() or "youtu.be" in url.lower():
        with (pasta / "videos.txt").open("a", encoding="utf-8") as arquivo:
            arquivo.write(f"{ad_id}: {url}\n")
