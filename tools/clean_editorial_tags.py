#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpeza editorial profunda do manuscrito.

Converte tags internas para formato publicável:
- [[BOX: Título]]...[[/BOX]] → blockquote formatado
- [[KEEP]]...[[/KEEP]] → remove tags, mantém conteúdo
- [[MOVE:CAP-XX]] → remove marcador, mantém conteúdo
- "Figura sugerida:" → remove ou move para backlog

Uso:
    python3 tools/clean_editorial_tags.py
    python3 tools/clean_editorial_tags.py --report  # apenas relatório
    python3 tools/clean_editorial_tags.py --dry-run # mostra mudanças sem aplicar
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import List, Tuple

from _config import CONTENT_DIR, BOX_MAPPING


@dataclass
class EditorialIssue:
    """Representa um problema editorial encontrado."""
    file: str
    line: int
    issue_type: str
    content: str
    suggestion: str


def normalize_box_title(title: str) -> str:
    """Normaliza título do BOX para formato de saída."""
    title_lower = title.lower().strip()
    for key, value in BOX_MAPPING.items():
        if key in title_lower or title_lower in key:
            return value
    # Se não encontrou mapeamento, usa o título original em maiúsculas
    return title.upper() if title else "NOTA CLÍNICA"


def convert_box_to_blockquote(match: re.Match) -> str:
    """Converte [[BOX: Título]]...[[/BOX]] para blockquote."""
    title = match.group(1).strip() if match.group(1) else ""
    content = match.group(2).strip()
    
    normalized_title = normalize_box_title(title)
    
    # Formatar cada linha do conteúdo como blockquote
    lines = content.split('\n')
    formatted_lines = []
    formatted_lines.append(f"> **{normalized_title}**")
    formatted_lines.append(">")
    for line in lines:
        line = line.strip()
        if line:
            formatted_lines.append(f"> {line}")
    
    return '\n'.join(formatted_lines)


def clean_file_content(text: str) -> Tuple[str, List[str]]:
    """
    Limpa conteúdo de um arquivo aplicando transformações editoriais.
    
    Retorna: (texto_limpo, lista_de_mudanças)
    """
    changes = []
    result = text
    
    # 1. Converter BOX com título para blockquote
    # Limite de 10000 chars para prevenir ReDoS em input malformado
    box_pattern = re.compile(
        r'\[\[BOX(?::\s*([^\]]*))?\]\]\s*\n?([\s\S]{0,10000}?)\s*\[\[/BOX\]\]',
        re.IGNORECASE
    )
    
    box_matches = list(box_pattern.finditer(result))
    if box_matches:
        changes.append(f"  → Convertidos {len(box_matches)} boxes para blockquote")
        result = box_pattern.sub(convert_box_to_blockquote, result)
    
    # 2. Remover [[KEEP]] e [[/KEEP]] (manter conteúdo)
    keep_pattern = re.compile(r'\[\[/?KEEP\]\]\s*\n?', re.IGNORECASE)
    keep_matches = list(keep_pattern.finditer(result))
    if keep_matches:
        changes.append(f"  → Removidas {len(keep_matches)} tags KEEP")
        result = keep_pattern.sub('', result)
    
    # 3. Remover [[MOVE:CAP-XX]] e [[/MOVE:CAP-XX]] (manter conteúdo)
    move_pattern = re.compile(r'\[\[/?MOVE:CAP-\d+\]\]\s*\n?', re.IGNORECASE)
    move_matches = list(move_pattern.finditer(result))
    if move_matches:
        changes.append(f"  → Removidas {len(move_matches)} tags MOVE")
        result = move_pattern.sub('', result)
    
    # 4. Remover [[TODO:...]] (linha inteira em release)
    todo_pattern = re.compile(r'^\s*\[\[TODO:[^\]]*\]\]\s*$\n?', re.MULTILINE | re.IGNORECASE)
    todo_matches = list(todo_pattern.finditer(result))
    if todo_matches:
        changes.append(f"  → Removidas {len(todo_matches)} tags TODO")
        result = todo_pattern.sub('', result)
    
    # 5. Remover [[DELETE]]...[[/DELETE]] (remove tudo)
    # Limite de 10000 chars para prevenir ReDoS
    delete_pattern = re.compile(r'\[\[DELETE\]\][\s\S]{0,10000}?\[\[/DELETE\]\]\s*\n?', re.IGNORECASE)
    delete_matches = list(delete_pattern.finditer(result))
    if delete_matches:
        changes.append(f"  → Removidos {len(delete_matches)} blocos DELETE")
        result = delete_pattern.sub('', result)
    
    # 6. Remover "Figura sugerida:" (opcional, movido para backlog)
    figura_pattern = re.compile(
        r'^\s*>\s*\*?\*?Figura sugerida[:\*]*.*$\n?',
        re.MULTILINE | re.IGNORECASE
    )
    figura_matches = list(figura_pattern.finditer(result))
    if figura_matches:
        changes.append(f"  → Removidas {len(figura_matches)} linhas 'Figura sugerida'")
        result = figura_pattern.sub('', result)
    
    # 7. Limpar linhas vazias excessivas
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    
    # 8. Limpar espaços no final das linhas
    result = re.sub(r' +$', '', result, flags=re.MULTILINE)
    
    return result, changes


