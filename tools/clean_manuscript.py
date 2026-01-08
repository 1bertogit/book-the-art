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
CONTENT_DIR = ROOT / "projects" / "eyelid-surgery" / "content"
DIST_DIR = ROOT / "dist"
INPUT_FILE = CONTENT_DIR / "00_MANUSCRITO.md"
DEFAULT_OUT = DIST_DIR / "manuscrito_limpo.md"

# Tags internas a remover (linhas inteiras)
TAG_PATTERNS_LINE = [
    # [[KEEP]] e [[/KEEP]] em linha própria
    re.compile(r"^\s*\[\[/?KEEP\]\]\s*$\n?", re.MULTILINE),
    # [[BOX]] e [[/BOX]] em linha própria
    re.compile(r"^\s*\[\[/?BOX[^\]]*\]\]\s*$\n?", re.MULTILINE),
    # [[MOVE:CAP-XX]] e [[/MOVE:CAP-XX]] em linha própria
    re.compile(r"^\s*\[\[/?MOVE:CAP-[^\]]*\]\]\s*$\n?", re.MULTILINE),
    # Comentários HTML de capítulo
    re.compile(r"^\s*<!--.*?-->\s*$\n?", re.MULTILINE),
]

# Tags internas INLINE (dentro do texto)
TAG_PATTERNS_INLINE = [
    # [[KEEP]] e [[/KEEP]]
    re.compile(r"\s*\[\[/?KEEP\]\]\s*"),
    # [[BOX:...]] e [[/BOX:...]] e [[BOX]] inline
    re.compile(r"\s*\[\[/?BOX[^\]]*\]\]\s*"),
    # [[MOVE:CAP-XX]] e [[/MOVE:CAP-XX]] inline
    re.compile(r"\s*\[\[/?MOVE:CAP-[^\]]*\]\]\s*"),
    # [[/MOVE:CAP-XX]] órfãos
    re.compile(r"\s*\[\[/MOVE:[^\]]*\]\]\s*"),
]

