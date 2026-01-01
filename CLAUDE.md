# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Medical textbook manuscript scaffold for "The Art of Eyelid Surgery" (cirurgia periorbitária). The project uses Python to compile Markdown chapters into DOCX, EPUB, and HTML formats.

## Build Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build outputs (requires Pandoc for best results)
python build.py --format html --out dist/ebook.html
python build.py --format docx --out dist/ebook.docx
python build.py --format epub --out dist/ebook.epub

# Validate manuscript (checks for broken MOVE links)
python3 tools/validate_manuscript.py

# Regenerate index files (SUMARIO_MESTRE, MAPA_DE_LINKS, BACKLOGs)
python3 tools/build_master_index.py
```

## Architecture

### Content Structure
- `content/` - Markdown chapters numbered `XX-titulo.md` (00-28)
- `assets/figures/` - Images named `fig-XX-titulo-curto.png`
- `assets/tables/` - Table files
- `config.yml` - Book metadata (title, author, language)

### Cross-Reference System
The manuscript uses internal linking via `[[MOVE:CAP-XX]]` markers:
- `[[MOVE:CAP-08]]` links to chapter 08
- `[[MOVE:CAP-XX]]` is a placeholder that fails validation
- `[[REF]]` marks citations needing bibliography entries
- `**Figura sugerida:**` marks where illustrations are needed

### Generated Index Files (in content/)
- `00_SUMARIO_MESTRE.md` - Auto-generated table of contents
- `00_MAPA_DE_LINKS_MOVE.md` - MOVE link resolution status
- `00_BACKLOG_ARTE.md` - Pending figure locations
- `00_BACKLOG_REFERENCIAS.md` - Pending citation counts

### Templates
- `CASE_TEMPLATE.md` - Clinical case documentation template
- `ALGORITHM_TEMPLATE.md` - Decision algorithm template
- `MANUSCRIPT_GUIDE.md` - Writing style guide

## Writing Conventions

### Chapter Structure
Standard sections per chapter:
- Objetivo
- Quando indicar / quando evitar
- Checklist pré-op (itens de decisão)
- Técnica (visão geral + variações)
- Erros comuns e resgate
- "Notas de arte": luz/sombra, unidades estéticas, continuidade

### Voice
- Surgeon-centric: teach *how to think* before *how to do*
- Core philosophy: **operar ≠ rejuvenescer** (operating ≠ rejuvenating)
- Always include indication, risk, and decision context

### Terms
Standardize on first use:
- "vetor negativo" (negative vector)
- "cantoplastia" vs "cantopexia"
- "tarsal strip"
