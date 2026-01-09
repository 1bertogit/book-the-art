#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida referências:
- Todo [[REF:ID]] usado no texto deve existir em 99_BIBLIOGRAFIA.md
- Avisa sobre IDs definidos mas não usados (não falha)

Uso:
    python3 tools/validate_refs.py
"""

from __future__ import annotations

import re
import sys

from _config import CONTENT_DIR, SKIP_FILE_PREFIXES, SKIP_FILES

BIB_FILE = CONTENT_DIR / "99_BIBLIOGRAFIA.md"

# Regex para [[REF:ID]] no texto
REF_IN_TEXT_RE = re.compile(r"\[\[REF:([A-Z0-9_-]+)\]\]")

# Regex para **[ID]** na bibliografia (formato atual)
BIB_ID_RE = re.compile(r"\*\*\[([A-Z0-9_-]+)\]\*\*")


def iter_md_files():
    """Itera arquivos markdown de capítulos."""
    for fp in sorted(CONTENT_DIR.glob("*.md")):
        if fp.name in SKIP_FILES:
            continue
        if fp.name.startswith(SKIP_FILE_PREFIXES):
            continue
        yield fp


def main() -> int:
    print("🔍 Validando referências...")
    print(f"   Bibliografia: {BIB_FILE}")
    print()

    if not BIB_FILE.exists():
        print(f"❌ Bibliografia não encontrada: {BIB_FILE}", file=sys.stderr)
        return 2

    # Extrair IDs da bibliografia
    bib_text = BIB_FILE.read_text(encoding="utf-8")
    bib_ids = set(BIB_ID_RE.findall(bib_text))

    if not bib_ids:
        print("⚠️  Nenhum ID encontrado na bibliografia (verifique o formato)", file=sys.stderr)
        return 2

    # Extrair IDs usados no texto
    used_ids: set[str] = set()
    used_by_file: dict[str, set[str]] = {}

    for fp in iter_md_files():
        text = fp.read_text(encoding="utf-8")
        ids = set(REF_IN_TEXT_RE.findall(text))
        if ids:
            used_ids |= ids
            used_by_file[fp.name] = ids

    # Verificar IDs faltantes
    missing = sorted(used_ids - bib_ids)
    unused = sorted(bib_ids - used_ids)

    if missing:
        print("❌ IDs usados no texto mas AUSENTES na bibliografia:\n", file=sys.stderr)
        for mid in missing:
            print(f"   • {mid}", file=sys.stderr)
            # Mostrar onde aparece
            for fname, ids in used_by_file.items():
                if mid in ids:
                    print(f"       └─ {fname}", file=sys.stderr)
        print()
        return 1

    print(f"✅ Todas as {len(used_ids)} referências usadas existem na bibliografia!")

    # Opcional: avisar IDs não usados (não falha)
    if unused:
        print(f"\n⚠️  {len(unused)} ID(s) na bibliografia mas NÃO usados (ok, só higiene):")
        for uid in unused:
            print(f"   • {uid}")

    print(f"\n📊 Resumo: {len(used_ids)} usados | {len(bib_ids)} definidos | {len(unused)} não usados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
