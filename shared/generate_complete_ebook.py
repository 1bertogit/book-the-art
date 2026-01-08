#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gerador de eBook Completo (.md + .docx) + Prompts de Imagens AI

Uso:
    python generate_complete_ebook.py

Gera:
    - ebook_completo.md (todos os capítulos consolidados)
    - ebook_completo.docx (via Pandoc)
    - image_prompts_ai.md (prompts para regenerar imagens no AI)
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Ordem correta dos arquivos baseada em 00_SUMARIO_MESTRE.md
CHAPTER_FILES = [
    "00-notas-legais-escopo-e-uso-respons-vel-educacional.md",
    "01-introdu-o-a-filosofia-do-rejuvenescimento-operar-rejuvenescer.md",
    "02-luz-e-sombra-unidades-est-ticas-e-continuidade-periorbit-ria.md",
    "03-envelhecimento-multifatorial-deflation-ligamentos-e-osso.md",
    "04-anatomia-cir-rgica-aplicada-lamelas-septo-e-ligamentos-retentores.md",
    "05-mapas-de-risco-e-erros-de-plano-zonas-de-seguran-a-vs-perigo.md",
    "06-checklist-mental-do-resultado-nota-10-princ-pios-replic-veis.md",
    "07-fotodocumenta-o-estrat-gica-sem-flash-com-flash-e-padroniza-o.md",
    "08-exame-f-sico-vetores-flacidez-testes-e-assimetrias.md",
    "09-consulta-e-expectativa-alinhar-pedido-do-paciente-com-necessidade-anat-mica.md",
    "10-algoritmos-por-fen-tipo-superior-inferior-ter-o-m-dio-e-casos-mistos.md",
    "11-marca-o-e-medidas-superior-e-inferior-conservadorismo-e-simetria.md",
    "12-anestesia-infiltra-o-hemostasia-e-p-s-imediato-seguran-a.md",
    "13-brow-management-por-que-blef-isolada-falha-connell-e-indica-es.md",
    "14-tecnicas-de-brow-lift-temporal-endosc-pico-casta-ares-modificado.md",
    "15-blefaroplastia-superior-pele-gordura-preserva-o-e-gl-ndula-lacrimal.md",
    "16-ptose-associada-no-superior-quando-reconhecer-e-como-integrar-ao-plano.md",
    "17-palpebra-inferior-transconjuntival-prefer-ncias-septo-e-bolsas.md",
    "18-transposi-o-redistribui-o-de-gordura-sulco-nasojugal-e-transi-o-p-lpebra-malar.md",
    "19-manejo-de-pele-no-inferior-pinch-e-refinamentos-sem-descolamento-amplo.md",
    "20-festoon-edema-malar-fisiopatologia-e-op-es-orbicular-espa-o-pr-malar-cauteriza-o.md",
    "21-sustenta-o-quando-cantopexia-resolve-e-quando-n-o-resolve.md",
    "22-cantopexia-vs-cantoplastia-indica-es-por-vetor-e-flacidez.md",
    "23-tecnicas-de-canto-lateral-mladick-tarsal-strip-e-mccord-e-varia-es.md",
    "24-microfat-coleta-preparo-e-inje-o-zonas-e-volumes-justa-periostal.md",
    "25-nanofat-e-qualidade-de-pele-cicatrizes-olheiras-textura-e-microagulhamento.md",
    "26-funcional-e-reconstru-o-ectr-pio-entr-pio-retra-o-e-princ-pios-das-lamelas.md",
    "27-reconstru-o-p-s-tumor-retalhos-cl-ssicos-tenzel-hughes-cutler-beard-mustard.md",
    "28-complica-es-revis-es-e-gest-o-preven-o-resgate-e-precifica-o.md",
    "99_BIBLIOGRAFIA.md"
]

# Mapeamento de links [[MOVE:CAP-XX]] para arquivos (baseado em MOVE_MAP.md)
MOVE_MAP = {
    "[[MOVE:CAP-15]]": "[→ Capítulo 15](./15-blefaroplastia-superior-pele-gordura-preserva-o-e-gl-ndula-lacrimal.md)",
    "[[MOVE:CAP-18]]": "[→ Capítulo 18](./18-transposi-o-redistribui-o-de-gordura-sulco-nasojugal-e-transi-o-p-lpebra-malar.md)",
    "[[MOVE:CAP-22]]": "[→ Capítulo 22](./22-cantopexia-vs-cantoplastia-indica-es-por-vetor-e-flacidez.md)",
    "[[MOVE:CAP-25]]": "[→ Capítulo 25](./25-nanofat-e-qualidade-de-pele-cicatrizes-olheiras-textura-e-microagulhamento.md)",
}

