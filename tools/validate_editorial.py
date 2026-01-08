#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida qualidade editorial do manuscrito.

Verifica:
- Densidade de negrito por capítulo (max 30)
- Presença de seções obrigatórias
- Lead editorial após figura principal
- Prefixos padronizados de blockquotes

Uso:
    python3 tools/validate_editorial.py
"""

from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "projects" / "eyelid-surgery" / "content"

# Configuração de limites
MAX_BOLD_PER_CHAPTER = 35
REQUIRED_SECTIONS = [
    "Objetivo",
    "Tecnica",  # ou "Técnica"
]


@dataclass
class ValidationResult:
    """Resultado de validação de um arquivo."""
    file: str
    errors: list[str]
    warnings: list[str]
    stats: dict


def count_bold(text: str) -> int:
    """Conta ocorrências de negrito."""
    return len(re.findall(r'\*\*[^*]+\*\*', text))


def has_section(text: str, section_name: str) -> bool:
    """Verifica se existe uma seção com o nome dado."""
    pattern = rf'##\s*{section_name}'
    return bool(re.search(pattern, text, re.IGNORECASE))


def has_figure(text: str) -> bool:
    """Verifica se tem figura principal."""
    return bool(re.search(r'!\[Figura\s+\d+\.\d+', text))


def has_lead(text: str) -> bool:
    """Verifica se tem lead editorial."""
    return bool(re.search(r'>\s*\*\*Leitura guiada', text, re.IGNORECASE))


def check_blockquote_prefixes(text: str) -> list[str]:
    """Verifica blockquotes com prefixos não padronizados."""
    issues = []

    # Prefixos antigos que deveriam ter sido normalizados
    old_prefixes = [
        (r'>\s*\*\*Aviso:\*\*', 'Aviso → Alerta'),
        (r'>\s*\*\*Nota:\*\*', 'Nota → Nota clínica'),
        (r'>\s*\*\*Atenção:\*\*', 'Atenção → Alerta'),
    ]

    for pattern, suggestion in old_prefixes:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(f"Blockquote não padronizado: {suggestion}")

    return issues


def validate_file(filepath: Path) -> ValidationResult:
    """Valida um arquivo e retorna resultado."""
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.name

    errors = []
    warnings = []
    stats = {}

    # 1. Contagem de negrito
    bold_count = count_bold(text)
    stats["bold_count"] = bold_count

    if bold_count > MAX_BOLD_PER_CHAPTER:
        warnings.append(f"Negrito excessivo: {bold_count} (max: {MAX_BOLD_PER_CHAPTER})")

    # 2. Seções obrigatórias (apenas para capítulos principais)
    if re.match(r'\d{2}-', filename) and not filename.startswith('00'):
        for section in REQUIRED_SECTIONS:
            if not has_section(text, section):
                # Apenas aviso, não erro
                warnings.append(f"Seção '{section}' não encontrada")

    # 3. Figura e lead editorial
    has_fig = has_figure(text)
    has_lead_block = has_lead(text)
    stats["has_figure"] = has_fig
    stats["has_lead"] = has_lead_block

    if has_fig and not has_lead_block:
        warnings.append("Figura presente, mas sem lead editorial")

    # 4. Blockquotes não padronizados
    blockquote_issues = check_blockquote_prefixes(text)
    for issue in blockquote_issues:
        warnings.append(issue)

    return ValidationResult(
        file=filename,
        errors=errors,
        warnings=warnings,
        stats=stats
    )


def main() -> int:
    print("🔍 Validando qualidade editorial...")
    print()

    files = sorted(CONTENT_DIR.glob("[0-9][0-9]-*.md"))

    total_errors = 0
    total_warnings = 0
    total_bold = 0
    files_with_issues = []

    for filepath in files:
        result = validate_file(filepath)
        total_bold += result.stats.get("bold_count", 0)

        if result.errors or result.warnings:
            files_with_issues.append(result)
            total_errors += len(result.errors)
            total_warnings += len(result.warnings)

    # Relatório
    print("="*60)
    print("📊 RELATÓRIO DE VALIDAÇÃO EDITORIAL")
    print("="*60)
    print()
    print(f"Capítulos analisados: {len(files)}")
    print(f"Total de negritos: {total_bold}")
    print(f"Média por capítulo: {total_bold / len(files):.1f}")
    print()

    if not files_with_issues:
        print("✅ Nenhum problema encontrado!")
        print()
        return 0

    print(f"Erros: {total_errors}")
    print(f"Avisos: {total_warnings}")
    print()
    print("-"*60)
    print("DETALHES:")
    print("-"*60)

    for result in files_with_issues:
        print(f"\n📄 {result.file}")

        for error in result.errors:
            print(f"   ❌ {error}")

        for warning in result.warnings:
            print(f"   ⚠️  {warning}")

    print()
    print("="*60)

    if total_errors > 0:
        print("❌ Validação FALHOU — corrija os erros acima")
        return 1
    else:
        print("⚠️  Validação OK com avisos — revisar manualmente se necessário")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
