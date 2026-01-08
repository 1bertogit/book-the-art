# Pipeline Premium — The Art of Eyelid Surgery

Este diretório contém os templates LaTeX para geração de PDF com qualidade editorial premium.

## Estrutura

```
pipeline/premium/
├── template.tex      # Template principal (importa os módulos)
├── typography.tex    # Fontes e espaçamento
├── colors.tex        # Paleta de cores médica
├── boxes.tex         # Boxes clínicos coloridos
├── headings.tex      # Capítulos, seções e headers/footers
└── README.md         # Este arquivo
```

## Uso

### Via Makefile principal (recomendado)

```bash
# A partir da raiz do projeto:
make premium-pdf
```

### Via Pandoc direto

```bash
cd pipeline/premium
pandoc ../../dist/manuscrito_limpo.md \
  --from markdown \
  --template template.tex \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 \
  --number-sections \
  -o ../../dist/book_premium.pdf
```

## Características do Template

### Tipografia
- **Fonte principal**: Charter (elegante, excelente legibilidade)
- **Sans-serif**: Helvetica Neue (headers, títulos)
- **Monospace**: Menlo (código, dados técnicos)

### Boxes Clínicos
| Box | Cor | Uso |
|-----|-----|-----|
| `alertbox` | Vermelho | Alertas, contraindicações, riscos |
| `pearlbox` | Dourado | Insights práticos, pérolas clínicas |
| `techbox` | Verde | Passos técnicos, manobras |
| `evidencebox` | Azul | Referências, literatura |
| `notebox` | Azul claro | Blockquotes genéricos |

### Layout
- Capítulos com número grande (72pt) e linha decorativa
- Margens otimizadas para impressão frente/verso
- Headers com nome do capítulo/seção
- Footers com número de página e título do livro

## Requisitos

- XeLaTeX (incluído no MacTeX ou TeX Live)
- Pandoc 3.x
- Fontes macOS: Charter, Helvetica Neue, Menlo

## Pipeline Completo

1. `make export` — Gera manuscrito limpo (sem tags editoriais)
2. `make premium-pdf` — Gera PDF premium usando este template

## Separação de Pipelines

Este diretório existe para separar:
- **Pipeline de revisão** (`make validate`, `make export`, `make docx`)
- **Pipeline de publicação** (`make premium-pdf`)

Assim você pode revisar e iterar no conteúdo sem interferir no design editorial final.
