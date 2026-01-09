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
EPUB_OUT := $(DIST)/book.epub

# Metadados Pandoc
BOOK_TITLE := The Art of Eyelid Surgery
BOOK_AUTHOR := Dr. Marcelo Cury
BOOK_LANG := pt-BR
BOOK_DATE := $(shell date +%Y-%m-%d)
BOOK_CSS := $(ASSETS)/style.css
EPUB_CSS := $(ASSETS)/epub.css
REFERENCE_DOCX := $(ASSETS)/reference.docx
PANDOC := pandoc

# =============================================================================
# TARGETS PRINCIPAIS
# =============================================================================

help: ## Mostra esta ajuda
	@echo "The Art of Eyelid Surgery — Build System"
	@echo ""
	@echo "Uso: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

all: build ## Alias para 'build'

validate: ## Valida MOVE e referências
	@echo "🔍 Validando manuscrito..."
	@python3 $(TOOLS)/validate_manuscript.py
	@python3 $(TOOLS)/validate_refs.py

build: validate ## Gera índices e manuscrito consolidado
	@echo ""
	@echo "📚 Gerando artefatos..."
	@python3 $(TOOLS)/build_master_index.py
	@python3 $(TOOLS)/build_manuscrito.py
	@echo ""
	@echo "✅ Build completo!"

