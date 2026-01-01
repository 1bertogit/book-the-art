#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera manuscrito consolidado a partir do sumário mestre.

- Concatena capítulos na ordem do 00_SUMARIO_MESTRE.md
- Remove tags internas ([[KEEP]], [[BOX]], [[MOVE]], etc.)
- Gera arquivo único para exportação/revisão

Uso:
    python3 tools/build_manuscrito.py
    python3 tools/build_manuscrito.py --clean  # remove tags internas
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
OUT_FILE = CONTENT_DIR / "00_MANUSCRITO.md"
SUMARIO = CONTENT_DIR / "00_SUMARIO_MESTRE.md"

# Regex para extrair links do sumário: [Título](./arquivo.md)
LINK_RE = re.compile(r"\]\(\./([^)]+\.md)\)")

# Tags internas a remover no modo --clean
INTERNAL_TAGS = [
    re.compile(r"\[\[/?KEEP\]\]\n?", re.IGNORECASE),
    re.compile(r"\[\[/?BOX\]\]\n?", re.IGNORECASE),
    re.compile(r"\[\[MOVE:CAP-\d+\]\].*?\[\[/MOVE:CAP-\d+\]\]\n?", re.DOTALL | re.IGNORECASE),
    re.compile(r"\[\[MOVE:CAP-\d+\]\]\n?", re.IGNORECASE),
    re.compile(r"\[\[/MOVE:CAP-\d+\]\]\n?", re.IGNORECASE),
]


def clean_text(text: str) -> str:
    """Remove tags internas do texto."""
    result = text
    for pattern in INTERNAL_TAGS:
        result = pattern.sub("", result)
    # Limpar linhas vazias excessivas
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera manuscrito consolidado")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove tags internas ([[KEEP]], [[BOX]], [[MOVE]])"
    )
    parser.add_argument(
        "--out",
        type=str,
        default=str(OUT_FILE),
        help=f"Arquivo de saída (default: {OUT_FILE})"
    )
    args = parser.parse_args()

    out_path = Path(args.out)

    print("📚 Gerando manuscrito consolidado...")
    print(f"   Sumário: {SUMARIO}")
    print(f"   Saída: {out_path}")
    print(f"   Clean: {'Sim' if args.clean else 'Não'}")
    print()

    if not SUMARIO.exists():
        print(f"❌ Sumário não encontrado: {SUMARIO}")
        return 1

    # Extrair lista de arquivos do sumário
    sum_text = SUMARIO.read_text(encoding="utf-8")
    rel_paths = LINK_RE.findall(sum_text)

    if not rel_paths:
        print("❌ Nenhum capítulo encontrado no sumário")
        return 1

    print(f"   Encontrados: {len(rel_paths)} capítulos")

    # Construir manuscrito
    parts: list[str] = []

    # Cabeçalho
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts.append("# The Art of Eyelid Surgery — Manuscrito Consolidado\n\n")
    parts.append(f"> Gerado automaticamente em {now}\n")
    parts.append("> Fonte: `00_SUMARIO_MESTRE.md`\n")
    if args.clean:
        parts.append("> Tags internas removidas (modo --clean)\n")
    parts.append("\n---\n")

    # Concatenar capítulos
    missing = 0
    for i, rel in enumerate(rel_paths, 1):
        fp = CONTENT_DIR / rel
        if not fp.exists():
            parts.append(f"\n\n---\n\n# ❌ Arquivo faltando: {rel}\n\n")
            missing += 1
            continue

        text = fp.read_text(encoding="utf-8").strip()

        if args.clean:
            text = clean_text(text)

        parts.append("\n\n---\n\n")
        parts.append(f"<!-- Capítulo {i}: {rel} -->\n\n")
        parts.append(text)
        parts.append("\n")

    # Rodapé
    parts.append("\n\n---\n\n")
    parts.append("# Fim do Manuscrito\n\n")
    parts.append(f"> Total: {len(rel_paths)} capítulos | {missing} faltando\n")

    # Escrever arquivo
    out_path.write_text("".join(parts), encoding="utf-8")

    # Estatísticas
    total_chars = sum(len(p) for p in parts)
    total_words = sum(len(p.split()) for p in parts)

    print()
    print(f"✅ Manuscrito gerado: {out_path}")
    print(f"   • {len(rel_paths)} capítulos")
    print(f"   • ~{total_words:,} palavras")
    print(f"   • ~{total_chars:,} caracteres")

    if missing > 0:
        print(f"   ⚠️  {missing} arquivo(s) faltando")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
