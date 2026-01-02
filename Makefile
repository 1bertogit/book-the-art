.PHONY: all validate build clean export help

# Diretórios
CONTENT := content
DIST := dist
TOOLS := tools
ASSETS := assets

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
# EXPORTAÇÃO
# =============================================================================

export: build ## Gera versão limpa para exportação
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
# CONVERSÕES (requer Pandoc)
# =============================================================================

docx: export ## Gera DOCX (requer Pandoc)
	@echo "📄 Gerando DOCX..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(DOCX_OUT) \
		--from markdown \
		--to docx \
		--toc \
		--toc-depth=2 \
		--standalone \
		--metadata title="$(BOOK_TITLE)" \
		--metadata author="$(BOOK_AUTHOR)" \
		--metadata date="$(BOOK_DATE)" \
		--metadata lang=$(BOOK_LANG)
	@echo "✅ Gerado: $(DOCX_OUT)"

pdf: export ## Gera PDF (requer Pandoc + LaTeX)
	@echo "📄 Gerando PDF..."
	@$(PANDOC) $(MANUSCRITO_LIMPO) -o $(PDF_OUT) \
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
	@echo "✅ Gerado: $(PDF_OUT)"

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
