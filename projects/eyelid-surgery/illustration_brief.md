# Brief Técnico e Checklist de Aceitação — Ilustração Médica

Este documento serve como a ponte entre o **Manuscrito Editorialmente Limpo** e a **Produção de Ilustração Médica**, garantindo que as novas figuras atendam aos padrões científicos e técnicos exigidos para "The Art of Eyelid Surgery".

---

## 1. Brief Técnico para o Ilustrador

### 1.1 Objetivos Estéticos
- **Estilo**: Didático-realista, premium.
- **Paleta de Cores**: Tons neutros e teciduais (pele, músculo, gordura, osso) com acentos claros para estruturas nobres (nervos em amarelo, artérias em vermelho, veias em azul).
- **Consistência**: Todos os 27 capítulos devem compartilhar a mesma "linguagem visual" (espessura de linha, estilo de seta, fonte de legenda).
- **Autoridade Visual**: Ausência total de estética "cartoon" ou exageros didáticos desnecessários. Preferência por proporções realistas, mesmo quando simplificadas.

### 1.2 Requisitos Anatômicos (Cruciais)
- **Nomenclatura**: Seguir rigorosamente a Terminologia Anatômica Internacional (em português).
- **Precisão**: Atenção especial ao **Septo Orbitário**, **Lamelas**, **Músculo Oblíquo Inferior** e **Ligamentos Retentores** (pontos críticos de erro nas versões IA).
- **Vetores**: Especificar sempre o **plano de referência** (ex.: Frankfurt horizontal ou eixo pupilar) e a natureza do vetor (gravitacional, tração cirúrgica ou eixo estético). Não misturar conceitos na mesma seta.

### 1.3 Formatos de Entrega
- **Matriz Vetorial (Fonte da Verdade)**: `.ai` ou `.svg` reais e editáveis. **Atenção:** Arquivos raster (pixels) encapsulados em SVG não serão aceitos.
- **Exportação Raster**: `.png` (transparente) e `.jpg` (fundo branco) em **300 DPI** obrigatórios para impressão.
- **Dimensões**: Manter consistência com o grid do PDF LaTeX (A4, margens de 2.5cm/3cm).

---

## 2. Checklist de Aceitação (Gate Oficial)

Uma figura **só pode** mudar de status (`ai-draft` → `final-ok`) se cumprir **todos** os critérios abaixo (condição necessária e suficiente):

- [ ] **Ortografia**: Zero erros de digitação nos labels (Checagem manual obrigatória).
- [ ] **Coerência de Plano**: A estrutura representada coincide com o nível de dissecção descrito no texto?
- [ ] **Legenda Verdadeira**: A imagem não "promete" mais do que mostra (fidelidade total ao caption).
- [ ] **Risco Explícito**: Zonas de perigo e estruturas nobres estão claramente destacadas (obrigatório em capítulos de segurança).
- [ ] **Legibilidade Dupla**: Os textos são legíveis tanto em escala de impressão (A4) quanto em e-reader (~6–8”).
- [ ] **Consistência Visual**: A figura respeita a identidade visual estabelecida para o restante da obra.

> **Regra:** Se qualquer item falhar, o status permanece `draft`. Sem exceções.

---

## 3. Fluxo de Substituição no Pipeline (Rastreável)

Para integrar a nova figura sem quebrar o build e mantendo histórico:

1. (Opcional) Mover a versão anterior para `projects/eyelid-surgery/assets/figures/_archive/` (para auditoria futura).
2. Salvar o novo arquivo na pasta `figures/` com o **exato mesmo nome** definido em `figures.yml`.
3. Executar `make build` e verificar a renderização no `00_MANUSCRITO.md`.
4. Atualizar o status no `figures_audit.md` para `final-ok` (somente se passou no Gate acima).
5. Gerar `make premium-pdf` para conferir sangria, margens e legibilidade final.

---
> [!IMPORTANT]
> A qualidade anatômica das figuras é o fator determinante para a aceitação do livro pela comunidade médica. Não aceite compromissos na precisão das inserções ligamentares e septais.
