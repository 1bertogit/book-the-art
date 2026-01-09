# Relatório de verificação: premium (gerado em 2026-01-09T03:01:01Z)

Resumo por item:

## Template LaTeX — PASS

Encontrado template em pipeline/premium

```
pipeline/premium/template-simple.tex
pipeline/premium/template.tex
```

## Makefile -> Pandoc flags — PASS

Makefile tem referência a --template e --pdf-engine=xelatex em regra de build (ex: premium-pdf / pdf)

```
.PHONY: all validate build clean export help premium-pdf

# Diretórios
PROJECT := projects/eyelid-surgery
CONTENT := $(PROJECT)/content
DIST := dist
TOOLS := tools
ASSETS := $(PROJECT)/assets

# Arquivos de saída
MANUSCRITO := $(CONTENT)/00_MANUSCRITO.md
MANUSCRITO_LIMPO := $(DIST)/manuscrito_limpo.md
DOCX_OUT := $(DIST)/manuscrito.docx
HTML_OUT := $(DIST)/ebook.html
PDF_OUT := $(DIST)/manuscrito.pdf

# Metadados Pandoc
BOOK_TITLE := The Art of Eyelid Surgery
BOOK_AUTHOR := Dr. Marcelo Cury
BOOK_LANG := pt-BR
BOOK_DATE := $(shell date +%Y-%m-%d)
BOOK_CSS := $(ASSETS)/style.css
REFERENCE_DOCX := $(ASSETS)/reference.docx
PANDOC := pandoc

# =============================================================================
# TARGETS PRINCIPAIS
# =============================================================================

help: ## Mostra esta ajuda
\t@echo \
```

## Capítulos (manuscrito) — FAIL

dist/manuscrito_limpo.md não encontrado


## Geometry — PASS

Found \\geometry with inner/outer in template

```
pipeline/premium/template.tex:61:  \\geometry{
pipeline/premium/template-simple.tex:37:  \\geometry{
```

## Head/Foot config — PASS

Encontrado headheight/headsep/footskip

```
pipeline/premium/template.tex:67:    headheight=14pt,
pipeline/premium/template.tex:68:    headsep=1.2cm,
pipeline/premium/template.tex:69:    footskip=1.5cm,
pipeline/premium/template-simple.tex:43:    headheight=14pt,
pipeline/premium/template-simple.tex:44:    headsep=12pt,
pipeline/premium/template-simple.tex:45:    footskip=24pt
projects/eyelid-surgery/assets/template.tex:21:  headheight=15pt,
projects/eyelid-surgery/assets/template.tex:22:  headsep=1cm,
projects/eyelid-surgery/assets/template.tex:23:  footskip=1.5cm
projects/eyelid-surgery/assets/template-didactic.tex:39:  headheight=14pt,
projects/eyelid-surgery/assets/template-didactic.tex:40:  headsep=1.2cm,
projects/eyelid-surgery/assets/template-didactic.tex:41:  footskip=1.5cm,
```

## Tipografia — PASS

Encontrado configuração de fonte/microtype

```
projects/eyelid-surgery/assets/template.tex:27:\\setmainfont{Palatino}
pipeline/premium/template.tex:10:% - Tipografia premium (Charter + Helvetica Neue + microtype)
pipeline/premium/template-simple.tex:9:% - Tipografia premium (Charter + Helvetica Neue + microtype)
pipeline/premium/template-simple.tex:60:  \\setmainfont{Libertinus Serif}
pipeline/premium/template-simple.tex:62:  \\setmainfont{Charter}
pipeline/premium/template-simple.tex:76:% Nota: expansion e spacing não funcionam com XeTeX
pipeline/premium/template-simple.tex:77:\\usepackage{microtype}
pipeline/premium/template-simple.tex:78:\\microtypesetup{
pipeline/premium/template-simple.tex:79:  protrusion=true
pipeline/premium/typography.tex:7:% REQUER: XeLaTeX (para fontspec e microtype avançado)
pipeline/premium/typography.tex:21:\\setmainfont{Charter}
pipeline/premium/typography.tex:35:\\usepackage{microtype}
pipeline/premium/typography.tex:36:\\microtypesetup{
pipeline/premium/typography.tex:37:  protrusion=true,    % Pequenas projeções para melhor margem visual
pipeline/premium/typography.tex:38:  expansion=true,     % Expansão/contração sutil para melhor justificação
projects/eyelid-surgery/assets/template-didactic.tex:50:\\setmainfont{Charter}
```

