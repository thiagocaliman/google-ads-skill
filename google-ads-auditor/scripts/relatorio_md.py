"""
Gera relatório Markdown da auditoria Google Ads.
Usa Jinja2 para manter template separado do código.
"""
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader


def gerar_relatorio_md(
    resultados_auditorias: List[Dict[str, Any]],
    analises_criativos: List[Dict[str, Any]],
    customer_id: str,
    output_path: str | None = None,
) -> str:
    # Resolve caminhos do projeto.
    raiz = Path(__file__).resolve().parents[1]
    # Cria pasta de relatórios.
    pasta_relatorios = raiz / "relatorios"
    pasta_relatorios.mkdir(exist_ok=True)
    # Define o caminho padrão quando não foi informado.
    caminho = Path(output_path) if output_path else pasta_relatorios / f"auditoria_{customer_id}_{date.today().isoformat()}.md"
    # Prepara ambiente Jinja2.
    env = Environment(loader=FileSystemLoader(raiz / "templates"), autoescape=False)
    # Carrega template Markdown.
    template = env.get_template("relatorio_template.md")
    # Renderiza conteúdo final.
    conteudo = template.render(
        customer_id=customer_id,
        data_geracao=date.today().isoformat(),
        resumo=_resumo(resultados_auditorias),
        resultados=resultados_auditorias,
        analises_criativos=analises_criativos,
    )
    # Salva em UTF-8.
    caminho.write_text(conteudo, encoding="utf-8")
    return str(caminho)


def _resumo(resultados: List[Dict[str, Any]]) -> Dict[str, int]:
    # Soma contagens de todas as auditorias.
    return {
        "criticos": sum(len(item.get("criticos", [])) for item in resultados),
        "avisos": sum(len(item.get("avisos", [])) for item in resultados),
        "ok": sum(len(item.get("ok", [])) for item in resultados),
    }
