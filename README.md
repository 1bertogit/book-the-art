# The Art of Eyelid Surgery — Estrutura (Scaffold)

Este repositório cria a **estrutura completa** do manuscrito em Markdown, pronta para compilar em **DOCX / EPUB / HTML** com Python.

## Estrutura
```
the_art_of_eyelid_surgery_scaffold/
├─ build.py
├─ requirements.txt
├─ config.yml
├─ MANUSCRIPT_GUIDE.md
├─ assets/
│  ├─ figures/
│  └─ tables/
└─ content/
   ├─ 00-notas-legais-e-escopo.md
   ├─ 01-introducao-filosofia.md
   ├─ ...
   └─ 28-gestao-e-precificacao.md
```

## Instalação
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> Recomendado: instalar **Pandoc** para exportação DOCX/EPUB com alta fidelidade.

## Build
```bash
# Validação + consolidado + versão limpa
make export

# Conversões (Pandoc)
make html   # dist/ebook.html (usa assets/style.css)
make docx   # dist/manuscrito.docx
make pdf    # dist/manuscrito.pdf (requer LaTeX)

# Alternativa: builder Python puro
python build.py --format html --out dist/ebook.html
python build.py --format docx --out dist/ebook.docx
python build.py --format epub --out dist/ebook.epub
```

### Estilo visual
- Personalize `assets/style.css` para ajustar tipografia/cores.
- `build.py` e o alvo `make html` injetam automaticamente esse CSS no HTML final.

## Como escrever (ritual simples)
1. Abra o capítulo correspondente em `content/`.
2. Preencha as seções do template.
3. Marque onde entram figuras/tabelas com os placeholders.
4. Gere HTML para revisar rápido; finalize no DOCX para revisão editorial e PDF.

© 2026
