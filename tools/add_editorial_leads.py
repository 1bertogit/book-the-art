#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona leads editoriais após figuras principais.

Extrai pontos-chave da seção "Objetivo do capítulo" e insere um blockquote
de "Leitura guiada" logo após a figura principal de cada capítulo.

Uso:
    python3 tools/add_editorial_leads.py --dry-run   # Preview
    python3 tools/add_editorial_leads.py --apply     # Aplicar
"""

from __future__ import annotations

import argparse
import re

from _config import CONTENT_DIR


def extract_objectives(text: str) -> list[str]:
    """Extrai pontos-chave da seção 'Objetivo do capítulo'."""
    # Encontrar seção de objetivo
    objetivo_match = re.search(
        r'##\s*Objetivo\s+do\s+cap[ií]tulo\s*\n(.*?)(?=\n##|\Z)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    if not objetivo_match:
        return []

    section = objetivo_match.group(1).strip()

    # Extrair bullets ou frases
    objectives = []

    # Primeiro tentar extrair de bullets
    bullets = re.findall(r'^[-*]\s*(.+)$', section, re.MULTILINE)
    if bullets:
        objectives = [b.strip() for b in bullets[:3]]
    else:
        # Se não houver bullets, pegar primeira frase significativa
        sentences = re.split(r'[.!?]\s+', section)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 20 and len(sent) < 150:
                objectives.append(sent)
                if len(objectives) >= 2:
                    break

    return objectives


def generate_lead(objectives: list[str]) -> str:
    """Gera o bloco de leitura guiada."""
    if not objectives:
        return ""

    # Limpar objetivos
    clean_objectives = []
    for obj in objectives:
        # Remover negrito
        obj = re.sub(r'\*\*(.+?)\*\*', r'\1', obj)
        # Remover pontuação final
        obj = obj.rstrip('.,;:')
        # Primeira letra minúscula para fluidez
        if obj and obj[0].isupper():
            obj = obj[0].lower() + obj[1:]
        clean_objectives.append(obj)

    if len(clean_objectives) == 1:
        lead = f"> **Leitura guiada:** este capítulo aborda {clean_objectives[0]}."
    elif len(clean_objectives) == 2:
        lead = (
            f"> **Leitura guiada:** este capítulo aborda {clean_objectives[0]}, "
            f"com foco em {clean_objectives[1]}."
        )
    else:
        lead = (
            f"> **Leitura guiada:** este capítulo aborda {clean_objectives[0]}, "
            f"com foco em {clean_objectives[1]}. "
            f"O ponto crítico é {clean_objectives[2]}."
        )

    return lead


def has_lead_already(text: str) -> bool:
    """Verifica se já existe um lead editorial."""
    return bool(re.search(r'>\s*\*\*Leitura guiada', text, re.IGNORECASE))


def find_figure_block(text: str) -> tuple[int, int] | None:
    """Encontra a posição do bloco de figura principal."""
    # Procurar por figura com formato: ![Figura XX.1
    match = re.search(r'!\[Figura\s+\d+\.1[^\]]*\]\([^)]+\)', text)
    if match:
        # Encontrar fim da linha da figura
        end = text.find('\n', match.end())
        if end == -1:
            end = len(text)
        return match.start(), end

    return None


def process_file(filepath: Path, dry_run: bool = True) -> dict:
    """Processa um arquivo e adiciona lead editorial."""
    text = filepath.read_text(encoding="utf-8")

    stats = {
        "file": filepath.name,
        "has_figure": False,
        "has_lead": False,
        "added": False,
        "lead": ""
    }

    # Verificar se já tem lead
    if has_lead_already(text):
        stats["has_lead"] = True
        return stats

    # Encontrar figura
    fig_pos = find_figure_block(text)
    if not fig_pos:
        return stats

    stats["has_figure"] = True

    # Extrair objetivos
    objectives = extract_objectives(text)
    if not objectives:
        return stats

    # Gerar lead
    lead = generate_lead(objectives)
    if not lead:
        return stats

    stats["lead"] = lead

    if not dry_run:
        # Inserir lead após a figura
        fig_start, fig_end = fig_pos
        # Encontrar próxima linha não vazia após a figura
        insert_pos = fig_end

        # Adicionar duas linhas em branco + lead + duas linhas em branco
        new_text = (
            text[:insert_pos] +
            "\n\n" + lead + "\n\n" +
            text[insert_pos:].lstrip('\n')
        )

        filepath.write_text(new_text, encoding="utf-8")
        stats["added"] = True

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Adiciona leads editoriais após figuras principais"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostrar mudanças sem aplicar"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplicar mudanças nos arquivos"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Processar apenas um arquivo específico"
    )
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Especifique --dry-run ou --apply")
        return 1

    print("📖 Adicionando leads editoriais...")
    print()

    if args.file:
        files = [Path(args.file)]
    else:
        files = sorted(CONTENT_DIR.glob("[0-9][0-9]-*.md"))

    added = 0
    skipped_no_fig = 0
    skipped_has_lead = 0

    for filepath in files:
        stats = process_file(filepath, dry_run=args.dry_run)

        if stats["has_lead"]:
            print(f"  ⏭️  {stats['file']}: já tem lead")
            skipped_has_lead += 1
        elif not stats["has_figure"]:
            print(f"  ⚠️  {stats['file']}: sem figura principal")
            skipped_no_fig += 1
        elif stats["lead"]:
            icon = "📄" if args.dry_run else "✅"
            print(f"  {icon} {stats['file']}")
            if args.dry_run:
                print(f"      {stats['lead'][:80]}...")
            added += 1

    print()
    print("="*50)
    print("📊 RESUMO")
    print("="*50)
    print(f"   Leads {'a adicionar' if args.dry_run else 'adicionados'}: {added}")
    print(f"   Já tinham lead: {skipped_has_lead}")
    print(f"   Sem figura principal: {skipped_no_fig}")
    print()

    if args.dry_run:
        print("💡 Execute com --apply para aplicar as mudanças")
    else:
        print("✅ Leads adicionados!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
