from pathlib import Path

CONTENT = Path("content")
FIGURES = Path("assets/figures")

for md in sorted(CONTENT.glob("[0-9][0-9]-*.md")):
    cap = md.name[:2]

    figure = next(FIGURES.glob(f"FIG-{cap}-01_*.png"), None)
    if not figure:
        print(f"⚠️ Figura não encontrada para capítulo {cap}")
        continue

    text = md.read_text(encoding="utf-8")

    if "[[FIGURE]]" not in text:
        print(f"⚠️ Marcador [[FIGURE]] ausente em {md.name}")
        continue

    block = (
        f"![Figura {cap}.1 — Ilustração principal do capítulo]"
        f"(assets/figures/{figure.name})\n"
    )

    md.write_text(text.replace("[[FIGURE]]", block), encoding="utf-8")
    print(f"✅ Figura inserida no capítulo {cap}")
