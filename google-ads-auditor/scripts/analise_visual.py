"""
Analisa criativos baixados usando Claude quando a biblioteca Anthropic está disponível.
Retorna JSON estruturado em português brasileiro.
"""
import base64
import json
from pathlib import Path
from typing import Any, Dict


def analisar_criativo(image_path: str) -> Dict[str, Any]:
    # Importa Anthropic só no momento de uso para manter instalação base enxuta.
    import anthropic  # type: ignore

    # Cria client usando ANTHROPIC_API_KEY do ambiente.
    client = anthropic.Anthropic()
    # Lê a imagem em bytes.
    with open(image_path, "rb") as arquivo:
        # Codifica imagem em base64 para a API.
        image_data = base64.standard_b64encode(arquivo.read()).decode("utf-8")
    # Envia a imagem para análise visual.
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
                {"type": "text", "text": _prompt_analise()},
            ],
        }],
    )
    # Converte a resposta JSON em dict Python.
    resultado = json.loads(message.content[0].text)
    # Guarda o nome do arquivo para o relatório.
    resultado["arquivo"] = Path(image_path).name
    # Guarda o caminho original para embed no HTML.
    resultado["image_path"] = image_path
    return resultado


def analisar_criativo_com_fallback(image_path: str) -> Dict[str, Any]:
    # Protege a execução quando a chave ou pacote Anthropic não existe.
    try:
        return analisar_criativo(image_path)
    except Exception as erro:
        return {
            "arquivo": Path(image_path).name,
            "image_path": image_path,
            "copy_principal": "Não analisado automaticamente.",
            "cta_identificado": "Não identificado.",
            "cores_dominantes": [],
            "legibilidade": 0,
            "forca_visual": 0,
            "problemas": [f"Análise visual não executada: {erro}"],
            "sugestoes_melhoria": ["Configurar ANTHROPIC_API_KEY e instalar pacote anthropic se necessário."],
        }


def _prompt_analise() -> str:
    # Mantém o prompt centralizado para facilitar ajustes.
    return """Analise este criativo de Google Ads. Retorne JSON com:
- copy_principal: texto principal do anúncio
- cta_identificado: qual o call-to-action visual
- cores_dominantes: 3 cores principais em hex
- legibilidade: nota 0-10
- forca_visual: nota 0-10
- problemas: lista de problemas detectados
- sugestoes_melhoria: 3 sugestões concretas

Responda APENAS o JSON, sem markdown, sem preamble."""
