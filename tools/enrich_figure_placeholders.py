#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enriquece placeholders de figuras sugeridas com prompts detalhados.

Analisa o contexto (capítulo, seção) e gera descrições mais úteis
para o ilustrador/designer.

Uso:
    python3 tools/enrich_figure_placeholders.py --dry-run   # Preview
    python3 tools/enrich_figure_placeholders.py --apply     # Aplicar
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "projects" / "eyelid-surgery" / "content"

# Mapeamento de capítulos para contexto de figuras
CHAPTER_CONTEXT = {
    "01": {
        "tema": "Filosofia do Rejuvenescimento",
        "figuras": [
            "Diagrama comparativo: 'Operar' vs 'Rejuvenescer' — mostrando abordagem fragmentada vs holística",
            "Ilustração: Continuidade de luz e sombra na face — como a intervenção deve preservar a harmonia"
        ]
    },
    "02": {
        "tema": "Luz e Sombra, Unidades Estéticas",
        "figuras": [
            "Mapa das unidades estéticas periorbitárias — demarcação de fronteiras e transições",
            "Diagrama de incidência de luz: como sombras revelam volumes e depressões"
        ]
    },
    "03": {
        "tema": "Envelhecimento Multifatorial",
        "figuras": [
            "Diagrama comparativo: Deflação vs Ptose vs Excesso de pele",
            "Ilustração anatômica: Ligamentos retentores e sua frouxidão com idade"
        ]
    },
    "04": {
        "tema": "Anatomia Cirúrgica Aplicada",
        "figuras": [
            "Corte sagital da pálpebra: Lamelas anterior e posterior, septo, tarso",
            "Vista frontal: Ligamentos retentores, gordura pré-aponeurótica, ROOF/SOOF"
        ]
    },
    "05": {
        "tema": "Mapas de Risco e Zonas de Segurança",
        "figuras": [
            "Mapa de risco cirúrgico: Zonas verdes (seguras), amarelas (atenção), vermelhas (perigo)",
            "Diagrama: Planos de dissecção seguros vs arriscados por região"
        ]
    },
    "06": {
        "tema": "Checklist Mental do Resultado Nota 10",
        "figuras": [
            "Infográfico: Checklist visual do resultado ideal — simetria, volume, contorno"
        ]
    },
    "07": {
        "tema": "Fotodocumentação Estratégica",
        "figuras": [
            "Comparativo: Foto sem flash (revela sombras/volumes) vs com flash (achata)",
            "Diagrama: Posições padronizadas para documentação (frontal, oblíqua, perfil)"
        ]
    },
    "08": {
        "tema": "Exame Físico: Vetores e Testes",
        "figuras": [
            "Diagrama: Vetor positivo vs neutro vs negativo — relação globo/malar",
            "Ilustração: Snap-back test e Distraction test — execução e interpretação",
            "Diagrama: Medida de MRD1 e MRD2"
        ]
    },
    "09": {
        "tema": "Consulta e Alinhamento de Expectativas",
        "figuras": [
            "Fluxograma: Queixa do paciente → Hipótese anatômica → Plano cirúrgico",
            "Diagrama: 'O que o paciente vê' vs 'O que o cirurgião deve corrigir'"
        ]
    },
    "10": {
        "tema": "Algoritmos por Fenótipo",
        "figuras": [
            "Fluxograma de decisão: Superior / Inferior / Terço médio / Casos mistos",
            "Árvore de decisão: Baseada em vetor, tônus, tear trough, festoon"
        ]
    },
    "11": {
        "tema": "Marcação e Medidas",
        "figuras": [
            "Diagrama de marcação superior: Linha do sulco + fuso, extensão lateral em RSTL",
            "Diagrama de marcação inferior: Técnica de skin pinch"
        ]
    },
    "12": {
        "tema": "Anestesia e Infiltração",
        "figuras": [
            "Mapa de pontos de bloqueio anestésico periorbitário",
            "Diagrama de planos de infiltração: Subcutâneo, pré-septal, pós-septal",
            "Sinal clínico: 'Blanching' como indicador de vasoconstrição"
        ]
    },
    "13": {
        "tema": "Brow Management",
        "figuras": [
            "Teste de Connell ilustrado: Bloqueio do frontal e observação da ptose",
            "Diagrama: Vetores de queda lateral do supercílio e 'capuz' lateral"
        ]
    },
    "14": {
        "tema": "Técnicas de Brow Lift",
        "figuras": [
            "Diagrama: Planos temporais (superficial vs profundo)",
            "Zona de perigo: Ramo temporal do nervo facial",
            "Vetores de tração: Direções oblíquo-laterais ideais"
        ]
    },
    "15": {
        "tema": "Blefaroplastia Superior",
        "figuras": [
            "Anatomia: Gordura pré-aponeurótica, glândula lacrimal, ROOF",
            "Técnica: Preservação vs ressecção conservadora de gordura"
        ]
    },
    "16": {
        "tema": "Ptose Associada",
        "figuras": [
            "Diagrama diagnóstico: MRD1, função do elevador, teste de fenilefrina",
            "Técnica: Acesso ao músculo de Müller e aponeurose"
        ]
    },
    "17": {
        "tema": "Pálpebra Inferior Transconjuntival",
        "figuras": [
            "Corte sagital: Acesso transconjuntival pré e pós-septal",
            "Anatomia: Compartimentos de gordura (nasal, central, lateral)"
        ]
    },
    "18": {
        "tema": "Transposição de Gordura",
        "figuras": [
            "Técnica: Fat repositioning para sulco nasojugal",
            "Diagrama: Transição pálpebra-malar ideal (continuidade)"
        ]
    },
    "19": {
        "tema": "Manejo de Pele no Inferior",
        "figuras": [
            "Técnica: Skin pinch — demarcação e excisão",
            "Comparativo: Com vs sem descolamento amplo"
        ]
    },
    "20": {
        "tema": "Festoon e Edema Malar",
        "figuras": [
            "Anatomia: Espaço pré-malar, músculo orbicular, SOOF",
            "Diagnóstico diferencial: Festoon vs malar mound vs bolsa"
        ]
    },
    "21": {
        "tema": "Sustentação: Quando Cantopexia Resolve",
        "figuras": [
            "Diagrama de decisão: Quando cantopexia é suficiente vs insuficiente",
            "Anatomia: Tendão cantal lateral e sua inserção"
        ]
    },
    "22": {
        "tema": "Cantopexia vs Cantoplastia",
        "figuras": [
            "Comparativo: Cantopexia (reforço) vs Cantoplastia (reconstrução)",
            "Indicações por vetor e grau de flacidez"
        ]
    },
    "23": {
        "tema": "Técnicas de Canto Lateral",
        "figuras": [
            "Técnica de Mladick: Passos ilustrados",
            "Lateral Tarsal Strip: Dissecção, preparação, fixação",
            "Técnica de McCord: Variações e indicações"
        ]
    },
    "24": {
        "tema": "Microfat",
        "figuras": [
            "Técnica de coleta: Seringa, cânula, processamento",
            "Mapa de injeção: Zonas periorbitárias, volumes, profundidade (justa-periostal)"
        ]
    },
    "25": {
        "tema": "Nanofat e Qualidade de Pele",
        "figuras": [
            "Processamento: Microfat → Nanofat (emulsificação)",
            "Aplicação: Técnica intradérmica, microagulhamento, zonas-alvo"
        ]
    },
    "26": {
        "tema": "Funcional e Reconstrução (Ectrópio, Entrópio, Retração)",
        "figuras": [
            "Diagnóstico: Ectrópio involucional vs cicatricial vs paralítico",
            "Princípio das lamelas: Enxerto vs retalho por camada"
        ]
    },
    "27": {
        "tema": "Reconstrução Pós-Tumor",
        "figuras": [
            "Retalho de Tenzel: Indicações e passos",
            "Retalho de Hughes: Técnica tarsoconjuntival",
            "Cutler-Beard: Reconstrução de pálpebra superior",
            "Mustardé: Reconstrução de canto lateral"
        ]
    },
    "28": {
        "tema": "Complicações, Revisões e Gestão",
        "figuras": [
            "Fluxograma: Prevenção → Reconhecimento → Resgate",
            "Algoritmo de gestão de complicações por gravidade"
        ]
    },
}