# Descrições dos capítulos para gerar prompts de imagens AI
CHAPTER_CONTEXTS = {
    "01": "Filosofia do rejuvenescimento periorbitário: diferença entre operar e rejuvenescer, conceito de harmonia facial",
    "02": "Luz, sombra e unidades estéticas da região periorbitária: análise de continuidade e transições estéticas",
    "03": "Envelhecimento multifatorial: deflação, ligamentos envelhecidos, reabsorção óssea orbital",
    "04": "Anatomia cirúrgica aplicada: lamelas palpebrais, septo orbital, ligamentos retentores (ORL, ZCL)",
    "05": "Mapas de risco cirúrgico: zonas de segurança vs perigo, planos anatômicos, estruturas neurovasculares",
    "07": "Fotodocumentação estratégica: técnica sem flash vs com flash, padronização de ângulos e iluminação",
    "08": "Exame físico periorbitário: análise de vetores, testes de flacidez, snap test, avaliação de assimetrias",
    "09": "Consulta e expectativa: alinhamento entre pedido estético do paciente e necessidade anatômica real",
    "10": "Algoritmos por fenótipo: superior isolado, inferior isolado, terço médio, casos mistos",
    "11": "Marcação e medidas: técnica de marcação superior e inferior, conservadorismo, busca de simetria",
    "12": "Anestesia e hemostasia: infiltração anestésica, controle hemostático, cuidados pós-imediato",
    "13": "Brow management: por que blefaroplastia isolada falha, critérios de Connell, indicações de brow lift",
    "14": "Técnicas de brow lift: temporal, endoscópico, Castañares modificado, comparação de resultados",
    "15": "Blefaroplastia superior: ressecção de pele, manejo de gordura com preservação, glândula lacrimal",
    "16": "Ptose palpebral associada: reconhecimento, avaliação da função do levador, integração ao plano cirúrgico",
    "17": "Pálpebra inferior transconjuntival: técnica, preferências, abordagem do septo, remoção de bolsas",
    "18": "Transposição de gordura: redistribuição para sulco nasojugal, transição pálpebra-malar, técnicas",
    "19": "Manejo de pele inferior: skin pinch, refinamentos sem descolamento amplo, preservação de estruturas",
    "20": "Festoon e edema malar: fisiopatologia, opções de tratamento (orbicular, pré-malar, cauterização)",
    "21": "Sustentação palpebral: quando cantopexia resolve, quando não resolve, análise de flacidez",
    "22": "Cantopexia vs cantoplastia: diferenças, indicações por vetor e grau de flacidez ligamentar",
    "23": "Técnicas de canto lateral: Mladick, Tarsal Strip, McCord e suas variações, comparação",
    "24": "Microfat: coleta, preparo, injeção justa-periostal, zonas e volumes periorbital, técnica",
    "25": "Nanofat: qualidade de pele, tratamento de cicatrizes, olheiras, textura, microagulhamento combinado",
    "26": "Cirurgia funcional e reconstrução: ectrópio, entrópio, retração palpebral, princípios das lamelas",
    "27": "Reconstrução pós-tumor: retalhos clássicos (Tenzel, Hughes, Cutler-Beard, Mustardé), indicações",
    "28": "Complicações e revisões: prevenção, estratégias de resgate, gestão de expectativas, precificação"
}


def replace_move_links(content):
    """Substitui links [[MOVE:CAP-XX]] pelos links corretos"""
    for old, new in MOVE_MAP.items():
        content = content.replace(old, new)
    return content


def extract_images_from_content(content, chapter_num):
    """Extrai referências de imagens do conteúdo"""
    pattern = r'!\[([^\]]*)\]\((assets/figures/FIG-\d+-\d+[^\)]*)\)'
    matches = re.findall(pattern, content)
    images = []
    for alt_text, img_path in matches:
        images.append({
            'chapter': chapter_num,
            'alt': alt_text,
            'path': img_path,
            'filename': os.path.basename(img_path)
        })
    return images


def generate_ebook_md():
    """Gera o ebook_completo.md"""
    print("🔨 Gerando ebook_completo.md...")
    
    content_dir = Path("content")
    all_content = []
    all_images = []
    
    # Cabeçalho do ebook
    all_content.append("---")
    all_content.append("title: \"The Art of Eyelid Surgery\"")
    all_content.append("subtitle: \"Do Diagnóstico Preciso ao Rejuvenescimento do Olhar: Técnicas Avançadas em Cirurgia Periorbitária\"")
    all_content.append("author: \"Dr. Marcelo Curi\"")
    all_content.append("date: \"2026\"")
    all_content.append("language: \"pt-BR\"")
    all_content.append("---")
    all_content.append("\n")
    
    # Processar cada capítulo
    for filename in CHAPTER_FILES:
        filepath = content_dir / filename
        
        if not filepath.exists():
            print(f"⚠️  Arquivo não encontrado: {filename}")
            continue
        
        print(f"   Processando: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir links [[MOVE:CAP-XX]]
        content = replace_move_links(content)
        
        # Extrair imagens (para gerar prompts depois)
        chapter_match = re.search(r'(\d+)-', filename)
        if chapter_match:
            chapter_num = chapter_match.group(1)
            images = extract_images_from_content(content, chapter_num)
            all_images.extend(images)
        
        # Adicionar conteúdo com separador de página
        all_content.append(content)
        all_content.append("\n\n\\newpage\n\n")
    
    # Salvar ebook_completo.md
    output_md = "ebook_completo.md"
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_content))
    
    print(f"✅ {output_md} gerado com sucesso!")
    return output_md, all_images


