#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reduz uso excessivo de negrito nos capítulos.

Regras:
1. MANTER negrito em termos técnicos (primeira ocorrência)
2. MANTER negrito em labels de seção
3. REMOVER negrito de palavras comuns
4. REMOVER negrito em parágrafos com >3 negritos (manter só o primeiro)

Uso:
    python3 tools/reduce_bold.py --dry-run          # Preview de mudanças
    python3 tools/reduce_bold.py --apply            # Aplicar mudanças
    python3 tools/reduce_bold.py --apply --verbose  # Aplicar com detalhes
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Set

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "projects" / "eyelid-surgery" / "content"
CONFIG_DIR = ROOT / "config"
TERMOS_FILE = CONFIG_DIR / "termos_tecnicos.txt"

# Palavras comuns que NUNCA devem ficar em negrito
PALAVRAS_COMUNS = {
    "pálpebra", "palpebra", "pálpebras", "palpebras",
    "cirurgia", "cirurgias", "cirúrgico", "cirúrgica",
    "paciente", "pacientes",
    "olho", "olhos",
    "face", "facial",
    "pele", "tecido", "tecidos",
    "superior", "inferior",
    "lateral", "medial",
    "anterior", "posterior",
    "importante", "essencial", "fundamental",
    "sempre", "nunca", "muito",
    "resultado", "resultados",
    "tratamento", "procedimento",
    "técnica", "método",
}


@dataclass
class BoldMatch:
    """Representa um match de negrito no texto."""
    start: int
    end: int
    content: str
    line_num: int
    keep: bool = True
    reason: str = ""


def load_termos_tecnicos() -> Set[str]:
    """Carrega lista de termos técnicos a preservar."""
    termos = set()
    if TERMOS_FILE.exists():
        for line in TERMOS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                termos.add(line.lower())
    return termos


def is_section_label(content: str) -> bool:
    """Verifica se o conteúdo é um label de seção."""
    labels = [
        "indicar quando", "evitar quando", "aplicar quando",
        "erro comum", "erro nota", "regra de ouro", "regra:",
        "ponto clínico", "prevenção", "resgate", "consequência",
        "nota clínica", "alerta", "leitura guiada",
        "visão geral", "variações", "zona de risco",
    ]
    content_lower = content.lower()
    return any(label in content_lower for label in labels)


def find_bold_matches(text: str) -> list[BoldMatch]:
    """Encontra todos os negritos no texto."""
    matches = []
    # Pattern para **texto** ou __texto__
    pattern = re.compile(r'\*\*(.+?)\*\*|__(.+?)__')

    lines = text.split('\n')
    pos = 0

    for line_num, line in enumerate(lines, 1):
        for m in pattern.finditer(line):
            content = m.group(1) or m.group(2)
            matches.append(BoldMatch(
                start=pos + m.start(),
                end=pos + m.end(),
                content=content,
                line_num=line_num
            ))
        pos += len(line) + 1  # +1 para o \n

    return matches


def analyze_bold(
    matches: list[BoldMatch],
    termos: Set[str],
    seen_terms: Set[str]
) -> list[BoldMatch]:
    """Analisa cada negrito e decide se deve manter ou remover."""

    for match in matches:
        content_lower = match.content.lower().strip()

        # Regra 1: Labels de seção → MANTER
        if is_section_label(match.content):
            match.keep = True
            match.reason = "label de seção"
            continue

        # Regra 2: Termo técnico (primeira ocorrência) → MANTER
        if content_lower in termos:
            if content_lower not in seen_terms:
                match.keep = True
                match.reason = "termo técnico (1ª ocorrência)"
                seen_terms.add(content_lower)
            else:
                match.keep = False
                match.reason = "termo técnico (repetido)"
            continue

        # Verificar se é parte de um termo técnico maior
        is_part_of_term = any(
            content_lower in termo or termo in content_lower
            for termo in termos
        )
        if is_part_of_term and content_lower not in seen_terms:
            match.keep = True
            match.reason = "parte de termo técnico"
            seen_terms.add(content_lower)
            continue

        # Regra 3: Palavras comuns → REMOVER
        words = set(content_lower.split())
        if words & PALAVRAS_COMUNS and len(words) <= 2:
            match.keep = False
            match.reason = "palavra comum"
            continue

        # Regra 4: Conteúdo muito curto (1-2 palavras genéricas) → avaliar
        if len(match.content.split()) <= 2:
            # Se já vimos esse termo, remover
            if content_lower in seen_terms:
                match.keep = False
                match.reason = "repetido"
            else:
                match.keep = True
                match.reason = "termo único"
                seen_terms.add(content_lower)
        else:
            # Frases longas em negrito → geralmente remover
            if len(match.content) > 50:
                match.keep = False
                match.reason = "frase longa (>50 chars)"
            else:
                match.keep = True
                match.reason = "frase curta"

    return matches


