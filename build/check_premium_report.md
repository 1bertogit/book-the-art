# Relatório de verificação: premium (gerado em 2026-01-08T23:05:51Z)

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
	@echo \
```

## Capítulos (manuscrito) — PASS

Capítulos nível 1 parecem corretos

```
73:# Notas legais, escopo e uso responsável (educacional) {-}
111:# Introdução: a filosofia do rejuvenescimento (operar ≠ rejuvenescer)
220:# Luz e sombra: unidades estéticas e continuidade periorbitária
341:# Envelhecimento multifatorial: deflation, ligamentos e osso
465:# Anatomia cirúrgica aplicada: lamelas, septo e ligamentos retentores
590:# Mapas de risco e erros de plano: zonas de segurança vs perigo
733:# Checklist mental do resultado “nota 10” (princípios replicáveis)
843:# Fotodocumentação estratégica: sem flash, com flash e padronização
971:# Exame físico: vetores, flacidez, testes e assimetrias
1108:# Consulta e expectativa: alinhar pedido do paciente com necessidade anatômica
1251:# Algoritmos por fenótipo: superior, inferior, terço médio e casos mistos
1381:# Marcação e medidas: superior e inferior (conservadorismo e simetria)
1500:# Anestesia, infiltração, hemostasia e pós imediato (segurança)
1625:# Brow management: por que blef isolada falha (Connell) e indicações
1746:# Técnicas de brow lift: temporal, endoscópico, Castañares modificado
1910:# Blefaroplastia superior: pele, gordura (preservação) e glândula lacrimal
2049:# Ptose associada no superior: quando reconhecer e como integrar ao plano
2178:# Pálpebra inferior transconjuntival: preferências, septo e bolsas
2329:# Transposição/redistribuição de gordura: sulco nasojugal e transição pálpebra-malar
2468:# Manejo de pele no inferior: skin pinch e refinamentos sem descolamento amplo
2604:# Festoon / edema malar: fisiopatologia e opções (orbicular, espaço pré-malar, resurfacing, excisão)
2737:# Sustentação: quando cantopexia resolve e quando não resolve
2890:# Cantopexia vs. Cantoplastia: indicações por vetor e flacidez
3036:# Técnicas de canto lateral: Mladick, Tarsal Strip e McCord (e variações)
3205:# Microfat: coleta, preparo e injeção; zonas e volumes (justa-periostal)
3372:# Nanofat e qualidade de pele: cicatrizes, olheiras, textura e microagulhamento
3539:# Funcional e reconstrução: ectrópio/entrópio/retração e princípios das lamelas
3704:# Reconstrução pós-tumor: retalhos clássicos (Tenzel, Hughes, Cutler-Beard, Mustardé)
3902:# Complicações, revisões e gestão: prevenção, resgate e precificação
4134:# Bibliografia Mestre {-}
4302:# Fim do Manuscrito {-}
```

## Geometry — PASS

Found \geometry with inner/outer in template

```
pipeline/premium/template-simple.tex:36:\geometry{
```

## Head/Foot config — PASS

Encontrado headheight/headsep/footskip

```
pipeline/premium/template.tex:64:  headheight=14pt,
pipeline/premium/template.tex:65:  headsep=1.2cm,
pipeline/premium/template.tex:66:  footskip=1.5cm,
pipeline/premium/template-simple.tex:42:  headheight=14pt,
pipeline/premium/template-simple.tex:43:  headsep=12pt,
pipeline/premium/template-simple.tex:44:  footskip=24pt
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
projects/eyelid-surgery/assets/template.tex:27:\setmainfont{Palatino}
projects/eyelid-surgery/assets/template-didactic.tex:50:\setmainfont{Charter}
pipeline/premium/template.tex:10:% - Tipografia premium (Charter + Helvetica Neue + microtype)
pipeline/premium/template-simple.tex:9:% - Tipografia premium (Charter + Helvetica Neue + microtype)
pipeline/premium/template-simple.tex:58:  \setmainfont{Libertinus Serif}
pipeline/premium/template-simple.tex:60:  \setmainfont{Charter}
pipeline/premium/template-simple.tex:74:% Nota: expansion e spacing não funcionam com XeTeX
pipeline/premium/template-simple.tex:75:\usepackage{microtype}
pipeline/premium/template-simple.tex:76:\microtypesetup{
pipeline/premium/template-simple.tex:77:  protrusion=true
pipeline/premium/typography.tex:7:% REQUER: XeLaTeX (para fontspec e microtype avançado)
pipeline/premium/typography.tex:21:\setmainfont{Charter}
pipeline/premium/typography.tex:35:\usepackage{microtype}
pipeline/premium/typography.tex:36:\microtypesetup{
pipeline/premium/typography.tex:37:  protrusion=true,    % Pequenas projeções para melhor margem visual
pipeline/premium/typography.tex:38:  expansion=true,     % Expansão/contração sutil para melhor justificação
```

## Font warnings (log) — WARN

Log do LaTeX não encontrado em build/*.log — rode o build para gerar logs


## Boxes clínicos — PASS

Pacote/mdframed ou redefinição de quote encontrada

```
pipeline/premium/template-simple.tex:140:\usepackage{mdframed}
pipeline/premium/template-simple.tex:143:
ewmdenv[
```

## Figuras — PASS

Encontradas referências a includegraphics/caption/maxwidth nos templates/tex

```
pipeline/premium/figures.tex:24:]{caption}
pipeline/premium/figures.tex:30:\usepackage{subcaption}
pipeline/premium/template-simple.tex:258:\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
pipeline/premium/template-simple.tex:259:\def\maxheight{\ifdim\Gin@nat@height>0.8\textheight 0.8\textheight\else\Gin@nat@height\fi}
pipeline/premium/template-simple.tex:261:\setkeys{Gin}{width=\maxwidth,height=\maxheight,keepaspectratio}
pipeline/premium/template-simple.tex:284:]{caption}
projects/eyelid-surgery/assets/template.tex:40:\usepackage[font=small,labelfont=bf]{caption}
projects/eyelid-surgery/assets/template-didactic.tex:98:]{caption}
projects/eyelid-surgery/assets/header-didactic.tex:109:]{caption}
```

## Idioma / hifenização — PASS

Configuração de idioma encontrada

```
pipeline/premium/template-simple.tex:52:\usepackage{polyglossia}
pipeline/premium/template-simple.tex:53:\setmainlanguage{portuguese}
pipeline/premium/template-simple.tex:96:% Hifenização (polyglossia já configura para português)
pipeline/premium/template-simple.tex:353:% Fix: polyglossia sobrescreve contentsname, forçar aqui
pipeline/premium/typography.tex:13:\usepackage{polyglossia}
pipeline/premium/typography.tex:14:\setmainlanguage{portuguese}
projects/eyelid-surgery/assets/template.tex:12:\usepackage{polyglossia}
projects/eyelid-surgery/assets/template.tex:13:\setmainlanguage{portuguese}
projects/eyelid-surgery/assets/template-base.tex:3:$for(babel-otherlangs)$
projects/eyelid-surgery/assets/template-base.tex:4:  $babel-otherlangs$,
projects/eyelid-surgery/assets/template-base.tex:6:$if(babel-lang)$
projects/eyelid-surgery/assets/template-base.tex:7:  $babel-lang$,
projects/eyelid-surgery/assets/template-didactic.tex:30:\usepackage{polyglossia}
projects/eyelid-surgery/assets/template-didactic.tex:31:\setmainlanguage{portuguese}
```

## Headers/Footers — PASS

Configuração de cabeçalhos/rodapés encontrada

```
pipeline/premium/template.tex:64:  headheight=14pt,
pipeline/premium/template.tex:65:  headsep=1.2cm,
pipeline/premium/template.tex:66:  footskip=1.5cm,
pipeline/premium/headings.tex:51:\usepackage{fancyhdr}
pipeline/premium/headings.tex:53:\pagestyle{fancy}
pipeline/premium/headings.tex:70:\fancypagestyle{plain}{
pipeline/premium/frontmatter.tex:72:  \thispagestyle{empty}
pipeline/premium/template-simple.tex:42:  headheight=14pt,
pipeline/premium/template-simple.tex:43:  headsep=12pt,
pipeline/premium/template-simple.tex:44:  footskip=24pt
pipeline/premium/template-simple.tex:203:\usepackage{fancyhdr}
pipeline/premium/template-simple.tex:205:\pagestyle{fancy}
pipeline/premium/template-simple.tex:220:\fancypagestyle{plain}{
pipeline/premium/template-simple.tex:391:\thispagestyle{empty}
projects/eyelid-surgery/assets/template.tex:21:  headheight=15pt,
projects/eyelid-surgery/assets/template.tex:22:  headsep=1cm,
projects/eyelid-surgery/assets/template.tex:23:  footskip=1.5cm
projects/eyelid-surgery/assets/template.tex:54:\usepackage{fancyhdr}
projects/eyelid-surgery/assets/template.tex:55:\pagestyle{fancy}
projects/eyelid-surgery/assets/template.tex:65:\fancypagestyle{plain}{
projects/eyelid-surgery/assets/header-didactic.tex:68:\usepackage{fancyhdr}
projects/eyelid-surgery/assets/header-didactic.tex:70:\pagestyle{fancy}
projects/eyelid-surgery/assets/header-didactic.tex:81:\fancypagestyle{plain}{
projects/eyelid-surgery/assets/template-didactic.tex:39:  headheight=14pt,
projects/eyelid-surgery/assets/template-didactic.tex:40:  headsep=1.2cm,
projects/eyelid-surgery/assets/template-didactic.tex:41:  footskip=1.5cm,
projects/eyelid-surgery/assets/template-didactic.tex:258:\usepackage{fancyhdr}
projects/eyelid-surgery/assets/template-didactic.tex:260:\pagestyle{fancy}
projects/eyelid-surgery/assets/template-didactic.tex:277:\fancypagestyle{plain}{
```

## TOC aparece como 'Sumário' — PASS

Sumário encontrado e CONTEÚDO não encontrado

```
The Art of Eyelid
Surgery
Cirurgia Palpebral e Periorbitária

Dr. Marcelo Cury, MD
Cirurgião Plástico — Especialista em Cirurgia Palpebral

Rio de Janeiro, Brasil
2026

The Art of Eyelid Surgery
Cirurgia Palpebral e Periorbitária
© 2026 Dr. Marcelo Cury — Todos os direitos reservados.
1ª Edição

Este conteúdo destina-se a ﬁns educacionais para proﬁssionais de saúde. Nenhuma parte desta obra pode
ser reproduzida sem autorização prévia.

ii

SUMÁRIO

Sumário
Direitos Autorais . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1

Nota Importante (Uso Educacional) . . . . . . . . . . . . . . . . . . . . . . . . .

1

Prefácio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1

Sobre o Autor . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1

Nota de Origem do Conteúdo . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2

Notas legais, escopo e uso responsável (educacional)

1

0.1

Escopo do livro . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

## Front matter no template — WARN

Não encontrei \frontmatter / \mainmatter / \pagenumbering{roman} no template — verifique se a separação de numeração está sendo feita

```
% ═══════════════════════════════════════════════════════════════════════════
% Template LaTeX PREMIUM — The Art of Eyelid Surgery
% ═══════════════════════════════════════════════════════════════════════════
% Estilo: EDITORIAL PREMIUM (Nature, NEJM, Springer)
% REQUER: XeLaTeX (para fontes OpenType via fontspec)
%
% Características:
% - Cores SUTIS (bordas finas 0.75pt, backgrounds quase-brancos)
% - Tipografia premium (Charter + Helvetica Neue + microtype)
% - Boxes clínicos elegantes (5 tipos)
% - Preparado para publicação profissional
%
% Uso: pandoc --pdf-engine=xelatex --template=template-simple.tex
% ═══════════════════════════════════════════════════════════════════════════

% PATCH 1: twoside + openany (padrão editorial médico)
\documentclass[11pt,twoside,openany]{book}

% ═══════════════════════════════════════════════════════════════════════════
% COMPATIBILIDADE PANDOC 3.8+
% ═══════════════════════════════════════════════════════════════════════════

\makeatletter
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\NewStructureName}[2]{}
\providecommand{\SetStructureName}[2]{}
\providecommand{\AssignStructureRole}[2]{}
\providecommand{\pandocbounded}[1]{#1}
\makeatother

% ═══════════════════════════════════════════════════════════════════════════
% GEOMETRIA — PATCH 2: margens simétricas (fix \
```

## make premium-pdf — PASS

make premium-pdf executou sem erro

```
🧹 Limpando...
✅ Limpo!
🔍 Validando manuscrito...
🔍 Validando manuscrito...
   Diretório: /Users/humbertolopes/Dev/work/marcelo-cury/the_art_of_eyelid_surgery_scaffold/content

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
