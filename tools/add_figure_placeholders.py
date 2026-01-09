#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona [[FIGURE]] placeholder após o primeiro H1 de cada capítulo.
"""

from pathlib import Path
import re

from _utils import atomic_write

CONTENT = Path(__file__).resolve().parents[1] / "content"

added = 0
for md in sorted(CONTENT.glob("[0-9][0-9]-*.md")):
    txt = md.read_text(encoding="utf-8")

    # já tem imagem inserida? pula
    if re.search(r'!\[Figura\s+\d{2}\.', txt):
        print(f"⏭️  já tem figura: {md.name}")
        continue

    # já tem marcador? pula
    if "[[FIGURE]]" in txt:
        print(f"⏭️  já tem placeholder: {md.name}")
        continue

    # insere após o primeiro título "# "
    lines = txt.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(i + 1, "")
            lines.insert(i + 2, "[[FIGURE]]")
            lines.insert(i + 3, "")
            atomic_write(md, "\n".join(lines) + "\n")
            print(f"✅ placeholder adicionado: {md.name}")
            added += 1
            break

print(f"\n📊 Total: {added} placeholders adicionados")
