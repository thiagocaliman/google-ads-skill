"""
Gera relatório HTML brutalist AI PRO Revolution.
O HTML é standalone com CSS e imagens em base64.
"""
import base64
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader


def gerar_relatorio_html(
    resultados_auditorias: List[Dict[str, Any]],
    analises_criativos: List[Dict[str, Any]],
    customer_id: str,
    output_path: str | None = None,
) -> str:
    # Resolve raiz do projeto.
    raiz = Path(__file__).resolve().parents[1]
    # Garante pasta final.
    pasta_relatorios = raiz / "relatorios"
    pasta_relatorios.mkdir(exist_ok=True)
    # Define nome padrão do arquivo.
    caminho = Path(output_path) if output_path else pasta_relatorios / f"auditoria_{customer_id}_{date.today().isoformat()}.html"
    # Lê CSS brutalist para inline.
    css_inline = (raiz / "assets" / "brutalist.css").read_text(encoding="utf-8")
    # Embarca logo em base64.
    logo_base64 = _base64_data_uri(raiz / "assets" / "logo_aipro.svg", "image/svg+xml")
    # Embarca imagens dos criativos.
    analises = [_com_imagem_base64(item) for item in analises_criativos]
    # Prepara Jinja.
    env = Environment(loader=FileSystemLoader(raiz / "templates"), autoescape=True)
    template = env.get_template("relatorio_template.html")
    # Renderiza HTML final.
    html = template.render(
        css_inline=css_inline,
        logo_base64=logo_base64,
        customer_id=customer_id,
        data_geracao=date.today().isoformat(),
        resumo=_resumo(resultados_auditorias),
        resultados=resultados_auditorias,
        analises_criativos=analises,
    )
    caminho.write_text(html, encoding="utf-8")
    return str(caminho)


def _base64_data_uri(caminho: Path, media_type: str) -> str:
    # Lê bytes e converte para data URI.
    dados = base64.b64encode(caminho.read_bytes()).decode("utf-8")
    return f"data:{media_type};base64,{dados}"


def _com_imagem_base64(item: Dict[str, Any]) -> Dict[str, Any]:
    # Copia o dict para não alterar o original.
    novo = dict(item)
    # Lê caminho da imagem quando existe.
    image_path = novo.get("image_path")
    # Embarca imagem PNG se o arquivo ainda existir.
    if image_path and Path(image_path).exists():
        novo["imagem_base64"] = _base64_data_uri(Path(image_path), "image/png")
    return novo


def _resumo(resultados: List[Dict[str, Any]]) -> Dict[str, int]:
    # Soma contagens de todas as auditorias.
    return {
        "criticos": sum(len(item.get("criticos", [])) for item in resultados),
        "avisos": sum(len(item.get("avisos", [])) for item in resultados),
        "ok": sum(len(item.get("ok", [])) for item in resultados),
    }