## Font warnings (log) — WARN

Log do LaTeX não encontrado em build/*.log — rode o build para gerar logs


## Boxes clínicos — PASS

Pacote/mdframed ou redefinição de quote encontrada

```
pipeline/premium/template-simple.tex:142:\\usepackage{mdframed}
pipeline/premium/template-simple.tex:145:\
ewmdenv[
```

## Figuras — PASS

Encontradas referências a includegraphics/caption/maxwidth nos templates/tex

```
pipeline/premium/figures.tex:24:]{caption}
pipeline/premium/figures.tex:30:\\usepackage{subcaption}
pipeline/premium/template-simple.tex:260:\\def\\maxwidth{\\ifdim\\Gin@nat@width>\\linewidth\\linewidth\\else\\Gin@nat@width\\fi}
pipeline/premium/template-simple.tex:261:\\def\\maxheight{\\ifdim\\Gin@nat@height>0.8\\textheight 0.8\\textheight\\else\\Gin@nat@height\\fi}
pipeline/premium/template-simple.tex:263:\\setkeys{Gin}{width=\\maxwidth,height=\\maxheight,keepaspectratio}
pipeline/premium/template-simple.tex:286:]{caption}
projects/eyelid-surgery/assets/template.tex:40:\\usepackage[font=small,labelfont=bf]{caption}
projects/eyelid-surgery/assets/header-didactic.tex:109:]{caption}
projects/eyelid-surgery/assets/template-didactic.tex:98:]{caption}
```

## Idioma / hifenização — PASS

Configuração de idioma encontrada

```
pipeline/premium/template-simple.tex:54:\\usepackage{polyglossia}
pipeline/premium/template-simple.tex:55:\\setmainlanguage{portuguese}
pipeline/premium/template-simple.tex:98:% Hifenização (polyglossia já configura para português)
pipeline/premium/template-simple.tex:355:% Fix: polyglossia sobrescreve contentsname, forçar aqui
pipeline/premium/typography.tex:13:\\usepackage{polyglossia}
pipeline/premium/typography.tex:14:\\setmainlanguage{portuguese}
projects/eyelid-surgery/assets/template.tex:12:\\usepackage{polyglossia}
projects/eyelid-surgery/assets/template.tex:13:\\setmainlanguage{portuguese}
projects/eyelid-surgery/assets/template-base.tex:3:$for(babel-otherlangs)$
projects/eyelid-surgery/assets/template-base.tex:4:  $babel-otherlangs$,
projects/eyelid-surgery/assets/template-base.tex:6:$if(babel-lang)$
projects/eyelid-surgery/assets/template-base.tex:7:  $babel-lang$,
projects/eyelid-surgery/assets/template-didactic.tex:30:\\usepackage{polyglossia}
projects/eyelid-surgery/assets/template-didactic.tex:31:\\setmainlanguage{portuguese}
```

## Headers/Footers — PASS

Configuração de cabeçalhos/rodapés encontrada

```
pipeline/premium/template.tex:67:    headheight=14pt,
pipeline/premium/template.tex:68:    headsep=1.2cm,
pipeline/premium/template.tex:69:    footskip=1.5cm,
pipeline/premium/headings.tex:51:\\usepackage{fancyhdr}
pipeline/premium/headings.tex:53:\\pagestyle{fancy}
pipeline/premium/headings.tex:70:\\fancypagestyle{plain}{
pipeline/premium/frontmatter.tex:72:  \\thispagestyle{empty}
projects/eyelid-surgery/assets/template.tex:21:  headheight=15pt,
projects/eyelid-surgery/assets/template.tex:22:  headsep=1cm,
projects/eyelid-surgery/assets/template.tex:23:  footskip=1.5cm
projects/eyelid-surgery/assets/template.tex:54:\\usepackage{fancyhdr}
projects/eyelid-surgery/assets/template.tex:55:\\pagestyle{fancy}
projects/eyelid-surgery/assets/template.tex:65:\\fancypagestyle{plain}{
pipeline/premium/template-simple.tex:43:    headheight=14pt,
pipeline/premium/template-simple.tex:44:    headsep=12pt,
pipeline/premium/template-simple.tex:45:    footskip=24pt
pipeline/premium/template-simple.tex:205:\\usepackage{fancyhdr}
pipeline/premium/template-simple.tex:207:\\pagestyle{fancy}
pipeline/premium/template-simple.tex:222:\\fancypagestyle{plain}{
pipeline/premium/template-simple.tex:393:\\thispagestyle{empty}
projects/eyelid-surgery/assets/header-didactic.tex:68:\\usepackage{fancyhdr}
projects/eyelid-surgery/assets/header-didactic.tex:70:\\pagestyle{fancy}
projects/eyelid-surgery/assets/header-didactic.tex:81:\\fancypagestyle{plain}{
projects/eyelid-surgery/assets/template-didactic.tex:39:  headheight=14pt,
projects/eyelid-surgery/assets/template-didactic.tex:40:  headsep=1.2cm,
projects/eyelid-surgery/assets/template-didactic.tex:41:  footskip=1.5cm,
projects/eyelid-surgery/assets/template-didactic.tex:258:\\usepackage{fancyhdr}
projects/eyelid-surgery/assets/template-didactic.tex:260:\\pagestyle{fancy}
projects/eyelid-surgery/assets/template-didactic.tex:277:\\fancypagestyle{plain}{
```

## TOC/Front matter (PDF) — WARN

PDF não encontrado em dist/*.pdf — tente gerar com make premium-pdf


## make premium-pdf — PASS

make premium-pdf executou sem erro

```
🧹 Limpando...
✅ Limpo!
🔍 Validando manuscrito...
🔍 Validando manuscrito...
   Diretório: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content

✅ Manuscrito válido — nenhum MOVE quebrado!
🔍 Validando referências...
   Bibliografia: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content/99_BIBLIOGRAFIA.md

✅ Todas as 39 referências usadas existem na bibliografia!

⚠️  2 ID(s) na bibliografia mas NÃO usados (ok, só higiene):
   • CASTANARES-1964
   • MOST-2007

📊 Resumo: 39 usados | 41 definidos | 2 não usados

📚 Gerando artefatos...
OK: gerados:
- content/00_SUMARIO_MESTRE.md
- content/00_MAPA_DE_LINKS_MOVE.md
- content/00_BACKLOG_ARTE.md
- content/00_BACKLOG_REFERENCIAS.md
📚 Gerando manuscrito consolidado...
   Sumário: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content/00_SUMARIO_MESTRE.md
   Saída: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content/00_MANUSCRITO.md
   Clean: Não

   Encontrados: 30 capítulos
   ✓ Front matter incluído: 00_FRONT_MATTER.md

✅ Manuscrito gerado: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content/00_MANUSCRITO.md
   • 30 capítulos
   • ~28,963 palavras
   • ~210,397 caracteres

✅ Build completo!

🧹 Limpando tags editoriais...
🔍 Limpeza Editorial — The Art of Eyelid Surgery
   Diretório: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content

   Arquivos: 36

🧹 APLICANDO LIMPEZA EDITORIAL
============================================================

============================================================
✅ 0 mudanças aplicadas

✅ Tags editoriais limpas!

📤 Gerando versão para exportação...
🧹 Limpando manuscrito para exportação...
   Entrada: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/content/00_MANUSCRITO.md
   Saída: dist/manuscrito_limpo.md
   Refs: keep
   Strip backlog: True

✅ Manuscrito limpo gerado: dist/manuscrito_limpo.md
   • 28,892 palavras
   • 208,413 caracteres
   • Redução: 0.9%

✅ Exportação completa: dist/manuscrito_limpo.md
🔧 Corrigindo paths de figuras...
   Manuscrito: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/dist/manuscrito_limpo.md
   Figuras: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/projects/eyelid-surgery/assets/figures

   figures.yml: 27 figuras declaradas
   Figuras no texto: 27

✅ 27 paths corrigidos
   Salvo em: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/dist/manuscrito_limpo.md
📚 Gerando PDF Premium...
✅ Gerado: dist/book_premium.pdf
```

## PDF gerado — PASS

PDF(s) encontrados em dist/: dist/book_premium.pdf 


### Observações
- Este script faz checagens heurísticas. Inspeção visual pode ser necessária para casos de layout/boxes/figuras.
- Se quiser, conecte este script ao CI e faça o Ralph executar repetidamente até PASS.
