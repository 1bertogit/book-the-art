# MOVE_MAP — Resolução de links internos

## Regra de substituição (padrão recomendado)
Dentro dos arquivos em `content/`, substitua:

- `[[MOVE:CAP-XX]]`

por:

- `[→ Capítulo XX](./<arquivo-do-cap-XX>.md)`

> Nota: use `./` porque os capítulos estão no mesmo diretório (`content/`).

---

## Mapa CAP → Arquivo

| CAP | Arquivo |
|---:|---|
| CAP-00 | 00-notas-legais-escopo-e-uso-responsavel-educacional.md |
| CAP-01 | 01-introducao-a-filosofia-do-rejuvenescimento-operar-rejuvenescer.md |
| CAP-02 | 02-luz-e-sombra-unidades-esteticas-e-continuidade-periorbitaria.md |
| CAP-03 | 03-envelhecimento-multifatorial-deflacao-ligamentos-e-osso.md |
| CAP-04 | 04-anatomia-cirurgica-aplicada-lamelas-septo-e-ligamentos-retentores.md |
| CAP-05 | 05-mapas-de-risco-e-erros-de-plano-zonas-de-seguranca-vs-perigo.md |
| CAP-06 | 06-checklist-mental-do-resultado-nota-10-principios-replicaveis.md |
| CAP-07 | 07-fotodocumentacao-estrategica-sem-flash-com-flash-e-padronizacao.md |
| CAP-08 | 08-exame-fisico-vetores-flacidez-testes-e-assimetrias.md |
| CAP-09 | 09-consulta-e-expectativa-alinhar-pedido-do-paciente-com-necessidade-anatomica.md |
| CAP-10 | 10-algoritmos-por-fenotipo-superior-inferior-terco-medio-e-casos-mistos.md |
| CAP-11 | 11-marcacao-e-medidas-superior-e-inferior-conservadorismo-e-simetria.md |
| CAP-12 | 12-anestesia-infiltracao-hemostasia-e-pos-imediato-seguranca.md |
| CAP-13 | 13-brow-management-por-que-blef-isolada-falha-connell-e-indicacoes.md |
| CAP-14 | 14-tecnicas-de-brow-lift-temporal-endoscopico-castanares-modificado.md |
| CAP-15 | 15-blefaroplastia-superior-pele-gordura-preservacao-e-glandula-lacrimal.md |
| CAP-16 | 16-ptose-associada-no-superior-quando-reconhecer-e-como-integrar-ao-plano.md |
| CAP-17 | 17-palpebra-inferior-transconjuntival-preferencias-septo-e-bolsas.md |
| CAP-18 | 18-transposicao-redistribuicao-de-gordura-sulco-nasojugal-e-transicao-palpebra-malar.md |
| CAP-19 | 19-manejo-de-pele-no-inferior-pinch-e-refinamentos-sem-descolamento-amplo.md |
| CAP-20 | 20-festoon-edema-malar-fisiopatologia-e-opcoes-orbicular-espaco-pre-malar-cauterizacao.md |
| CAP-21 | 21-sustentacao-quando-cantopexia-resolve-e-quando-nao-resolve.md |
| CAP-22 | 22-cantopexia-vs-cantoplastia-indicacoes-por-vetor-e-flacidez.md |
| CAP-23 | 23-tecnicas-de-canto-lateral-mladick-tarsal-strip-e-mccord-e-variacoes.md |
| CAP-24 | 24-microfat-coleta-preparo-e-injecao-zonas-e-volumes-justa-periostal.md |
| CAP-25 | 25-nanofat-e-qualidade-de-pele-cicatrizes-olheiras-textura-e-microagulhamento.md |
| CAP-26 | 26-funcional-e-reconstrucao-ectropio-entropio-retracao-e-principios-das-lamelas.md |
| CAP-27 | 27-reconstrucao-pos-tumor-retalhos-classicos-tenzel-hughes-cutler-beard-mustarde.md |
| CAP-28 | 28-complicacoes-revisoes-e-gestao-prevencao-resgate-e-precificacao.md |

---

## Ocorrências `[[MOVE]]` já identificadas (com substituição)

### Em CAP-14
- Original: `[[MOVE:CAP-15]]`
- Substituir por: `[→ Capítulo 15](./15-blefaroplastia-superior-pele-gordura-preservacao-e-glandula-lacrimal.md)`

### Em CAP-17
- Original: `[[MOVE:CAP-18]]`
- Substituir por: `[→ Capítulo 18](./18-transposicao-redistribuicao-de-gordura-sulco-nasojugal-e-transicao-palpebra-malar.md)`

### Em CAP-21
- Original: `[[MOVE:CAP-22]]`
- Substituir por: `[→ Capítulo 22](./22-cantopexia-vs-cantoplastia-indicacoes-por-vetor-e-flacidez.md)`

### Em CAP-24
- Original: `[[MOVE:CAP-25]]`
- Substituir por: `[→ Capítulo 25](./25-nanofat-e-qualidade-de-pele-cicatrizes-olheiras-textura-e-microagulhamento.md)`

### Em CAP-26
- Original: `[[MOVE:CAP-22]]`
- Substituir por: `[→ Capítulo 22](./22-cantopexia-vs-cantoplastia-indicacoes-por-vetor-e-flacidez.md)`

---

## Opcional (sanidade): varredura rápida
Procure por `[[MOVE:` e `[[REF]]` para listar pendências remanescentes.
