# Multi-Project Ebook Generator

Este repositório gerencia **múltiplos projetos de ebooks** usando scripts compartilhados para compilar em **DOCX / EPUB / HTML / PDF**.

## 📁 Estrutura Geral

```
the_art_of_eyelid_surgery_scaffold/
├─ projects/
│  ├─ eyelid-surgery/          # Projeto: The Art of Eyelid Surgery
│  │  ├─ config.yml
│  │  ├─ content/              # 28 capítulos
│  │  ├─ assets/
│  │  └─ dist/                 # Output
│  │
│  └─ modern-face/             # Projeto: Modern Face
│     ├─ config_template.yml
│     ├─ ebook-1/              # 5 ebooks independentes
│     ├─ ebook-2/
│     ├─ ebook-3/
│     ├─ ebook-4/
│     └─ ebook-5/
│
├─ shared/                     # Scripts compartilhados
│  ├─ build.py
│  └─ generate_complete_ebook.py
│
├─ tools/                      # Ferramentas auxiliares
├─ requirements.txt
└─ Makefile
```

## Instalação
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> Recomendado: instalar **Pandoc** para exportação DOCX/EPUB com alta fidelidade.

## 🚀 Como Usar

### Para o projeto **Eyelid Surgery**:
```bash
cd projects/eyelid-surgery
python ../../shared/generate_complete_ebook.py
# Output: dist/ebook_completo.md
```

### Para o projeto **Modern Face**:
```bash
cd projects/modern-face/ebook-1
# 1. Adicione seus capítulos em content/
# 2. Copie e ajuste config_template.yml
python ../../../shared/generate_complete_ebook.py --config config_ebook1.yml
```

### Build com Pandoc (qualquer projeto):
```bash
# Navegue até a pasta do projeto
cd projects/eyelid-surgery  # ou projects/modern-face/ebook-1

# Gere HTML
pandoc dist/ebook_completo.md -o dist/ebook.html --css=assets/style.css

# Gere DOCX
pandoc dist/ebook_completo.md -o dist/ebook.docx

# Gere PDF (requer LaTeX)
pandoc dist/ebook_completo.md -o dist/ebook.pdf
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
