#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migra referências:
  [[REF]] Autor  -> [[REF:ID]] Autor

- Só altera linhas que tenham [[REF]] seguido do nome do autor (case-insensitive).
- Não toca em linhas que já tenham [[REF:...]].
- Suporta múltiplas ocorrências na mesma linha.
- Dry-run por padrão (mostra diff). Use --apply para escrever.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

# MAPEAMENTO: "autor citado" -> "ID"
AUTHOR_TO_ID = {
    "jelks": "JELKS-1993",
    "fagien": "FAGIEN-1999",
    "rohrich": "ROHRICH-2008",
    "anderson": "ANDERSON-1979",
    "mladick": "MLADICK-1979",
    "mccord": "MCCORD-1995",
    "coleman": "COLEMAN-1997",
    "tonnard": "TONNARD-2013",
    "hamra": "HAMRA-1995",
    "goldberg": "GOLDBERG-1998",
    "connell": "CONNELL-1978",
    "knize": "KNIZE-2001",
    "lambros": "LAMBROS-2007",
    "mendelson": "MENDELSON-2008",
    "pessa": "PESSA-2008",
    "zide": "ZIDE-1985",
    "codner": "MCCORD-1995",  # livro conjunto com McCord
    "tenzel": "TENZEL-1975",
    "hughes": "HUGHES-1937",
    "cutler": "CUTLER-1946",
    "beard": "CUTLER-1946",
    "mustardé": "MUSTARDE-1966",
    "mustarde": "MUSTARDE-1966",
    "hass": "HASS-2004",
    "gorney": "GORNEY-1999",
    "sarwer": "SARWER-2006",
    "collin": "COLLIN-1983",
    "perry": "PERRY-2013",
    "kpodzo": "KPODZO-2014",
    "marten": "MARTEN-2008",
    "massry": "MASSRY-2012",
    "flowers": "FLOWERS-1993",
    "rees": "REES-1984",
    "bodian": "BODIAN-1982",
    "hidalgo": "HIDALGO-2011",
    "putterman": "PUTTERMAN-1975",
    "park": "PARK-2008",
    "ramirez": "RAMIREZ-2000",
    "gunter": "GUNTER-2007",
    "hirmand": "HIRMAND-2010",
    "most": "MOST-2007",
    "weiss": "WEISS-1979",
    "jones": "WEISS-1979",  # mesmo paper
    "cohen": "COHEN-2017",  # adicionar na bibliografia se necessário
    "verpaele": "TONNARD-2013",  # mesmo paper do Tonnard
    "gordy": "ANDERSON-1979",  # coautor Anderson
    "adams": "ROHRICH-2008",  # coautor Rohrich
}

# Regex: [[REF]] seguido de espaço e autor
REF_TAG = r"\[\[REF\]\]"


def migrate_text(text: str) -> str:
    """Migra [[REF]] Autor -> [[REF:ID]] Autor."""
    out = text

    # Para cada autor, substitui: [[REF]] <spaces> Autor
    # Preserva capitalização original do autor
    for author_key, ref_id in AUTHOR_TO_ID.items():
        # Match: [[REF]] seguido de espaço(s) e o nome do autor
        # Captura o autor como aparece no texto
        pattern = re.compile(
            rf"(\[\[REF\]\])(\s+)({re.escape(author_key)})\b",
            re.IGNORECASE
        )

        def make_repl(rid: str):
            def repl(m: re.Match) -> str:
                return f"[[REF:{rid}]]{m.group(2)}{m.group(3)}"
            return repl

        out = pattern.sub(make_repl(ref_id), out)

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Migra [[REF]] Autor -> [[REF:ID]] Autor")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Escreve alterações nos arquivos (padrão: dry-run)"
    )
    ap.add_argument(
        "--root",
        default="content",
        help="Pasta raiz (default: content)"
    )
    ap.add_argument(
        "--glob",
        default="**/*.md",
        help="Glob de arquivos (default: **/*.md)"
    )
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Erro: pasta '{root}' não existe.")
        return 1

    files = sorted(root.glob(args.glob))

    # Arquivos a pular
    skip_prefixes = ("00_", "99_")
    skip_names = {"MOVE_MAP.md"}

    changed = 0
    total_replacements = 0

    for fp in files:
        if fp.name.startswith(skip_prefixes):
            continue
        if fp.name in skip_names:
            continue

        original = fp.read_text(encoding="utf-8")
        migrated = migrate_text(original)

        if migrated != original:
            changed += 1
            # Contar substituições
            orig_refs = len(re.findall(r"\[\[REF\]\]", original))
            new_refs = len(re.findall(r"\[\[REF\]\]", migrated))
            replacements = orig_refs - new_refs
            total_replacements += replacements

            if not args.apply:
                print(f"\n{'='*60}")
                print(f"📄 {fp}")
                print(f"   {replacements} substituição(ões)")
                print('='*60)
                diff = difflib.unified_diff(
                    original.splitlines(keepends=True),
                    migrated.splitlines(keepends=True),
                    fromfile=str(fp),
                    tofile=str(fp),
                    lineterm=""
                )
                for line in diff:
                    if line.startswith('+') and not line.startswith('+++'):
                        print(f"\033[32m{line}\033[0m", end='')
                    elif line.startswith('-') and not line.startswith('---'):
                        print(f"\033[31m{line}\033[0m", end='')
                    else:
                        print(line, end='')
            else:
                fp.write_text(migrated, encoding="utf-8")
                print(f"✅ {fp.name}: {replacements} ref(s) migrada(s)")

    print()
    if not args.apply:
        print(f"📊 DRY-RUN: {changed} arquivo(s) seriam alterados ({total_replacements} refs)")
        print("   Para aplicar: python3 tools/migrate_refs.py --apply")
    else:
        print(f"📊 APLICADO: {changed} arquivo(s) alterados ({total_replacements} refs migradas)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