# Backlog patterns (opcional)
BACKLOG_PATTERNS = [
    re.compile(r"^>\s*\*\*Figura sugerida[:\*]*.*$\n?", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*\(inserir esquema.*?\)\s*$\n?", re.MULTILINE | re.IGNORECASE),
]

# Ref patterns
REF_PATTERN = re.compile(r"\[\[REF:([A-Z0-9_-]+)\]\]")


def clean_tags(text: str) -> str:
    """Remove tags internas (linhas inteiras e inline)."""
    result = text

    # Primeiro: remover tags em linhas próprias
    for pattern in TAG_PATTERNS_LINE:
        result = pattern.sub("", result)

    # Depois: remover tags inline (dentro do texto)
    for pattern in TAG_PATTERNS_INLINE:
        result = pattern.sub(" ", result)  # Substituir por espaço para não colar palavras

    # Limpar espaços duplos resultantes
    result = re.sub(r"  +", " ", result)

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


def ensure_spacing_around_blocks(text: str) -> str:
    """Garante linha em branco antes e depois de headers e listas."""
    result = text

    # === HEADERS ===
    # Linha vazia ANTES de headers (se não houver)
    result = re.sub(r'([^\n])\n(#{1,3}\s)', r'\1\n\n\2', result)
    # Linha vazia DEPOIS de headers (se não houver)
    result = re.sub(r'(#{1,3}[^\n]+)\n([^\n#])', r'\1\n\n\2', result)

    # === LISTAS ===
    # Linha vazia ANTES de listas (-, *, [ ]) quando precedidas por texto
    result = re.sub(r'([^\n\-\*\[\s])\n([\-\*]\s|\[[ x]\]\s)', r'\1\n\n\2', result)
    # Linha vazia DEPOIS de listas quando seguidas por texto (não lista)
    result = re.sub(r'([\-\*].*)\n([^\-\*\[\n\s])', r'\1\n\n\2', result)

    # === BLOCKQUOTES ===
    # Linha vazia ANTES de blockquotes
    result = re.sub(r'([^\n>])\n(>\s)', r'\1\n\n\2', result)
    # Linha vazia DEPOIS de blockquotes
    result = re.sub(r'(>.*)\n([^>\n])', r'\1\n\n\2', result)

    return result


def break_long_paragraphs(text: str, max_sentences: int = 6) -> str:
    """Quebra parágrafos muito longos em parágrafos menores."""
    lines = text.split('\n')
    result_lines = []

    for line in lines:
        # Ignorar headers, listas, blockquotes, imagens
        if (line.startswith('#') or
            line.startswith('-') or
            line.startswith('*') or
            line.startswith('>') or
            line.startswith('[') or
            line.startswith('!') or
            not line.strip()):
            result_lines.append(line)
            continue

        # Contar sentenças (aproximado)
        sentences = re.split(r'(?<=[.!?])\s+', line)
        if len(sentences) > max_sentences:
            # Dividir em grupos
            mid = len(sentences) // 2
            first_half = ' '.join(sentences[:mid])
            second_half = ' '.join(sentences[mid:])
            result_lines.append(first_half)
            result_lines.append('')  # linha vazia
            result_lines.append(second_half)
        else:
            result_lines.append(line)

    return '\n'.join(result_lines)


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


def normalize_blockquotes(text: str) -> str:
    """Padroniza prefixos de blockquotes para consistência editorial."""
    # Mapeamento de prefixos antigos → novos
    replacements = [
        # Avisos e alertas
        (r'>\s*\*\*Aviso:\*\*', '> **Alerta:**'),
        (r'>\s*\*\*Aviso importante:\*\*', '> **Alerta:**'),
        (r'>\s*\*\*Atenção:\*\*', '> **Alerta:**'),
        (r'>\s*\*\*Cuidado:\*\*', '> **Alerta:**'),

        # Notas
        (r'>\s*\*\*Nota:\*\*', '> **Nota clínica:**'),
        (r'>\s*\*\*Nota de escopo:\*\*', '> **Nota de escopo:**'),  # manter
        (r'>\s*\*\*Observação:\*\*', '> **Nota clínica:**'),

        # Regras
        (r'>\s*\*\*Regra:\*\*', '> **Regra de ouro:**'),

        # Erros (padronizar formato)
        (r'>\s*\*\*Erro\s+nota\s+7:\*\*', '> **Erro Nota 7:**'),
        (r'>\s*\*\*Erro\s+Nota\s+7:\*\*', '> **Erro Nota 7:**'),
    ]

    result = text
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    return result


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

    # NOVO: Garantir espaçamento correto antes/depois de blocos
    text = ensure_spacing_around_blocks(text)

    # NOVO: Quebrar parágrafos muito longos
    text = break_long_paragraphs(text)

    text = normalize_whitespace(text)

    # NOVO: Padronizar prefixos de blockquotes
    text = normalize_blockquotes(text)

    # Converter separadores horizontais --- para * * * (evita conflito YAML no Pandoc)
    text = convert_hr_separators(text)

    # Adicionar cabeçalho limpo (opcional)
    if not args.no_header:
        now = datetime.now().strftime("%Y-%m-%d")
        header = f"""---
title: "The Art of Eyelid Surgery"
subtitle: "Cirurgia Palpebral e Periorbitária"
author: "Dr. Marcelo Cury"
date: "{now}"
lang: pt-BR
rights: "© Dr. Marcelo Cury. Conteúdo baseado no curso online do autor."
toc: true
toc-title: "Sumário"
toc-depth: 2
---

"""
        # Remover todos os YAML headers existentes
        while text.startswith("---"):
            end_idx = text.find("---", 3)
            if end_idx > 0:
                text = text[end_idx + 3:].lstrip()
            else:
                break
        
        # Remover cabeçalhos gerados automaticamente (várias variações)
        text = re.sub(
            r"^# The Art of Eyelid Surgery — Manuscrito.*?\n+> Gerado automaticamente.*?\n+> Fonte:.*?\n*(\* \* \*\n*)?",
            "",
            text,
            flags=re.MULTILINE | re.DOTALL
        )
        # Remover título órfão se ainda existir
        text = re.sub(
            r"^# The Art of Eyelid Surgery — Manuscrito Consolidado\s*\n",
            "",
            text,
            flags=re.MULTILINE
        )
        # Remover linhas "Gerado automaticamente" órfãs
        text = re.sub(
            r"^>\s*Gerado automaticamente.*?\n",
            "",
            text,
            flags=re.MULTILINE
        )
        # Remover linhas "Fonte:" órfãs
        text = re.sub(
            r"^>\s*Fonte:.*?\n",
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
