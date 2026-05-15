"""
AI PRO Revolution | Google Ads Auditor v1.0.
Auditoria completa de contas Google Ads com relatórios Markdown e HTML.
"""
import argparse
from pathlib import Path
from typing import Any, Dict, List

from google.ads.googleads.client import GoogleAdsClient
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

from analise_visual import analisar_criativo_com_fallback
from audits import (
    AuditoriaAds,
    AuditoriaBudget,
    AuditoriaConversoes,
    AuditoriaEstrutura,
    AuditoriaKeywords,
    AuditoriaRemarketing,
    AuditoriaTracking,
)
from config import ConfigError, carregar_credenciais, carregar_customer_id_padrao
from download_criativos import baixar_imagens_ads
from relatorio_html import gerar_relatorio_html
from relatorio_md import gerar_relatorio_md


console = Console()


def main() -> None:
    # Mostra header brutalist no terminal.
    console.print(Panel.fit(
        "[bold orange1]AI PRO REVOLUTION[/bold orange1]\n"
        "[white]Google Ads Auditor v1.0[/white]\n"
        "[dim]aiprorevolution.com.br[/dim]",
        border_style="orange1",
    ))
    # Lê argumentos de linha de comando.
    args = _parse_args()
    try:
        # Carrega credenciais e valida .env.
        credenciais = carregar_credenciais()
        # Define customer_id por CLI ou .env.
        customer_id = (args.customer_id or carregar_customer_id_padrao()).replace("-", "")
        # Cria client oficial Google Ads.
        client = GoogleAdsClient.load_from_dict(credenciais)
        # Executa as 7 auditorias.
        resultados = _rodar_auditorias(client, customer_id)
        # Baixa criativos em pasta local.
        imagens = baixar_imagens_ads(client, customer_id, str(_raiz() / "criativos_baixados"))
        # Analisa criativos com fallback amigável.
        analises = [analisar_criativo_com_fallback(imagem) for imagem in track(imagens, description="Analisando criativos")]
        # Gera relatórios finais.
        md_path = gerar_relatorio_md(resultados, analises, customer_id)
        html_path = gerar_relatorio_html(resultados, analises, customer_id)
        # Mostra caminhos de saída.
        console.print(f"[green]Relatório Markdown:[/green] {md_path}")
        console.print(f"[green]Relatório HTML:[/green] {html_path}")
    except ConfigError as erro:
        console.print(f"[bold red]{erro}[/bold red]")


def _parse_args() -> argparse.Namespace:
    # Configura ajuda de CLI.
    parser = argparse.ArgumentParser(description="Audita uma conta Google Ads e gera relatórios AI PRO.")
    # Customer ID aceita com ou sem hífens.
    parser.add_argument("--customer-id", help="Customer ID da conta cliente, com ou sem hífens.")
    # Retorna namespace do argparse.
    return parser.parse_args()


def _rodar_auditorias(client: Any, customer_id: str) -> List[Dict[str, Any]]:
    # Lista as classes na ordem oficial da especificação.
    classes = [
        AuditoriaConversoes,
        AuditoriaTracking,
        AuditoriaEstrutura,
        AuditoriaRemarketing,
        AuditoriaKeywords,
        AuditoriaAds,
        AuditoriaBudget,
    ]
    # Acumula resultados.
    resultados = []
    # Executa com barra de progresso.
    for classe in track(classes, description="Rodando auditorias"):
        try:
            resultados.append(classe(client, customer_id).executar())
        except Exception as erro:
            resultados.append({
                "titulo": f"⚠️ {classe.__name__}",
                "criticos": [f"Auditoria não executada: {erro}"],
                "avisos": [],
                "ok": [],
                "recomendacoes": ["Revisar compatibilidade GAQL desta seção com a versão atual da Google Ads API."],
            })
    return resultados


def _raiz() -> Path:
    # Resolve raiz do projeto a partir de scripts/auditor.py.
    return Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    main()
