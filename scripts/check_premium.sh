#!/usr/bin/env bash
# check_premium.sh
# Verificações automatizadas do checklist "premium" (LaTeX / Pandoc / Makefile).
# Saídas:
#  - build/check_premium_report.md (relatório legível)
#  - build/check_premium_report.json (máquina)
#
# Não quebra na primeira falha — coleta todos os resultados e sai com código != 0 se houver algum FAIL.

set -u
BASEDIR="$(pwd)"
OUTDIR="${BASEDIR}/build"
REPORT_MD="${OUTDIR}/check_premium_report.md"
REPORT_JSON="${OUTDIR}/check_premium_report.json"
mkdir -p "${OUTDIR}"

# Ferramentas preferidas
if command -v rg >/dev/null 2>&1; then
  FIND='rg -n --hidden --no-ignore-vcs'
else
  FIND='grep -R -n --binary-files=without-match'
fi

has() { command -v "$1" >/dev/null 2>&1; }

# Collect results
results=()

add_result() {
  local name="$1"; local status="$2"; local msg="$3"; local detail="$4"
  # Escape newlines for JSON (portable way)
  local escaped_detail
  escaped_detail=$(echo "$detail" | awk '{printf "%s\\n", $0}' | sed 's/\\n$//' | sed 's/"/\\"/g')
  results+=("$(printf '{"name":"%s","status":"%s","message":"%s","detail":"%s"}' \
    "$(echo "$name" | sed 's/"/\\"/g')" \
    "$status" \
    "$(echo "$msg" | sed 's/"/\\"/g')" \
    "$escaped_detail")")
}

# Helpers
read_file_snippet() {
  local path="$1"; local lines="${2:-40}"
  if [ -f "$path" ]; then
    sed -n "1,${lines}p" "$path"
  else
    echo ""
  fi
}

# 1) Estrutura do projeto (template LaTeX e Makefile usando --template e xelatex)
check_template_exists() {
  local candidates
  candidates=$(sh -c "ls pipeline/premium/template*.tex 2>/dev/null || true")
  if [ -z "$candidates" ]; then
    if [ -f pipeline/premium/template-simple.tex ]; then
      candidates="pipeline/premium/template-simple.tex"
    fi
  fi

  if [ -n "$candidates" ]; then
    add_result "Template LaTeX" "PASS" "Encontrado template em pipeline/premium" "$candidates"
    TEMPLATE="$(echo "$candidates" | head -n1 | awk '{print $1}')"
  else
    add_result "Template LaTeX" "FAIL" "Nenhum template pipeline/premium/template*.tex ou template-simple.tex encontrado" ""
    TEMPLATE=""
  fi
}

check_makefile_flags() {
  local makefile="Makefile"
  if [ ! -f "$makefile" ]; then
    add_result "Makefile" "FAIL" "Makefile não encontrado" ""
    return
  fi

  local has_target
  has_target=$(grep -E "^[a-zA-Z0-9_-]+:.*" "$makefile" | rg -n "premium-pdf|pdf" || true)

  local contains_template contains_engine
  contains_template=$(sh -c "$FIND --hidden --no-ignore-vcs --no-line-number --only-matching --no-heading --glob 'Makefile' -- \"--template\" 2>/dev/null || true")
  contains_engine=$(sh -c "$FIND --hidden --no-ignore-vcs --no-line-number --only-matching --no-heading --glob 'Makefile' -- \"--pdf-engine=xelatex\" 2>/dev/null || true")

  if [ -n "$contains_template" ] && [ -n "$contains_engine" ] && (echo "$has_target" | rg -q "premium-pdf|pdf" >/dev/null 2>&1 || true); then
    add_result "Makefile -> Pandoc flags" "PASS" "Makefile tem referência a --template e --pdf-engine=xelatex em regra de build (ex: premium-pdf / pdf)" "$(sed -n '1,160p' Makefile)"
  else
    add_result "Makefile -> Pandoc flags" "FAIL" "Makefile não aparenta chamar pandoc com --template ... e --pdf-engine=xelatex (procure por premium-pdf/pdf target e flags --template/--pdf-engine=xelatex)" "$(sed -n '1,160p' Makefile)"
  fi
}

