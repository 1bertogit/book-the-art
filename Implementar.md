Visão geral do que vamos construir

Você não vai mexer no conteúdo agora.
O Markdown atual (manuscrito_limpo.md) passa a ser fonte única da verdade.

O LaTeX premium entra como camada de apresentação.

Resultado esperado ao final desta fase

PDF com cara de livro médico internacional

Tipografia correta

Hierarquia visual clara

Boxes clínicos elegantes

Figuras bem posicionadas

Sumário automático

Numeração de páginas

Front matter separado (sem numeração romana misturada)

Arquitetura correta (não misturar tudo)

Dentro do repositório atual (book-the-art):

pipeline/
└── premium/
    ├── template.tex          # Template principal Pandoc
    ├── typography.tex        # Fontes, espaçamentos, microtipografia
    ├── headings.tex          # Estilo de títulos
    ├── boxes.tex             # Boxes clínicos
    ├── figures.tex           # Figuras e legendas
    ├── frontmatter.tex       # Capa, prefácio, sumário
    └── colors.tex            # Paleta editorial


Nada disso toca:

content/

tools/

pipeline atual de DOCX / HTML

Isso é camada premium isolada.

Escolhas editoriais (padrão “livro médico sério”)
Engine

xelatex (obrigatório)

Fonte (padrão internacional)

Texto: Libertinus Serif ou Minion Pro (se tiver licença)

Títulos: Libertinus Serif Semibold

Monoespaçada: Inconsolata (apenas se necessário)

Nada de Computer Modern.

1️⃣ template.tex (núcleo)

Este arquivo orquestra tudo.

\documentclass[
  11pt,
  oneside,
  openany
]{book}

% === Pacotes base ===
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{tocloft}
\usepackage{enumitem}
\usepackage{csquotes}

% === Margens (livro médico) ===
\geometry{
  paper=a4paper,
  inner=28mm,
  outer=22mm,
  top=25mm,
  bottom=25mm
}

% === Includes modulares ===
\input{pipeline/premium/colors.tex}
\input{pipeline/premium/typography.tex}
\input{pipeline/premium/headings.tex}
\input{pipeline/premium/boxes.tex}
\input{pipeline/premium/figures.tex}
\input{pipeline/premium/frontmatter.tex}

\begin{document}

$if(frontmatter)$
\frontmatter
$frontmatter$
$endif$

\mainmatter
$body$

\end{document}


Isso já resolve:

estrutura de livro

separação front/main matter

compatibilidade Pandoc

2️⃣ typography.tex (onde livros ganham classe)
% === Fontes ===
\setmainfont{Libertinus Serif}
\setsansfont{Libertinus Sans}
\setmonofont{Inconsolata}

% === Espaçamento ===
\onehalfspacing
\setlength{\parindent}{1.2em}
\setlength{\parskip}{0pt}

% === Microtipografia ===
\microtypesetup{
  protrusion=true,
  expansion=true
}


Nada de texto “arejado demais” ou acadêmico feio.

3️⃣ headings.tex (hierarquia limpa)
\titleformat{\chapter}
  {\normalfont\huge\bfseries}
  {\thechapter}
  {1em}
  {}

\titlespacing*{\chapter}
  {0pt}{0pt}{24pt}

\titleformat{\section}
  {\normalfont\Large\bfseries}
  {\thesection}
  {1em}
  {}

\titleformat{\subsection}
  {\normalfont\large\bfseries}
  {\thesubsection}
  {1em}
  {}


Regra:

nada além de 3 níveis

nada de subsubsection

4️⃣ boxes.tex (onde o livro vira clínico de verdade)

Pandoc vai transformar blockquotes em ambiente customizado:

\usepackage{tcolorbox}

\newtcolorbox{clinicalbox}{
  colback=gray!5,
  colframe=black!40,
  boxrule=0.4pt,
  arc=2mm,
  left=6pt,
  right=6pt,
  top=6pt,
  bottom=6pt
}