def generate_docx(md_file):
    """Converte .md para .docx usando Pandoc"""
    print("\n🔨 Gerando ebook_completo.docx via Pandoc...")
    
    # Verificar se Pandoc está instalado
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        print(f"   Pandoc encontrado: {result.stdout.split()[1]}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERRO: Pandoc não encontrado!")
        print("   Instale o Pandoc:")
        print("   - macOS: brew install pandoc")
        print("   - Linux: sudo apt install pandoc")
        print("   - Windows: https://pandoc.org/installing.html")
        return False
    
    # Converter usando Pandoc
    output_docx = "ebook_completo.docx"
    cmd = [
        'pandoc',
        md_file,
        '-o', output_docx,
        '--toc',  # Gerar índice
        '--toc-depth=3',
        '--highlight-style=tango',
        '-V', 'geometry:margin=2.5cm',
        '-V', 'fontsize=11pt',
        '-V', 'linestretch=1.5'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ {output_docx} gerado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar DOCX: {e}")
        return False


def generate_ai_prompts(images):
    """Gera arquivo com prompts para regenerar imagens no AI"""
    print("\n🔨 Gerando image_prompts_ai.md...")
    
    output = []
    output.append("# Prompts para Geração de Imagens no AI (Nano Banana ou similar)\n")
    output.append("Este arquivo contém prompts detalhados para regenerar todas as imagens do ebook.\n")
    output.append("---\n\n")
    
    # Agrupar imagens por capítulo
    images_by_chapter = {}
    for img in images:
        ch = img['chapter']
        if ch not in images_by_chapter:
            images_by_chapter[ch] = []
        images_by_chapter[ch].append(img)
    
    # Gerar prompts
    for chapter in sorted(images_by_chapter.keys()):
        imgs = images_by_chapter[chapter]
        context = CHAPTER_CONTEXTS.get(chapter, "Cirurgia periorbitária")
        
        output.append(f"## Capítulo {chapter}\n")
        output.append(f"**Contexto**: {context}\n\n")
        
        for img in imgs:
            output.append(f"### {img['filename']}\n")
            output.append(f"**Alt text original**: {img['alt']}\n\n")
            output.append("**Prompt sugerido para AI**:\n")
            output.append("```\n")
            
            # Gerar prompt detalhado baseado no contexto
            prompt = f"""Medical illustration, educational style, high quality anatomical diagram.
Subject: {context}
Style: Clean, professional medical textbook illustration with labels in Portuguese (Brazil).
Technical requirements:
- High resolution, suitable for print
- Clear anatomical structures
- Professional color palette (medical blue, neutral tones)
- Annotations and arrows pointing to key structures
- Cross-sectional or frontal view as appropriate
- Emphasis on surgical landmarks and safety zones
Context: Oculoplastic surgery / eyelid surgery / periorbital rejuvenation
Target audience: Plastic surgeons and oculoplastic specialists
"""
            output.append(prompt)
            output.append("```\n\n")
            output.append("---\n\n")
    
    # Nota adicional
    output.append("\n## Instruções Gerais\n\n")
    output.append("1. Use estes prompts como base e ajuste conforme necessário\n")
    output.append("2. Mantenha consistência visual entre todas as figuras\n")
    output.append("3. Adicione labels em português (Brasil)\n")
    output.append("4. Priorize clareza sobre realismo fotográfico\n")
    output.append("5. Salve as imagens geradas em `assets/figures/` com os nomes corretos\n")
    
    # Salvar arquivo
    output_file = "image_prompts_ai.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(output))
    
    print(f"✅ {output_file} gerado com {len(images)} prompts de imagens!")


def main():
    """Função principal"""
    print("=" * 60)
    print("  GERADOR DE EBOOK COMPLETO + PROMPTS DE IMAGENS AI")
    print("  The Art of Eyelid Surgery - Dr. Marcelo Curi")
    print("=" * 60)
    print()
    
    # 1. Gerar ebook_completo.md
    md_file, images = generate_ebook_md()
    
    # 2. Gerar ebook_completo.docx
    generate_docx(md_file)
    
    # 3. Gerar prompts de imagens AI
    generate_ai_prompts(images)
    
    print("\n" + "=" * 60)
    print("✅ PROCESSO COMPLETO!")
    print("=" * 60)
    print(f"\nArquivos gerados:")
    print(f"  📄 ebook_completo.md")
    print(f"  📘 ebook_completo.docx")
    print(f"  🎨 image_prompts_ai.md ({len(images)} prompts)")
    print(f"\n💡 Próximos passos:")
    print(f"  1. Abra ebook_completo.docx no Word")
    print(f"  2. Revise formatação e ajuste conforme necessário")
    print(f"  3. Use image_prompts_ai.md para gerar as imagens no AI")
    print(f"  4. Insira as imagens manualmente no documento Word")
    print()


if __name__ == "__main__":
    main()