#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de manuscrito — "Gate" para build verde.

Falha (exit 1) se:
- Existir [[MOVE:CAP-XX]] (placeholder)
- Existir [[MOVE:CAP-NN]] onde NN não existe como arquivo
- Existir [[MOVE: com espaço antes do CAP

Uso:
    python3 tools/validate_manuscript.py
    # ou integrar no CI/pre-commit
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

# Arquivos ignorados (índices gerados)
SKIP_FILES = {
    "MOVE_MAP.md",
    "00_SUMARIO_MESTRE.md",
    "00_MAPA_DE_LINKS_MOVE.md",
    "00_BACKLOG_ARTE.md",
    "00_BACKLOG_REFERENCIAS.md",
}

# Regex para detectar MOVE
MOVE_RE = re.compile(r"\[\[MOVE:\s*CAP-(\d+|XX)\s*\]\]", re.IGNORECASE)
MOVE_SPACE_RE = re.compile(r"\[\[MOVE:\s+CAP-", re.IGNORECASE)  # espaço após :
FILE_CAP_RE = re.compile(r"^(\d+)[-_].+\.md$", re.IGNORECASE)


def get_cap_from_filename(name: str) -> str | None:
    m = FILE_CAP_RE.match(name)
    return m.group(1).zfill(2) if m else None


def validate() -> Tuple[bool, List[str]]:
    """Retorna (sucesso, lista de erros)."""
    errors: List[str] = []

    # Mapear CAPs existentes
    existing_caps = set()
    md_files = [p for p in CONTENT.glob("*.md") if p.name not in SKIP_FILES]

    for p in md_files:
        cap = get_cap_from_filename(p.name)
        if cap:
            existing_caps.add(cap)

    # Validar cada arquivo
    for p in md_files:
        text = p.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")

        for i, line in enumerate(lines, 1):
            # Verificar MOVE com espaço
            if MOVE_SPACE_RE.search(line):
                errors.append(f"❌ MOVE com espaço: {p.name}:{i}")

            # Verificar todos os MOVE
            for m in MOVE_RE.finditer(line):
                cap_target = m.group(1)

                if cap_target.upper() == "XX":
                    errors.append(f"❌ Placeholder CAP-XX: {p.name}:{i}")
                else:
                    cap_padded = cap_target.zfill(2)
                    if cap_padded not in existing_caps:
                        errors.append(
                            f"❌ CAP inexistente: {p.name}:{i} → CAP-{cap_padded}"
                        )

    return len(errors) == 0, errors


def main() -> int:
    print("🔍 Validando manuscrito...")
    print(f"   Diretório: {CONTENT}")
    print()

    ok, errors = validate()

    if ok:
        print("✅ Manuscrito válido — nenhum MOVE quebrado!")
        return 0
    else:
        print(f"❌ {len(errors)} erro(s) encontrado(s):\n")
        for err in errors:
            print(f"   {err}")
        print()
        print("💡 Corrija os erros acima antes de prosseguir.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