def limit_bold_per_paragraph(text: str, matches: list[BoldMatch], max_per_para: int = 3) -> list[BoldMatch]:
    """Limita negritos por parágrafo, mantendo apenas os primeiros."""
    paragraphs = text.split('\n\n')
    para_starts = []
    pos = 0
    for para in paragraphs:
        para_starts.append((pos, pos + len(para)))
        pos += len(para) + 2  # +2 para \n\n

    for para_start, para_end in para_starts:
        para_matches = [m for m in matches if para_start <= m.start < para_end and m.keep]
        if len(para_matches) > max_per_para:
            # Manter apenas os primeiros max_per_para
            for m in para_matches[max_per_para:]:
                m.keep = False
                m.reason = f"excesso no parágrafo (>{max_per_para})"

    return matches


def apply_changes(text: str, matches: list[BoldMatch]) -> str:
    """Aplica as mudanças, removendo negritos marcados."""
    # Processar de trás para frente para não invalidar posições
    result = text
    for match in sorted(matches, key=lambda m: m.start, reverse=True):
        if not match.keep:
            # Substituir **texto** por texto
            old = result[match.start:match.end]
            new = match.content
            result = result[:match.start] + new + result[match.end:]
    return result


def process_file(
    filepath: Path,
    termos: Set[str],
    dry_run: bool = True,
    verbose: bool = False
) -> dict:
    """Processa um arquivo e retorna estatísticas."""
    text = filepath.read_text(encoding="utf-8")
    matches = find_bold_matches(text)

    if not matches:
        return {"file": filepath.name, "total": 0, "kept": 0, "removed": 0}

    seen_terms: Set[str] = set()
    matches = analyze_bold(matches, termos, seen_terms)
    matches = limit_bold_per_paragraph(text, matches)

    kept = sum(1 for m in matches if m.keep)
    removed = sum(1 for m in matches if not m.keep)

    stats = {
        "file": filepath.name,
        "total": len(matches),
        "kept": kept,
        "removed": removed,
        "reduction": f"{(removed / len(matches) * 100):.1f}%" if matches else "0%"
    }

    if verbose:
        print(f"\n{'='*60}")
        print(f"Arquivo: {filepath.name}")
        print(f"{'='*60}")
        for m in matches:
            status = "MANTER" if m.keep else "REMOVER"
            icon = "✓" if m.keep else "✗"
            print(f"  {icon} L{m.line_num}: **{m.content[:40]}...** → {status} ({m.reason})")

    if not dry_run:
        new_text = apply_changes(text, matches)
        filepath.write_text(new_text, encoding="utf-8")

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reduz uso excessivo de negrito nos capítulos"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostrar mudanças sem aplicar"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplicar mudanças nos arquivos"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar detalhes de cada mudança"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Processar apenas um arquivo específico"
    )
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Especifique --dry-run ou --apply")
        return 1

    print("🔍 Analisando uso de negrito...")
    print()

    termos = load_termos_tecnicos()
    print(f"   Termos técnicos carregados: {len(termos)}")
    print()

    if args.file:
        files = [Path(args.file)]
    else:
        files = sorted(CONTENT_DIR.glob("[0-9][0-9]-*.md"))

    total_stats = {"total": 0, "kept": 0, "removed": 0}

    for filepath in files:
        stats = process_file(
            filepath,
            termos,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        total_stats["total"] += stats["total"]
        total_stats["kept"] += stats["kept"]
        total_stats["removed"] += stats["removed"]

        if not args.verbose:
            icon = "📄" if args.dry_run else "✅"
            print(f"  {icon} {stats['file']}: {stats['total']} → {stats['kept']} (−{stats['removed']})")

    print()
    print("="*50)
    print("📊 RESUMO")
    print("="*50)
    print(f"   Total de negritos: {total_stats['total']}")
    print(f"   Mantidos: {total_stats['kept']}")
    print(f"   Removidos: {total_stats['removed']}")
    if total_stats['total'] > 0:
        reduction = (total_stats['removed'] / total_stats['total']) * 100
        print(f"   Redução: {reduction:.1f}%")
    print()

    if args.dry_run:
        print("💡 Execute com --apply para aplicar as mudanças")
    else:
        print("✅ Mudanças aplicadas!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