\renewenvironment{quote}
  {\begin{clinicalbox}\itshape}
  {\end{clinicalbox}}


Resultado:

boxes elegantes

sem cara de apostila

sem gambiarra visual

5️⃣ figures.tex (figuras médicas decentes)
\captionsetup{
  font=small,
  labelfont=bf,
  justification=raggedright
}

\setlength{\abovecaptionskip}{6pt}
\setlength{\belowcaptionskip}{0pt}


O Pandoc já cuida de:

numeração automática

chamadas no texto (@fig:xx)

6️⃣ frontmatter.tex (acabou a bagunça)
\pagestyle{empty}

\renewcommand{\contentsname}{Sumário}

\cleardoublepage
\tableofcontents
\cleardoublepage

\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}


Isso garante:

sumário limpo

numeração correta

front matter sem número árabe

7️⃣ Target novo no Makefile (isolado)
premium-pdf:
	pandoc dist/manuscrito_limpo.md \
	  --from markdown \
	  --template pipeline/premium/template.tex \
	  --pdf-engine=xelatex \
	  --toc \
	  -o dist/The_Art_of_Eyelid_Surgery_Premium.pdf



      Após finalizar a implementação, 


      Iniciar essa implementação

      Você **tem que implementar** (colocar no repo) — não é “só exemplo” — **se** você quer que o `make premium-pdf` (ou o comando `pandoc ... --template template.tex`) gere um PDF com esse layout.

O texto que você colou mistura duas coisas:

1. **A ideia/arquitetura** (explicação)
2. **Os arquivos reais** que precisam existir para o template funcionar

### O que é obrigatório implementar (mínimo viável)

Para rodar o PDF premium **de verdade**, você precisa ter no repositório:

* `pipeline/premium/template.tex`
* `pipeline/premium/colors.tex`
* `pipeline/premium/typography.tex`
* `pipeline/premium/headings.tex`
* `pipeline/premium/boxes.tex`
* `pipeline/premium/figures.tex`
* `pipeline/premium/frontmatter.tex`

E rodar com:

```bash
pandoc dist/manuscrito_limpo.md \
  --pdf-engine=xelatex \
  --template pipeline/premium/template.tex \
  --toc --toc-depth=2 \
  -o dist/book_premium.pdf
```

Sem esses arquivos, o `\input{pipeline/premium/...}` do `template.tex` **vai falhar**.

---

## O que é “só recomendação” (não quebra build)

Essas partes **não são obrigatórias** para funcionar, mas melhoram o resultado:

* escolher fontes “Minion Pro” (se não tiver licença, esquece)
* adicionar capa “100% LaTeX” mais sofisticada
* ajustar microtipografia, kerning e espaçamentos finos
* criar regras mais avançadas para figuras (float placement)

---

## Atalho: começa com 2 arquivos e depois modulariza

Se você quiser validar rápido, dá pra começar só com:

* `pipeline/premium/template.tex` (contendo tudo inline, sem `\input`)
  e depois quebrar em arquivos.

Mas **do jeito profissional**, modular é melhor (e foi o que eu te entreguei antes).

---

## Checklist pra você saber se “deu certo”

Depois de implementar e rodar:

* o PDF abre com **Sumário** (toc)
* páginas numeradas no rodapé
* capítulos com título grande e consistente
* blockquotes viram **boxes**
* figuras aparecem com legenda “Figura X”

Se qualquer item acima falhar, o template ainda não está sendo usado (ou o build está pegando outro template).

---

### Minha recomendação objetiva

**Não recomeça do zero.** Continua nesse repo e adiciona a camada premium em `pipeline/premium/`. Isso não mexe em `content/` nem destrói seu pipeline atual — é só “skin” de PDF.

Se você colar aqui o seu `Makefile` atual (ou o target de pdf), eu te digo exatamente **onde inserir** o `premium-pdf` sem quebrar nada.
