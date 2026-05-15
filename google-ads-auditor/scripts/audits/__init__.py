"""
Exporta as 7 auditorias da skill.
Usa importlib porque os arquivos começam com números por exigência da especificação.
"""
from importlib import import_module


AuditoriaConversoes = import_module(".01_conversoes", __name__).AuditoriaConversoes
AuditoriaTracking = import_module(".02_tracking", __name__).AuditoriaTracking
AuditoriaEstrutura = import_module(".03_estrutura", __name__).AuditoriaEstrutura
AuditoriaRemarketing = import_module(".04_remarketing", __name__).AuditoriaRemarketing
AuditoriaKeywords = import_module(".05_keywords", __name__).AuditoriaKeywords
AuditoriaAds = import_module(".06_ads", __name__).AuditoriaAds
AuditoriaBudget = import_module(".07_budget", __name__).AuditoriaBudget

__all__ = [
    "AuditoriaConversoes",
    "AuditoriaTracking",
    "AuditoriaEstrutura",
    "AuditoriaRemarketing",
    "AuditoriaKeywords",
    "AuditoriaAds",
    "AuditoriaBudget",
]