def analyze_file(filepath: Path) -> List[EditorialIssue]:
    """Analisa um arquivo e retorna lista de problemas editoriais."""
    issues = []
    text = filepath.read_text(encoding='utf-8')
    lines = text.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Verificar tags que deveriam ter sido limpas
        if '[[KEEP]]' in line or '[[/KEEP]]' in line:
            issues.append(EditorialIssue(
                file=filepath.name,
                line=i,
                issue_type="TAG_KEEP",
                content=line[:80],
                suggestion="Remover tag, manter conteúdo"
            ))
        
        if '[[BOX' in line and '> **' not in line:
            issues.append(EditorialIssue(
                file=filepath.name,
                line=i,
                issue_type="TAG_BOX",
                content=line[:80],
                suggestion="Converter para blockquote"
            ))
        
        if '[[MOVE:' in line or '[[/MOVE:' in line:
            issues.append(EditorialIssue(
                file=filepath.name,
                line=i,
                issue_type="TAG_MOVE",
                content=line[:80],
                suggestion="Remover marcador, manter conteúdo"
            ))
        
        if 'Figura sugerida' in line.lower():
            issues.append(EditorialIssue(
                file=filepath.name,
                line=i,
                issue_type="PLACEHOLDER_FIGURA",
                content=line[:80],
                suggestion="Substituir por figura real ou remover"
            ))
        
        # Verificar negrito excessivo (mais de 50 caracteres em negrito)
        bold_pattern = re.compile(r'\*\*[^*]{50,}\*\*')
        if bold_pattern.search(line):
            issues.append(EditorialIssue(
                file=filepath.name,
                line=i,
                issue_type="BOLD_EXCESSIVE",
                content=line[:80],
                suggestion="Reduzir negrito para termos-chave apenas"
            ))
    
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Limpeza editorial profunda do manuscrito"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Apenas gera relatório de problemas, sem modificar arquivos"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra mudanças que seriam feitas, sem aplicar"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Processa apenas um arquivo específico"
    )
    args = parser.parse_args()
    
    print("🔍 Limpeza Editorial — The Art of Eyelid Surgery")
    print(f"   Diretório: {CONTENT_DIR}")
    print()
    
    # Encontrar arquivos de capítulos
    if args.file:
        files = [CONTENT_DIR / args.file]
    else:
        files = sorted(CONTENT_DIR.glob("[0-9]*.md"))
    
    if not files:
        print("❌ Nenhum arquivo de capítulo encontrado")
        return 1
    
    print(f"   Arquivos: {len(files)}")
    print()
    
    # Modo relatório: apenas lista problemas
    if args.report:
        print("📋 RELATÓRIO DE PROBLEMAS EDITORIAIS")
        print("=" * 60)
        
        total_issues = 0
        for fp in files:
            issues = analyze_file(fp)
            if issues:
                print(f"\n📄 {fp.name}")
                for issue in issues:
                    print(f"   L{issue.line:4d} [{issue.issue_type}] {issue.suggestion}")
                    total_issues += 1
        
        print()
        print("=" * 60)
        print(f"Total: {total_issues} problemas encontrados")
        return 0 if total_issues == 0 else 1
    
    # Modo limpeza
    print("🧹 APLICANDO LIMPEZA EDITORIAL")
    print("=" * 60)
    
    total_changes = 0
    for fp in files:
        text = fp.read_text(encoding='utf-8')
        cleaned, changes = clean_file_content(text)
        
        if changes:
            print(f"\n📄 {fp.name}")
            for change in changes:
                print(change)
            total_changes += len(changes)
            
            if not args.dry_run:
                fp.write_text(cleaned, encoding='utf-8')
    
    print()
    print("=" * 60)
    
    if args.dry_run:
        print(f"🔄 DRY RUN: {total_changes} mudanças seriam aplicadas")
    else:
        print(f"✅ {total_changes} mudanças aplicadas")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