def get_chapter_number(filename: str) -> str:
    """Extrai número do capítulo do nome do arquivo."""
    match = re.match(r"(\d{2})-", filename)
    return match.group(1) if match else ""


def enrich_placeholder(line: str, chapter_num: str, fig_index: int) -> str:
    """Enriquece um placeholder de figura com contexto."""
    context = CHAPTER_CONTEXT.get(chapter_num, {})
    tema = context.get("tema", "")
    figuras = context.get("figuras", [])

    # Se temos sugestões específicas para este capítulo
    if figuras and fig_index < len(figuras):
        sugestao = figuras[fig_index]
    else:
        sugestao = f"Ilustração relacionada ao tema: {tema}" if tema else "Ilustração a definir"

    # Criar novo placeholder enriquecido
    return f"> **📎 FIGURA NECESSÁRIA (Cap. {chapter_num}):**\n> {sugestao}\n> *Estilo: Diagrama técnico-didático, cores neutras, legendas claras*"


def process_file(filepath: Path, dry_run: bool = True) -> dict:
    """Processa um arquivo e enriquece placeholders."""
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.name
    chapter_num = get_chapter_number(filename)

    # Encontrar todos os placeholders
    pattern = re.compile(r"^>\s*\*\*Figura sugerida[:\*]*.*$", re.MULTILINE | re.IGNORECASE)
    matches = list(pattern.finditer(text))

    stats = {
        "file": filename,
        "count": len(matches),
        "enriched": 0
    }

    if not matches:
        return stats

    # Processar de trás para frente
    new_text = text
    for i, match in enumerate(reversed(matches)):
        idx = len(matches) - 1 - i  # Índice original
        enriched = enrich_placeholder(match.group(), chapter_num, idx)
        new_text = new_text[:match.start()] + enriched + new_text[match.end():]
        stats["enriched"] += 1

    if not dry_run:
        filepath.write_text(new_text, encoding="utf-8")

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enriquece placeholders de figuras com prompts detalhados"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostrar mudanças sem aplicar"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplicar mudanças nos arquivos"
    )
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Especifique --dry-run ou --apply")
        return 1

    print("🎨 Enriquecendo placeholders de figuras...")
    print()

    files = sorted(CONTENT_DIR.glob("[0-9][0-9]-*.md"))
    total_enriched = 0

    for filepath in files:
        stats = process_file(filepath, dry_run=args.dry_run)
        if stats["count"] > 0:
            icon = "📄" if args.dry_run else "✅"
            print(f"  {icon} {stats['file']}: {stats['count']} placeholders")
            total_enriched += stats["enriched"]

    print()
    print(f"📊 Total: {total_enriched} placeholders enriquecidos")

    if args.dry_run:
        print("💡 Execute com --apply para aplicar as mudanças")
    else:
        print("✅ Placeholders enriquecidos!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
