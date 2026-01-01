#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

MOVE_RE = re.compile(r"\[\[MOVE:\s*CAP-(\d+|XX)\s*\]\]", re.IGNORECASE)
REF_RE = re.compile(r"\[\[REF\]\]", re.IGNORECASE)
FIG_RE = re.compile(r"\*\*Figura sugerida[:\*]*|FIG-\d+", re.IGNORECASE)

# Pega o primeiro H1 do arquivo como "título do capítulo"
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

# Heurística: capítulo é o prefixo numérico do filename (ex: 24-....md)
FILE_CAP_RE = re.compile(r"^(\d+)[-_].+\.md$", re.IGNORECASE)


@dataclass
class MoveHit:
    file: str
    line: int
    cap_target: str   # "08", "XX", etc.
    raw: str


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def line_number_from_pos(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def cap_from_filename(name: str) -> str | None:
    m = FILE_CAP_RE.match(name)
    if not m:
        return None
    return m.group(1).zfill(2)


def title_from_md(text: str, fallback: str) -> str:
    m = H1_RE.search(text)
    return m.group(1).strip() if m else fallback


SKIP_FILES = {"MOVE_MAP.md", "00_SUMARIO_MESTRE.md", "00_MAPA_DE_LINKS_MOVE.md", "00_BACKLOG_ARTE.md", "00_BACKLOG_REFERENCIAS.md", "00_MANUSCRITO.md"}


def main() -> None:
    md_files = sorted([p for p in CONTENT.glob("*.md") if p.name not in SKIP_FILES])

    # Map: CAP -> (file, title)
    cap_index: Dict[str, Tuple[str, str]] = {}

    for p in md_files:
        txt = read_text(p)
        cap = cap_from_filename(p.name)
        if cap:
            cap_index[cap] = (p.name, title_from_md(txt, p.stem))

    # Collect MOVE / REF / FIG hits
    moves: List[MoveHit] = []
    refs: List[Tuple[str, int, str]] = []
    figs: List[Tuple[str, int, str]] = []

    for p in md_files:
        if not p.exists():
            continue
        txt = read_text(p)

        for m in MOVE_RE.finditer(txt):
            line = line_number_from_pos(txt, m.start())
            cap_target = m.group(1)
            moves.append(MoveHit(p.name, line, cap_target, m.group(0)))

        for m in REF_RE.finditer(txt):
            line = line_number_from_pos(txt, m.start())
            refs.append((p.name, line, "REF"))

        for m in FIG_RE.finditer(txt):
            line = line_number_from_pos(txt, m.start())
            figs.append((p.name, line, "Figura sugerida"))

    # Build SUMÁRIO mestre (ordenado por CAP)
    sumario_lines: List[str] = []
    sumario_lines.append("# SUMÁRIO MESTRE\n")
    sumario_lines.append("> Índice gerado automaticamente a partir de `content/*.md`.\n")

    for cap in sorted(cap_index.keys()):
        fn, title = cap_index[cap]
        # Link relativo simples (GitHub/Obsidian-friendly)
        sumario_lines.append(f"- **CAP-{cap}** — [{title}](./{fn})")

    sumario_lines.append("")

    # Build MOVE MAP
    move_lines: List[str] = []
    move_lines.append("# MAPA DE LINKS — MOVE\n")
    move_lines.append("> Lista de `[[MOVE:CAP-..]]` encontrados, com resolução para arquivo quando existir.\n")

    ok, broken = 0, 0

    for hit in sorted(moves, key=lambda x: (x.cap_target, x.file, x.line)):
        if hit.cap_target == "XX":
            status = "❌ CAP-XX (placeholder)"
            broken += 1
            move_lines.append(f"- {status} — `{hit.file}:{hit.line}` → `{hit.raw}`")
            continue

        cap = hit.cap_target.zfill(2)
        if cap in cap_index:
            dest_file, dest_title = cap_index[cap]
            status = "✅"
            ok += 1
            move_lines.append(
                f"- {status} `{hit.file}:{hit.line}` → **CAP-{cap}** "
                f"[{dest_title}](./{dest_file})"
            )
        else:
            status = "⚠️ CAP sem arquivo"
            broken += 1
            move_lines.append(f"- {status} — `{hit.file}:{hit.line}` → `CAP-{cap}` (não encontrado em filenames)")

    move_lines.append("")
    move_lines.append(f"**Resumo:** {ok} resolvidos • {broken} pendentes/quebrados\n")

    # Backlog Arte
    art_lines: List[str] = []
    art_lines.append("# BACKLOG DE ARTE — FIGURAS SUGERIDAS\n")
    for f, line, _ in figs:
        art_lines.append(f"- `{f}:{line}` — Figura sugerida")
    art_lines.append("")

    # Backlog Referências
    ref_lines: List[str] = []
    ref_lines.append("# BACKLOG DE REFERÊNCIAS — [[REF]]\n")
    # Contagem por arquivo
    counts: Dict[str, int] = {}
    for f, _, _ in refs:
        counts[f] = counts.get(f, 0) + 1
    for f in sorted(counts.keys()):
        ref_lines.append(f"- `{f}` — {counts[f]} ocorrência(s) de `[[REF]]`")
    ref_lines.append("")

    # Write outputs
    (CONTENT / "00_SUMARIO_MESTRE.md").write_text("\n".join(sumario_lines), encoding="utf-8")
    (CONTENT / "00_MAPA_DE_LINKS_MOVE.md").write_text("\n".join(move_lines), encoding="utf-8")
    (CONTENT / "00_BACKLOG_ARTE.md").write_text("\n".join(art_lines), encoding="utf-8")
    (CONTENT / "00_BACKLOG_REFERENCIAS.md").write_text("\n".join(ref_lines), encoding="utf-8")

    print("OK: gerados:")
    print("- content/00_SUMARIO_MESTRE.md")
    print("- content/00_MAPA_DE_LINKS_MOVE.md")
    print("- content/00_BACKLOG_ARTE.md")
    print("- content/00_BACKLOG_REFERENCIAS.md")


if __name__ == "__main__":
    main()
