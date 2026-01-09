#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insere figuras nos capítulos usando formato editorial correto para Pandoc.

O formato gerado permite:
- Renderização como <figure> em HTML/EPUB
- Numeração automática
- Referência cruzada via @fig:XX-YY

Uso:
    python3 tools/insert_figures.py
"""

import re

from _config import CONTENT_DIR as CONTENT, FIGURES_DIR as FIGURES
from _utils import atomic_write


def get_figure_caption(cap: str, idx: int, filename: str) -> str:
    """Gera legenda descritiva baseada no nome do arquivo."""
    # Extrai parte descritiva do nome: FIG-01-01_filosofia.png → filosofia
    match = re.search(r'FIG-\d+-\d+_(.+)\.\w+$', filename)
    if match:
        desc = match.group(1).replace('_', ' ').replace('-', ' ')
        desc = desc.capitalize()
        return f"Figura {cap}.{idx} — {desc}"
    return f"Figura {cap}.{idx} — Ilustração do capítulo"


def main():
    print("🖼️  Inserindo figuras nos capítulos...")
    print()

    inserted = 0
    skipped = 0

    for md in sorted(CONTENT.glob("[0-9][0-9]-*.md")):
        cap = md.name[:2]

        # Buscar figura principal do capítulo
        figure = next(FIGURES.glob(f"FIG-{cap}-01_*.png"), None)
        if not figure:
            print(f"⚠️  Figura não encontrada para capítulo {cap}")
            skipped += 1
            continue

        text = md.read_text(encoding="utf-8")

        if "[[FIGURE]]" not in text:
            print(f"⚠️  Marcador [[FIGURE]] ausente em {md.name}")
            skipped += 1
            continue

        # Gerar bloco de figura editorial
        caption = get_figure_caption(cap, 1, figure.name)
        fig_id = f"fig:{cap}-01"

        # Formato Pandoc com atributo de referência cruzada
        block = (
            f"\n"
            f"![{caption}](assets/figures/{figure.name}){{#{fig_id}}}\n"
            f"\n"
        )

        atomic_write(md, text.replace("[[FIGURE]]", block))
        print(f"✅ Figura inserida: {md.name} → {figure.name}")
        inserted += 1

    print()
    print(f"📊 Resultado: {inserted} inseridas, {skipped} ignoradas")


if __name__ == "__main__":
    main()
