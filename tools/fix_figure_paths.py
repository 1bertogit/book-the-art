#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige paths de figuras no manuscrito para usar caminhos absolutos.

Usa o figures.yml como fonte da verdade para nomes de arquivos.

Uso:
    python3 tools/fix_figure_paths.py
"""

from __future__ import annotations

import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "projects" / "eyelid-surgery"
CONTENT_DIR = PROJECT_DIR / "content"
FIGURES_DIR = PROJECT_DIR / "assets" / "figures"
FIGURES_YAML = PROJECT_DIR / "figures.yml"
DIST_DIR = ROOT / "dist"
MANUSCRITO_LIMPO = DIST_DIR / "manuscrito_limpo.md"

# Regex para encontrar chamadas de figura: ![Texto](path)
FIGURE_RE = re.compile(
    r'!\[([^\]]*)\]\(([^)]+)\)',
    re.MULTILINE
)


def load_figures_yaml() -> dict:
    """Carrega o arquivo figures.yml."""
    if not FIGURES_YAML.exists():
        return {}
    with open(FIGURES_YAML, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('figures', {}) if data else {}


def get_figure_id_from_alt(alt_text: str) -> str | None:
    """Extrai o ID da figura do alt text (ex: 'Figura 01.1 — ...' → 'FIG-01-01')."""
    match = re.search(r'(?:Figura|FIG)[- ]?(\d+)[.\-](\d+)', alt_text, re.IGNORECASE)
    if match:
        chapter = match.group(1).zfill(2)
        seq = match.group(2).zfill(2)
        return f"FIG-{chapter}-{seq}"
    return None


def fix_figure_path(match: re.Match, figures: dict, figures_dir: Path) -> str:
    """Corrige o path de uma figura."""
    alt_text = match.group(1)
    old_path = match.group(2)
    
    # Tentar extrair ID da figura
    fig_id = get_figure_id_from_alt(alt_text)
    
    if fig_id and fig_id in figures:
        # Usar nome de arquivo do YAML
        filename = figures[fig_id].get('filename')
        if filename:
            abs_path = figures_dir / filename
            if abs_path.exists():
                return f"![{alt_text}]({abs_path})"
    
    # Fallback: tentar corrigir path relativo
    if 'assets/figures/' in old_path:
        filename = old_path.split('/')[-1]
        abs_path = figures_dir / filename
        if abs_path.exists():
            return f"![{alt_text}]({abs_path})"
        
        # Tentar encontrar arquivo similar
        for existing_file in figures_dir.glob('*.png'):
            if fig_id and fig_id.replace('-', '_').lower() in existing_file.name.lower():
                return f"![{alt_text}]({existing_file})"
            if fig_id and fig_id.lower() in existing_file.name.lower():
                return f"![{alt_text}]({existing_file})"
    
    # Não conseguiu corrigir, retorna original
    return match.group(0)


def main() -> int:
    print("🔧 Corrigindo paths de figuras...")
    print(f"   Manuscrito: {MANUSCRITO_LIMPO}")
    print(f"   Figuras: {FIGURES_DIR}")
    print()
    
    if not MANUSCRITO_LIMPO.exists():
        print("❌ Manuscrito não encontrado. Execute 'make export' primeiro.")
        return 1
    
    figures = load_figures_yaml()
    print(f"   figures.yml: {len(figures)} figuras declaradas")
    
    # Ler manuscrito
    text = MANUSCRITO_LIMPO.read_text(encoding='utf-8')
    
    # Contar figuras antes
    matches_before = list(FIGURE_RE.finditer(text))
    print(f"   Figuras no texto: {len(matches_before)}")
    print()
    
    # Corrigir paths
    fixed_count = 0
    
    def replacer(match):
        nonlocal fixed_count
        old = match.group(0)
        new = fix_figure_path(match, figures, FIGURES_DIR)
        if old != new:
            fixed_count += 1
        return new
    
    new_text = FIGURE_RE.sub(replacer, text)
    
    # Salvar
    MANUSCRITO_LIMPO.write_text(new_text, encoding='utf-8')
    
    print(f"✅ {fixed_count} paths corrigidos")
    print(f"   Salvo em: {MANUSCRITO_LIMPO}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