clean: ## Limpa arquivos gerados
	@echo "🧹 Limpando..."
	@rm -f $(MANUSCRITO)
	@rm -f $(MANUSCRITO_LIMPO)
	@rm -rf $(DIST)/*
	@echo "✅ Limpo!"

# =============================================================================
# FIGURAS
# =============================================================================

figures-report: ## Relatório de figuras (YAML vs arquivos vs texto)
	@python3 $(TOOLS)/validate_figures.py

figures-validate: ## Valida figuras (falha se houver erros)
	@python3 $(TOOLS)/validate_figures.py --strict

# =============================================================================
# EXPORTAÇÃO
# =============================================================================

editorial-report: ## Relatório de problemas editoriais
	@echo ""
	@echo "📋 Analisando problemas editoriais..."
	@python3 $(TOOLS)/clean_editorial_tags.py --report

editorial-clean: ## Limpa tags editoriais dos capítulos
	@echo ""
	@echo "🧹 Limpando tags editoriais..."
	@python3 $(TOOLS)/clean_editorial_tags.py
	@echo ""
	@echo "✅ Tags editoriais limpas!"

export: build editorial-clean ## Gera versão limpa para exportação
	@echo ""
	@echo "📤 Gerando versão para exportação..."
	@mkdir -p $(DIST)
	@python3 $(TOOLS)/clean_manuscript.py --strip-backlog --out $(MANUSCRITO_LIMPO)
	@echo ""
	@echo "✅ Exportação completa: $(MANUSCRITO_LIMPO)"

export-refs-paren: build ## Exporta com refs em parênteses (ID)
	@mkdir -p $(DIST)
	@python3 $(TOOLS)/clean_manuscript.py --strip-backlog --ref-style=paren --out $(DIST)/manuscrito_refs_paren.md

# =============================================================================
# PIPELINE PREMIUM (LaTeX de publicação)
# =============================================================================

PREMIUM_DIR := pipeline/premium
PREMIUM_TEMPLATE := $(PREMIUM_DIR)/template-simple.tex
PREMIUM_PDF := $(DIST)/book_premium.pdf

premium-pdf: export fix-figures ## Gera PDF premium (qualidade editorial)
	@echo "📚 Gerando PDF Premium..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(PREMIUM_PDF) \
		--from markdown \
		--template $(PREMIUM_TEMPLATE) \
		--pdf-engine=xelatex \
		--top-level-division=chapter \
		--toc \
		--toc-depth=2 \
		--number-sections \
		--metadata title="$(BOOK_TITLE)" \
		--metadata subtitle="Cirurgia Palpebral e Periorbitária" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)" \
		--metadata lang=$(BOOK_LANG) \
		--metadata rights="© 2026 Dr. Marcelo Cury. Todos os direitos reservados."
	@echo "✅ Gerado: $(PREMIUM_PDF)"

# =============================================================================
# CONVERSÕES (requer Pandoc)
# =============================================================================

docx: export ## Gera DOCX (requer Pandoc)
	@echo "📄 Gerando DOCX..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(DOCX_OUT) \
		--from markdown \
		--to docx \
		--reference-doc=$(REFERENCE_DOCX) \
		--toc \
		--toc-depth=2 \
		--standalone \
		--metadata title="$(BOOK_TITLE)" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)" \
		--metadata lang=$(BOOK_LANG)
	@echo "✅ Gerado: $(DOCX_OUT)"

fix-figures: ## Corrige paths de figuras para absolutos
	@python3 $(TOOLS)/fix_figure_paths.py

pdf: export fix-figures ## Gera PDF didático premium (default)
	@echo "📄 Gerando PDF Didático Premium..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(PDF_OUT) \
		--from markdown \
		--to pdf \
		--pdf-engine=xelatex \
		--toc \
		--toc-depth=2 \
		--number-sections \
		-V documentclass=book \
		-V classoption=11pt,a4paper,twoside,openright \
		-V geometry:top=2.5cm,bottom=2.5cm,inner=3cm,outer=2.5cm \
		-V mainfont="Charter" \
		-V sansfont="Helvetica Neue" \
		-V monofont="Menlo" \
		-V linestretch=1.15 \
		-V linkcolor=NavyBlue \
		-V urlcolor=NavyBlue \
		-V toccolor=NavyBlue \
		-V colorlinks=true \
		--metadata title="$(BOOK_TITLE)" \
		--metadata subtitle="Cirurgia Palpebral e Periorbitária" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)" \
		--metadata lang=$(BOOK_LANG) \
		--metadata rights="© 2026 Dr. Marcelo Cury. Todos os direitos reservados."
	@echo "✅ Gerado: $(PDF_OUT)"

pdf-classic: export fix-figures ## Gera PDF clínico elegante (Springer/Elsevier style)
	@echo "📄 Gerando PDF Clínico Elegante..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(DIST)/manuscrito_classic.pdf \
		--from markdown \
		--to pdf \
		--template=$(ASSETS)/template.tex \
		--pdf-engine=xelatex \
		--toc \
		--toc-depth=2 \
		--number-sections \
		--metadata title="$(BOOK_TITLE)" \
		--metadata subtitle="Cirurgia Palpebral e Periorbitária" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)" \
		--metadata lang=$(BOOK_LANG) \
		--metadata rights="© 2026 Dr. Marcelo Cury. Todos os direitos reservados."
	@echo "✅ Gerado: $(DIST)/manuscrito_classic.pdf"

pdf-basic: export ## Gera PDF básico (sem template customizado)
	@echo "📄 Gerando PDF básico..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(DIST)/manuscrito_basic.pdf \
		--from markdown \
		--to pdf \
		--toc \
		--toc-depth=2 \
		--pdf-engine=xelatex \
		-V geometry:margin=2.5cm \
		-V fontsize=11pt \
		-V lang=$(BOOK_LANG) \
		--metadata title="$(BOOK_TITLE)" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)"
	@echo "✅ Gerado: $(DIST)/manuscrito_basic.pdf"

html: export ## Gera HTML standalone
	@echo "📄 Gerando HTML..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(HTML_OUT) \
		--from markdown \
		--to html5 \
		--toc \
		--toc-depth=2 \
		--standalone \
		--embed-resources \
		--metadata title="$(BOOK_TITLE)" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)" \
		--metadata lang=$(BOOK_LANG) \
		--css $(BOOK_CSS)
	@echo "✅ Gerado: $(HTML_OUT)"

epub: export fix-figures ## Gera ePub (Kindle/Apple Books)
	@echo "📱 Gerando ePub..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(EPUB_OUT) \
		--from markdown \
		--to epub3 \
		--toc \
		--toc-depth=2 \
		--epub-chapter-level=1 \
		--css=$(EPUB_CSS) \
		--metadata title="$(BOOK_TITLE)" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata lang=$(BOOK_LANG) \
		--metadata rights="© 2026 Dr. Marcelo Cury. Todos os direitos reservados."
	@echo "✅ Gerado: $(EPUB_OUT)"

# =============================================================================
# DESENVOLVIMENTO
# =============================================================================

watch: ## Monitora mudanças e rebuilda (requer fswatch)
	@echo "👀 Monitorando mudanças em $(CONTENT)/*.md..."
	@fswatch -o $(CONTENT)/*.md | xargs -n1 -I{} make build

stats: ## Mostra estatísticas do manuscrito
	@echo "📊 Estatísticas do Manuscrito"
	@echo ""
	@echo "Capítulos:"
	@ls -1 $(CONTENT)/[0-9]*.md 2>/dev/null | wc -l | xargs echo "  Total:"
	@echo ""
	@echo "Palavras (aproximado):"
	@cat $(CONTENT)/[0-9]*.md 2>/dev/null | wc -w | xargs echo "  Total:"
	@echo ""
	@echo "Referências:"
	@grep -oh '\[\[REF:[A-Z0-9_-]*\]\]' $(CONTENT)/[0-9]*.md 2>/dev/null | sort -u | wc -l | xargs echo "  IDs únicos:"
	@grep -oh '\[\[REF:[A-Z0-9_-]*\]\]' $(CONTENT)/[0-9]*.md 2>/dev/null | wc -l | xargs echo "  Total citações:"
	@echo ""
	@echo "Figuras sugeridas:"
	@grep -c 'Figura sugerida' $(CONTENT)/[0-9]*.md 2>/dev/null | awk -F: '{sum += $$2} END {print "  Total: " sum}'

check: validate ## Alias para 'validate'