# 2) Front matter e sumário
check_toc_and_frontmatter() {
  local pdf
  pdf=$(ls -1 dist/*.pdf 2>/dev/null | head -n1 || true)
  local pdftxt=""
  if [ -z "$pdf" ]; then
    add_result "TOC/Front matter (PDF)" "WARN" "PDF não encontrado em dist/*.pdf — tente gerar com make premium-pdf" ""
    return
  fi

  if has pdftotext; then
    pdftotext "$pdf" - | sed -n '1,300p' > "${OUTDIR}/pdf_text_snippet.txt"
    pdftxt=$(cat "${OUTDIR}/pdf_text_snippet.txt")
    if echo "$pdftxt" | rg -q "Sumário"; then
      if ! echo "$pdftxt" | rg -q "CONTEÚDO"; then
        add_result "TOC aparece como 'Sumário'" "PASS" "Sumário encontrado e CONTEÚDO não encontrado" "$(echo "$pdftxt" | head -n50)"
      else
        add_result "TOC aparece como 'Sumário'" "FAIL" "Texto 'CONTEÚDO' apareceu no PDF (esperado 'Sumário')" "$(echo "$pdftxt" | head -n50)"
      fi
    else
      add_result "TOC aparece como 'Sumário'" "FAIL" "Não encontrei 'Sumário' no texto do PDF (procure por cabeçalhos do índice)" "$(echo "$pdftxt" | head -n50)"
    fi
  else
    add_result "TOC/Front matter (PDF)" "WARN" "pdftotext não disponível — não é possível inspecionar texto do PDF" ""
  fi

  # Inspecionar .tex para \frontmatter / \mainmatter ou \pagenumbering{roman}
  if [ -n "$TEMPLATE" ] && [ -f "$TEMPLATE" ]; then
    local tmpl_snip
    tmpl_snip=$(sed -n '1,240p' "$TEMPLATE")
    if echo "$tmpl_snip" | rg -q "\\\\pagenumbering\\{roman\\}|\\\\frontmatter|\\\\mainmatter"; then
      add_result "Front matter no template" "PASS" "Template contém marcações esperadas de front/mainmatter ou pagenumbering{roman}" "$(echo "$tmpl_snip" | head -n80)"
    else
      add_result "Front matter no template" "WARN" "Não encontrei \\frontmatter / \\mainmatter / \\pagenumbering{roman} no template — verifique se a separação de numeração está sendo feita" "$(echo "$tmpl_snip" | head -n80)"
    fi
  fi
}

# 3) Capítulos em dist/manuscrito_limpo.md
check_chapters() {
  local mdfile="dist/manuscrito_limpo.md"
  if [ ! -f "$mdfile" ]; then
    add_result "Capítulos (manuscrito)" "FAIL" "dist/manuscrito_limpo.md não encontrado" ""
    return
  fi
  local heads
  heads=$(grep -n "^# " "$mdfile" | sed -n '1,200p' || true)
  if [ -z "$heads" ]; then
    add_result "Capítulos (manuscrito)" "FAIL" "Não encontrei cabeçalhos de nível 1 em dist/manuscrito_limpo.md" ""
    return
  fi

  if echo "$heads" | rg -q "0\\.|Cap[ií]tulo .*0[0-9]"; then
    add_result "Capítulos (manuscrito)" "WARN" "Alguns capítulos aparentam ter prefixos 0.x ou 'Capítulo 01' — revise títulos" "$heads"
  else
    add_result "Capítulos (manuscrito)" "PASS" "Capítulos nível 1 parecem corretos" "$heads"
  fi
}

# 4) Geometry e head/foot
check_geometry() {
  local search_paths="pipeline/premium/*.tex *.tex"
  local geom
  geom=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' '\\\\geometry' 2>/dev/null || true")
  local headcfg
  headcfg=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' 'headheight|headsep|footskip' 2>/dev/null || true")

  local geom_ok=false
  if [ -n "$TEMPLATE" ] && [ -f "$TEMPLATE" ]; then
    if grep -q "inner=" "$TEMPLATE" && grep -q "outer=" "$TEMPLATE"; then
       geom_ok=true
    fi
  fi

  if [ "$geom_ok" = true ]; then
    add_result "Geometry" "PASS" "Found \\geometry with inner/outer in template" "$geom"
  else
    add_result "Geometry" "FAIL" "Não encontrei \\geometry{ inner=..., outer=... } no template" "$geom"
  fi

  if [ -n "$headcfg" ]; then
    add_result "Head/Foot config" "PASS" "Encontrado headheight/headsep/footskip" "$headcfg"
  else
    add_result "Head/Foot config" "WARN" "headheight/headsep/footskip não encontrados — verifique se há colisão de headers com texto" ""
  fi
}

# 5) Tipografia (setmainfont, microtype)
check_typography() {
  local typ
  typ=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' 'setmainfont|microtype|protrusion|expansion' 2>/dev/null || true")
  if [ -n "$typ" ]; then
    add_result "Tipografia" "PASS" "Encontrado configuração de fonte/microtype" "$typ"
  else
    add_result "Tipografia" "WARN" "Não encontrei \\setmainfont nem microtype/protrusion — pode haver fallback de fonte" ""
  fi

  # checar logs do XeLaTeX se existirem
  local log
  log=$(ls -1 build/*.log 2>/dev/null | head -n1 || true)
  if [ -n "$log" ] && [ -f "$log" ]; then
    if rg -n "Font .* not found|font not found" "$log" >/dev/null 2>&1; then
      add_result "Font warnings (log)" "FAIL" "Warnings de fonte encontrados no log do LaTeX" "$(sed -n '1,200p' "$log")"
    else
      add_result "Font warnings (log)" "PASS" "Nenhuma mensagem óbvia de 'font not found' no log" "$(sed -n '1,120p' "$log")"
    fi
  else
    add_result "Font warnings (log)" "WARN" "Log do LaTeX não encontrado em build/*.log — rode o build para gerar logs" ""
  fi
}

# 6) Boxes (mdframed, redefinição de quote)
check_boxes() {
  local boxes
  boxes=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' 'mdframed|newmdenv|renewenvironment\\{quote\\}' 2>/dev/null || true")
  if [ -n "$boxes" ]; then
    add_result "Boxes clínicos" "PASS" "Pacote/mdframed ou redefinição de quote encontrada" "$boxes"
  else
    add_result "Boxes clínicos" "WARN" "mdframed/newmdenv/renewenvironment{quote} não encontrados no template — blockquotes podem não virar boxes" ""
  fi
}

# 7) Figuras (captions, maxwidth)
check_figures() {
  local texs
  texs=$(sh -c "ls pipeline/premium/*.tex 2>/dev/null || true")
  local fig_info
  fig_info=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' '\\\\includegraphics|\\\\maxwidth|\\\\maxheight|caption' 2>/dev/null || true")
  if [ -n "$fig_info" ]; then
    add_result "Figuras" "PASS" "Encontradas referências a includegraphics/caption/maxwidth nos templates/tex" "$fig_info"
  else
    add_result "Figuras" "WARN" "Não encontrei veelhas óbvias de tratamento de figuras (\\maxwidth/\\maxheight/caption). Inspecione manualmente." ""
  fi
}

# 8) Hifenização/idioma
check_language() {
  local lang
  lang=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' 'polyglossia|babel|setmainlanguage|portuguese|brazil' 2>/dev/null || true")
  if [ -n "$lang" ]; then
    add_result "Idioma / hifenização" "PASS" "Configuração de idioma encontrada" "$lang"
  else
    add_result "Idioma / hifenização" "WARN" "Nenhuma configuração clara de babel/polyglossia encontrada — risco de hifenização incorreta" ""
  fi
}

# 9) Headers/footers/paginação (inspeção superficial)
check_headers_footers() {
  local hf
  hf=$(sh -c "$FIND --hidden --no-ignore-vcs -g 'pipeline/premium/*.tex' -g '*.tex' 'fancyhdr|headheight|headsep|footskip|pagestyle' 2>/dev/null || true")
  if [ -n "$hf" ]; then
    add_result "Headers/Footers" "PASS" "Configuração de cabeçalhos/rodapés encontrada" "$hf"
  else
    add_result "Headers/Footers" "WARN" "Não encontrei fancyhdr/headheight/headsep/footskip/pagestyle claramente definidos" ""
  fi
}

# 10) Integração no Makefile (make premium-pdf e idempotência)
check_make_integration() {
  if has make; then
    # detect timeout command (GNU timeout or gtimeout on macOS via coreutils)
    TIMEOUT_CMD=""
    if command -v timeout >/dev/null 2>&1; then
      TIMEOUT_CMD="timeout 600"
    elif command -v gtimeout >/dev/null 2>&1; then
      TIMEOUT_CMD="gtimeout 600"
    fi

    echo "Executando: make clean && make premium-pdf..."
    if [ -n "$TIMEOUT_CMD" ]; then
      if $TIMEOUT_CMD bash -lc "make clean && make premium-pdf" > "${OUTDIR}/make_premium_output.txt" 2>&1; then
        add_result "make premium-pdf" "PASS" "make premium-pdf executou sem erro" "$(sed -n '1,240p' ${OUTDIR}/make_premium_output.txt)"
        # verificar existência do PDF
        local pdfs
        pdfs=$(ls -1 dist/*.pdf 2>/dev/null || true)
        if [ -n "$pdfs" ]; then
          add_result "PDF gerado" "PASS" "PDF(s) encontrados em dist/: $(echo "$pdfs" | tr '\n' ' ')" ""
        else
          add_result "PDF gerado" "FAIL" "make premium-pdf não produziu dist/*.pdf visível" "$(sed -n '1,240p' ${OUTDIR}/make_premium_output.txt)"
        fi
      else
        add_result "make premium-pdf" "FAIL" "make premium-pdf falhou ou excedeu timeout" "$(sed -n '1,240p' ${OUTDIR}/make_premium_output.txt)"
      fi
    else
      echo "WARN: no timeout found — running make without timeout" > "${OUTDIR}/make_premium_output.txt"
      if bash -lc "make clean && make premium-pdf" >> "${OUTDIR}/make_premium_output.txt" 2>&1; then
        add_result "make premium-pdf" "PASS" "make premium-pdf executou sem erro (sem timeout)" "$(sed -n '1,240p' ${OUTDIR}/make_premium_output.txt)"
        # verificar existência do PDF
        local pdfs
        pdfs=$(ls -1 dist/*.pdf 2>/dev/null || true)
        if [ -n "$pdfs" ]; then
          add_result "PDF gerado" "PASS" "PDF(s) encontrados em dist/: $(echo "$pdfs" | tr '\n' ' ')" ""
        else
          add_result "PDF gerado" "FAIL" "make premium-pdf não produziu dist/*.pdf visível" "$(sed -n '1,240p' ${OUTDIR}/make_premium_output.txt)"
        fi
      else
        add_result "make premium-pdf" "FAIL" "make premium-pdf falhou (sem timeout)" "$(sed -n '1,240p' ${OUTDIR}/make_premium_output.txt)"
      fi
    fi
  else
    add_result "make premium-pdf" "WARN" "make não disponível nesta máquina" ""
  fi
}

# Run checks
check_template_exists
check_makefile_flags
check_chapters
check_geometry
check_typography
check_boxes
check_figures
check_language
check_headers_footers
check_toc_and_frontmatter
check_make_integration

# Emitir relatórios
# Markdown
{
  echo "# Relatório de verificação: premium (gerado em $(date -u +"%Y-%m-%dT%H:%M:%SZ"))"
  echo
  echo "Resumo por item:"
  echo
  for item in "${results[@]}"; do
    name=$(echo "$item" | sed 's/.*"name":"\([^"]*\)".*/\1/')
    status=$(echo "$item" | sed 's/.*"status":"\([^"]*\)".*/\1/')
    message=$(echo "$item" | sed 's/.*"message":"\([^"]*\)".*/\1/')
    detail=$(echo "$item" | sed 's/.*"detail":"\([^"]*\)".*/\1/')
    echo "## $name — $status"
    echo
    [ -n "$message" ] && echo "$message"
    echo
    if [ -n "$detail" ]; then
      echo '```'
      echo "$detail" | sed 's/\\n/\n/g'
      echo '```'
    fi
    echo
  done

  # Small hints
  echo "### Observações"
  echo "- Este script faz checagens heurísticas. Inspeção visual pode ser necessária para casos de layout/boxes/figuras."
  echo "- Se quiser, conecte este script ao CI e faça o Ralph executar repetidamente até PASS."
} > "$REPORT_MD"

# JSON
{
  echo "{"
  echo "  \"generated_at\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\","
  echo "  \"results\": ["
  first=true
  for item in "${results[@]}"; do
    if [ "$first" = true ]; then
      first=false
    else
      echo "    ,"
    fi
    # item already JSON-ish
    echo "    $item"
  done
  echo
  echo "  ]"
  echo "}"
} > "$REPORT_JSON"

# Print summary to stdout and exit code
echo
echo "Relatório gerado:"
echo " - Markdown: $REPORT_MD"
echo " - JSON:     $REPORT_JSON"
echo
# any FAIL?
if echo "${results[@]}" | rg -q '"status":"FAIL"' >/dev/null 2>&1; then
  echo "Algumas verificações falharam. Veja $REPORT_MD"
  exit 2
else
  echo "Nenhuma falha detectada nas checagens automatizadas (ou apenas WARN)."
  exit 0
fi
