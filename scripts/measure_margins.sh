#!/usr/bin/env bash
# measure_margins.sh
# Mede as margens reais (xMin) de páginas par e ímpar para validar o "gutter" (encadernação).

set -euo pipefail

PDF="${1:-dist/book_premium.pdf}"

if [ ! -f "$PDF" ]; then
  echo "Erro: Arquivo $PDF não encontrado."
  exit 1
fi

if ! command -v pdftotext >/dev/null 2>&1; then
  echo "Erro: pdftotext não encontrado. Instale com 'brew install poppler'."
  exit 1
fi

# páginas de amostra (par/ímpar) no miolo
EVEN_PAGE="${2:-4}"
ODD_PAGE="${3:-5}"

tmp_even="$(mktemp).html"
tmp_odd="$(mktemp).html"

echo "Analisando PDF: $PDF"
echo "Páginas de amostra: par=$EVEN_PAGE, ímpar=$ODD_PAGE"

pdftotext -bbox-layout -f "$EVEN_PAGE" -l "$EVEN_PAGE" "$PDF" "$tmp_even"
pdftotext -bbox-layout -f "$ODD_PAGE"  -l "$ODD_PAGE"  "$PDF" "$tmp_odd"

pt_to_mm() {
  if [ -z "$1" ]; then echo "0.00"; return; fi
  python3 -c "print(f'{float($1)*25.4/72:.2f}')"
}

min_x_line() {
  local f="$1"
  # pega xMin de <line ...> ignorando topo/rodapé extremos (margens de 80 a 760 pt de altura)
  local xmin
  xmin=$(perl -ne '
    if(/<line[^>]*xMin="([0-9.]+)".*yMin="([0-9.]+)"/){
      $x=$1; $y=$2;
      if($y>80 && $y<760){ print "$x\n"; }
    }
  ' "$f" | sort -n | head -n 1)
  echo "$xmin"
}

even_min_pt="$(min_x_line "$tmp_even")"
odd_min_pt="$(min_x_line "$tmp_odd")"

even_min_mm="$(pt_to_mm "$even_min_pt")"
odd_min_mm="$(pt_to_mm "$odd_min_pt")"

echo "--------------------------------------------------"
echo "Resultados da Medição de Margem Esquerda (xMin):"
echo "Página PAR ($EVEN_PAGE):  $even_min_pt pt (~$even_min_mm mm)"
echo "Página ÍMPAR ($ODD_PAGE): $odd_min_pt pt (~$odd_min_mm mm)"
echo "--------------------------------------------------"

# Explicação do resultado
# Em twoside (book):
# Página ÍMPAR (direita): Margem esquerda é a INNER (Gutter) -> Deve ser MAIOR.
# Página PAR (esquerda): Margem esquerda é a OUTER -> Deve ser MENOR.

diff_mm=$(python3 -c "print(f'{abs(float($odd_min_mm) - float($even_min_mm)):.2f}')")

if (( $(echo "$odd_min_pt > $even_min_pt" | bc -l) )); then
  echo "✅ Layout TWOSIDE detectado: A margem esquerda da página ímpar é $diff_mm mm maior que a da par."
  echo "   Isso confirma que o 'Gutter' (margem de encadernação) está configurado corretamente."
else
  echo "❌ Layout SIMÉTRICO: As margens parecem iguais ou invertidas. Verifique o template LaTeX."
fi

rm -f "$tmp_even" "$tmp_odd"
