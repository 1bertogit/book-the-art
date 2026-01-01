#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera versão limpa do manuscrito para exportação.

Remove tags internas e prepara para PDF/DOCX/EPUB.

Uso:
    python3 tools/clean_manuscript.py
    python3 tools/clean_manuscript.py --ref-style=paren    # [[REF:ID]] → (ID)
    python3 tools/clean_manuscript.py --strip-backlog      # remove "Figura sugerida"
    python3 tools/clean_manuscript.py --out dist/livro.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
DIST_DIR = ROOT / "dist"
INPUT_FILE = CONTENT_DIR / "00_MANUSCRITO.md"
DEFAULT_OUT = DIST_DIR / "manuscrito_limpo.md"

# Tags internas a remover
TAG_PATTERNS = [
    # [[KEEP]] e [[/KEEP]]
    re.compile(r"^\s*\[\[/?KEEP\]\]\s*$\n?", re.MULTILINE),
    # [[BOX]] e [[/BOX]]
    re.compile(r"^\s*\[\[/?BOX\]\]\s*$\n?", re.MULTILINE),
    # [[MOVE:CAP-XX]] e [[/MOVE:CAP-XX]] (linhas inteiras)
    re.compile(r"^\s*\[\[/?MOVE:CAP-\d+\]\]\s*$\n?", re.MULTILINE),
    # Comentários HTML de capítulo
    re.compile(r"^\s*<!--.*?-->\s*$\n?", re.MULTILINE),
]

# Backlog patterns (opcional)
BACKLOG_PATTERNS = [
    re.compile(r"^>\s*\*\*Figura sugerida[:\*]*.*$\n?", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*\(inserir esquema.*?\)\s*$\n?", re.MULTILINE | re.IGNORECASE),
]

# Ref patterns
REF_PATTERN = re.compile(r"\[\[REF:([A-Z0-9_-]+)\]\]")


def clean_tags(text: str) -> str:
    """Remove tags internas."""
    result = text
    for pattern in TAG_PATTERNS:
        result = pattern.sub("", result)
    return result


def clean_backlog(text: str) -> str:
    """Remove placeholders de figuras/backlog."""
    result = text
    for pattern in BACKLOG_PATTERNS:
        result = pattern.sub("", result)
    return result


def convert_refs(text: str, style: str) -> str:
    """Converte [[REF:ID]] para outro formato."""
    if style == "keep":
        return text
    elif style == "paren":
        # [[REF:JELKS-1993]] → (JELKS-1993)
        return REF_PATTERN.sub(r"(\1)", text)
    elif style == "superscript":
        # [[REF:JELKS-1993]] → ^JELKS-1993^
        return REF_PATTERN.sub(r"^[\1]^", text)
    elif style == "remove":
        # Remove completamente
        return REF_PATTERN.sub("", text)
    else:
        return text


def normalize_whitespace(text: str) -> str:
    """Normaliza espaços em branco excessivos."""
    # Remove mais de 2 linhas vazias consecutivas
    result = re.sub(r"\n{4,}", "\n\n\n", text)
    # Remove espaços no final das linhas
    result = re.sub(r" +$", "", result, flags=re.MULTILINE)
    return result


def convert_hr_separators(text: str) -> str:
    """Converte --- horizontais para *** (evita conflito com YAML)."""
    # Apenas --- em linha própria (não no header YAML)
    return re.sub(r"^---$", "* * *", text, flags=re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera versão limpa do manuscrito para exportação"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(INPUT_FILE),
        help=f"Arquivo de entrada (default: {INPUT_FILE})"
    )
    parser.add_argument(
        "--out",
        type=str,
        default=str(DEFAULT_OUT),
        help=f"Arquivo de saída (default: {DEFAULT_OUT})"
    )
    parser.add_argument(
        "--ref-style",
        choices=["keep", "paren", "superscript", "remove"],
        default="keep",
        help="Estilo de referências: keep (manter), paren (parênteses), superscript, remove"
    )
    parser.add_argument(
        "--strip-backlog",
        action="store_true",
        help="Remove placeholders de figuras sugeridas"
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Remove cabeçalho gerado automaticamente"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out)

    print("🧹 Limpando manuscrito para exportação...")
    print(f"   Entrada: {input_path}")
    print(f"   Saída: {out_path}")
    print(f"   Refs: {args.ref_style}")
    print(f"   Strip backlog: {args.strip_backlog}")
    print()

    if not input_path.exists():
        print(f"❌ Arquivo não encontrado: {input_path}")
        print("   Execute primeiro: python3 tools/build_manuscrito.py")
        return 1

    # Ler entrada
    text = input_path.read_text(encoding="utf-8")
    original_len = len(text)

    # Aplicar limpezas
    text = clean_tags(text)

    if args.strip_backlog:
        text = clean_backlog(text)

    text = convert_refs(text, args.ref_style)
    text = normalize_whitespace(text)
    
    # Converter separadores horizontais --- para * * * (evita conflito YAML no Pandoc)
    text = convert_hr_separators(text)

    # Adicionar cabeçalho limpo (opcional)
    if not args.no_header:
        now = datetime.now().strftime("%Y-%m-%d")
        header = f"""---
title: "The Art of Eyelid Surgery"
author: "Dr. Marcelo Cury"
date: "{now}"
lang: pt-BR
---

"""
        # Remover todos os YAML headers existentes
        while text.startswith("---"):
            end_idx = text.find("---", 3)
            if end_idx > 0:
                text = text[end_idx + 3:].lstrip()
            else:
                break
        
        # Remover cabeçalhos gerados automaticamente
        text = re.sub(
            r"^# The Art of Eyelid Surgery — Manuscrito.*?\n+> Gerado automaticamente.*?\n+> Fonte:.*?\n+---\n*",
            "",
            text,
            flags=re.MULTILINE
        )
        
        # Remover separadores órfãos (--- sozinho em uma linha) até encontrar conteúdo real
        lines = text.split("\n")
        while lines and lines[0].strip() in ("---", ""):
            lines.pop(0)
        text = "\n".join(lines)
        
        text = header + text.lstrip()

    # Criar diretório de saída
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Escrever saída
    out_path.write_text(text, encoding="utf-8")

    # Estatísticas
    final_len = len(text)
    reduction = ((original_len - final_len) / original_len) * 100 if original_len > 0 else 0
    word_count = len(text.split())

    print(f"✅ Manuscrito limpo gerado: {out_path}")
    print(f"   • {word_count:,} palavras")
    print(f"   • {final_len:,} caracteres")
    print(f"   • Redução: {reduction:.1f}%")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
