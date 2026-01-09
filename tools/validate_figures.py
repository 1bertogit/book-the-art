#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida figuras: compara figures.yml, arquivos existentes e chamadas no texto.

Uso:
    python3 tools/validate_figures.py           # Relatório completo
    python3 tools/validate_figures.py --strict  # Falha se houver inconsistências
"""

from __future__ import annotations

import argparse
import re
from typing import Dict, List, Set, Tuple
import yaml

from _config import (
    CONTENT_DIR,
    FIGURES_DIR,
    FIGURES_YAML,
)

# Regex para encontrar chamadas de figura no Markdown
# Padrão: ![Figura XX.Y — Legenda](caminho)
FIGURE_CALL_RE = re.compile(
    r'!\[(?:FIG-|Figura\s*)(\d+)[\.-](\d+)[^\]]*\]\(([^)]+)\)',
    re.IGNORECASE
)

# Padrão alternativo: ![FIG-XX-YY: Legenda](caminho)
FIG_ID_RE = re.compile(r'FIG-(\d+)-(\d+)', re.IGNORECASE)


def load_figures_yaml() -> Dict:
    """Carrega o arquivo figures.yml."""
    if not FIGURES_YAML.exists():
        return {}
    with open(FIGURES_YAML, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('figures', {}) if data else {}


def get_existing_files() -> Set[str]:
    """Lista arquivos de figura existentes."""
    if not FIGURES_DIR.exists():
        return set()
    return {f.name for f in FIGURES_DIR.glob('*.png')}


def get_calls_in_text() -> List[Tuple[str, str, int, str]]:
    """
    Encontra todas as chamadas de figura no texto.
    Retorna: [(figura_id, arquivo_origem, linha, legenda)]
    """
    calls = []
    
    for md_file in sorted(CONTENT_DIR.glob('[0-9]*.md')):
        text = md_file.read_text(encoding='utf-8')
        lines = text.split('\n')
        
        for i, line in enumerate(lines, 1):
            for match in FIGURE_CALL_RE.finditer(line):
                chapter = match.group(1).zfill(2)
                seq = match.group(2).zfill(2)
                fig_id = f"FIG-{chapter}-{seq}"
                path = match.group(3)
                calls.append((fig_id, md_file.name, i, path))
    
    return calls


def validate() -> Tuple[int, int, int]:
    """
    Executa validação completa.
    Retorna: (erros, avisos, ok)
    """
    errors = 0
    warnings = 0
    ok_count = 0
    
    print("🔍 Validação de Figuras — The Art of Eyelid Surgery")
    print("=" * 60)
    print()
    
    # 1. Carregar dados
    yaml_figures = load_figures_yaml()
    existing_files = get_existing_files()
    text_calls = get_calls_in_text()
    
    print(f"📄 figures.yml: {len(yaml_figures)} figuras declaradas")
    print(f"📁 assets/figures/: {len(existing_files)} arquivos PNG")
    print(f"📝 Chamadas no texto: {len(text_calls)} referências")
    print()
    
    # 2. Verificar figuras declaradas vs arquivos
    print("📋 VERIFICAÇÃO: YAML vs Arquivos")
    print("-" * 40)
    
    yaml_filenames = {fig.get('filename') for fig in yaml_figures.values() if fig.get('filename')}
    
    # Arquivos declarados mas não existem
    missing_files = yaml_filenames - existing_files
    if missing_files:
        print("❌ Declaradas no YAML mas NÃO existem:")
        for f in sorted(missing_files):
            print(f"   • {f}")
            errors += 1
    else:
        print("✅ Todas as figuras declaradas existem")
        ok_count += 1
    
    # Arquivos existem mas não declarados
    extra_files = existing_files - yaml_filenames - {'.DS_Store', 'CAPA_ebook_principal.png'}
    if extra_files:
        print("⚠️  Existem mas NÃO declaradas no YAML:")
        for f in sorted(extra_files):
            print(f"   • {f}")
            warnings += 1
    
    print()
    
    # 3. Verificar chamadas no texto vs YAML
    print("📋 VERIFICAÇÃO: Texto vs YAML")
    print("-" * 40)
    
    text_fig_ids = {call[0] for call in text_calls}
    yaml_fig_ids = set(yaml_figures.keys())
    
    # Chamadas sem declaração
    undeclared = text_fig_ids - yaml_fig_ids
    if undeclared:
        print("❌ Chamadas no texto SEM declaração no YAML:")
        for fig_id in sorted(undeclared):
            calls = [c for c in text_calls if c[0] == fig_id]
            for _, file, line, _ in calls:
                print(f"   • {fig_id} em {file}:{line}")
            errors += 1
    else:
        print("✅ Todas as chamadas estão declaradas no YAML")
        ok_count += 1
    
    # Declaradas sem chamada no texto
    unused = yaml_fig_ids - text_fig_ids
    if unused:
        print("⚠️  Declaradas no YAML mas SEM chamada no texto:")
        for fig_id in sorted(unused):
            print(f"   • {fig_id}")
            warnings += 1
    
    print()
    
    # 4. Estatísticas por prioridade
    print("📊 ESTATÍSTICAS")
    print("-" * 40)
    
    priorities = {'P0': 0, 'P1': 0, 'P2': 0}
    statuses = {'final': 0, 'review': 0, 'draft': 0}
    
    for fig_id, fig in yaml_figures.items():
        p = fig.get('priority', 'P1')
        s = fig.get('status', 'draft')
        priorities[p] = priorities.get(p, 0) + 1
        statuses[s] = statuses.get(s, 0) + 1
    
    print(f"   Prioridade:")
    print(f"     P0 (críticas):     {priorities.get('P0', 0)}")
    print(f"     P1 (importantes):  {priorities.get('P1', 0)}")
    print(f"     P2 (complementar): {priorities.get('P2', 0)}")
    print()
    print(f"   Status:")
    print(f"     final:  {statuses.get('final', 0)}")
    print(f"     review: {statuses.get('review', 0)}")
    print(f"     draft:  {statuses.get('draft', 0)}")
    
    print()
    print("=" * 60)
    print(f"Resumo: {errors} erros | {warnings} avisos | {ok_count} checks OK")
    print()
    
    return errors, warnings, ok_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida figuras do livro")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Falha (exit 1) se houver qualquer erro"
    )
    args = parser.parse_args()
    
    errors, warnings, _ = validate()
    
    if args.strict and errors > 0:
        return 1
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
