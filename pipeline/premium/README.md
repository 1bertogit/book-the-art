# Pipeline Premium LaTeX

Template modular para geração de PDF com qualidade editorial.

## Filosofia de Design

**Estilo Editorial** (não didático):
- Cores SUTIS (bordas finas 0.75pt, backgrounds quase-brancos)
- Tipografia profissional com Charter + microtype
- Inspirado em Nature, NEJM, Springer

## Estrutura Modular

```
pipeline/premium/
├── template.tex          # Orquestrador principal
├── typography.tex        # Fontes + microtype
├── colors.tex            # Paleta sutil
├── boxes.tex             # 5 tipos de boxes clínicos
├── headings.tex          # Capítulos/seções/TOC
├── figures.tex           # Legendas de figuras
├── frontmatter.tex       # Capa + sumário
└── template-simple.tex   # Versão sem tcolorbox (fallback)
```

## Dependências dos Módulos

```
template.tex (orquestrador)
├── typography.tex  → INDEPENDENTE
├── colors.tex      → INDEPENDENTE
├── boxes.tex       → depende de colors.tex
├── headings.tex    → depende de colors.tex
├── figures.tex     → depende de colors.tex
└── frontmatter.tex → depende de colors.tex
```

## Paleta de Cores (Sutil/Editorial)

| Box Type | Borda (RGB) | Background (RGB) | Uso |
|----------|-------------|------------------|-----|
| Alert    | 140,60,60   | 252,248,248      | Alertas, contraindicações |
| Pearl    | 120,100,50  | 252,251,246      | Insights, pérolas clínicas |
| Tech     | 60,100,80   | 248,252,250      | Passos técnicos |
| Evidence | 70,100,130  | 248,250,252      | Referências, literatura |
| Note     | 100,120,140 | 250,251,252      | Blockquotes genéricos |

## Uso

```bash
# Via Makefile (recomendado)
make premium-pdf

# Diretamente com Pandoc
pandoc dist/manuscrito_limpo.md \
  --template pipeline/premium/template.tex \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 \
  -o dist/book_premium.pdf
```

## Boxes Clínicos

No Markdown, use fenced divs:

```markdown
::: alertbox
Evite operar em infecção ativa!
:::

::: pearlbox
Use Vicryl 6-0 para fixação do tarsal strip.
:::

::: techbox
Passo técnico detalhado aqui.
:::

::: evidencebox
Estudo de 2024 mostrou que...
:::
```

Blockquotes (`>`) são convertidos automaticamente para `notebox`.

## Tipografia

- **Fonte principal**: Charter (elegante, excelente legibilidade)
- **Sans-serif**: Helvetica Neue (headers, títulos)
- **Monospace**: Menlo (código, dados técnicos)
- **Microtype**: Protrusion e expansion para justificação premium

## Layout

- Capítulos com número grande (72pt) e linha decorativa
- Margens otimizadas para impressão frente/verso (inner=3cm, outer=2.5cm)
- Headers com nome do capítulo/seção
- Footers com número de página e título do livro

## Requisitos

- **XeLaTeX** (para fontspec e polyglossia)
- **Pandoc 3.x+**
- **tcolorbox** (para boxes coloridos)
- Fontes macOS: Charter, Helvetica Neue, Menlo

## Modificando Cores

Para ajustar as cores, edite **apenas** `colors.tex`. Todos os outros módulos herdam as cores definidas lá.

## Fallback

Se tcolorbox não estiver disponível, use `template-simple.tex` que renderiza blockquotes como minipages simples:

```bash
# No Makefile, altere:
PREMIUM_TEMPLATE := $(PREMIUM_DIR)/template-simple.tex
```

## Pipeline Completo

1. `make export` — Gera manuscrito limpo (sem tags editoriais)
2. `make premium-pdf` — Gera PDF premium usando este template

## Separação de Pipelines

Este diretório existe para separar:
- **Pipeline de revisão** (`make validate`, `make export`, `make docx`)
- **Pipeline de publicação** (`make premium-pdf`)

Assim você pode revisar e iterar no conteúdo sem interferir no design editorial final.
