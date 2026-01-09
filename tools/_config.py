#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações compartilhadas para scripts de ferramentas.

Centraliza paths, regex patterns e constantes usadas em múltiplos scripts.
"""

from __future__ import annotations

import re
from pathlib import Path

# =============================================================================
# PATHS
# =============================================================================

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "projects" / "eyelid-surgery"
CONTENT_DIR = PROJECT_DIR / "content"
FIGURES_DIR = PROJECT_DIR / "assets" / "figures"
FIGURES_YAML = PROJECT_DIR / "figures.yml"
CONFIG_DIR = ROOT / "config"
DIST_DIR = ROOT / "dist"

# =============================================================================
# REGEX PATTERNS
# =============================================================================

# Capítulo do nome do arquivo: "01-titulo.md" → "01"
FILE_CAP_RE = re.compile(r"^(\d+)[-_].+\.md$", re.IGNORECASE)

# Links internos [[MOVE:CAP-XX]]
MOVE_RE = re.compile(r"\[\[MOVE:\s*CAP-(\d+|XX)\s*\]\]", re.IGNORECASE)

# Referências [[REF]]
REF_RE = re.compile(r"\[\[REF\]\]", re.IGNORECASE)

# Figuras sugeridas
FIG_SUGERIDA_RE = re.compile(r"\*\*Figura sugerida[:\*]*|FIG-\d+", re.IGNORECASE)

# Primeiro H1 do arquivo
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

# =============================================================================
# SKIP FILES
# =============================================================================

# Arquivos gerados automaticamente que devem ser ignorados em validações
SKIP_FILES = {
    "MOVE_MAP.md",
    "SUMMARY.md",
    "00_SUMARIO_MESTRE.md",
    "00_MAPA_DE_LINKS_MOVE.md",
    "00_BACKLOG_ARTE.md",
    "00_BACKLOG_REFERENCIAS.md",
    "00_MANUSCRITO.md",
    "00_FRONT_MATTER.md",
}

# Prefixos de arquivos a ignorar
SKIP_FILE_PREFIXES = ("00_", "99_")


def should_skip_file(filename: str) -> bool:
    """Verifica se um arquivo deve ser ignorado em validações."""
    return (
        filename in SKIP_FILES or
        filename.startswith(SKIP_FILE_PREFIXES)
    )


# =============================================================================
# EDITORIAL CONSTANTS
# =============================================================================

# Limite máximo de negritos por capítulo
MAX_BOLD_PER_CHAPTER = 35

# Seções obrigatórias em capítulos
REQUIRED_SECTIONS = [
    "Objetivo",
    "Tecnica",  # ou "Técnica"
]

# Mapeamento de títulos de BOX para saída formatada
BOX_MAPPING = {
    "pérola clínica": "PÉROLA CLÍNICA",
    "perola clinica": "PÉROLA CLÍNICA",
    "pearl": "PÉROLA CLÍNICA",
    "atenção": "ATENÇÃO",
    "atencao": "ATENÇÃO",
    "warning": "ATENÇÃO",
    "alerta": "ATENÇÃO",
    "técnica": "TÉCNICA",
    "tecnica": "TÉCNICA",
    "technique": "TÉCNICA",
    "evidência": "EVIDÊNCIA",
    "evidencia": "EVIDÊNCIA",
    "evidence": "EVIDÊNCIA",
    "regra de ouro": "REGRA DE OURO",
    "regra": "REGRA DE OURO",
    "rule": "REGRA DE OURO",
    "": "NOTA CLÍNICA",  # BOX sem título
}
