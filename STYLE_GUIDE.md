# Style Guide — The Art of Eyelid Surgery

Este documento define as regras editoriais do livro. **Toda edição deve seguir estas diretrizes.**

---

## 1. Negrito

- **Uso restrito** a termos técnicos na primeira ocorrência do capítulo
- Máximo 2-3 palavras em negrito por parágrafo
- **Nunca** em frases inteiras
- Exceção: nomes de técnicas (ex: **Tarsal Strip**, **Müller-conjuntival**)

### Exemplos

✅ Correto:
> A **deflação volumétrica** é o mecanismo dominante.

❌ Errado:
> **A deflação volumétrica é o mecanismo dominante no envelhecimento.**

---

## 2. Boxes Clínicos

### Formato de entrada (nos arquivos .md):

```markdown
[[BOX: Pérola Clínica]]
Texto do box aqui.
[[/BOX]]
```

### Formato de saída (após build):

```markdown
> **PÉROLA CLÍNICA**  
> Texto do box aqui.
```

### Tipos permitidos:

| Tag no Markdown | Saída no Blockquote |
|-----------------|---------------------|
| `[[BOX: Pérola Clínica]]` | `> **PÉROLA CLÍNICA**` |
| `[[BOX: Atenção]]` | `> **ATENÇÃO**` |
| `[[BOX: Técnica]]` | `> **TÉCNICA**` |
| `[[BOX: Evidência]]` | `> **EVIDÊNCIA**` |
| `[[BOX: Regra de Ouro]]` | `> **REGRA DE OURO**` |
| `[[BOX]]` (sem título) | `> **NOTA CLÍNICA**` |

### Limite: máximo 3 boxes por capítulo

---

## 3. Headings (Títulos)

```markdown
# Título do Capítulo (único por arquivo)
## Seção Principal
### Subseção
```

- Máximo **3 níveis** de profundidade
- Nunca pular níveis (ex: `#` → `###`)
- Capitalização: primeira letra maiúscula, resto minúsculo
- **Exceção**: epônimos e termos técnicos mantêm capitalização correta (ex: "Sinal de Bell", "Lei de Hering", "Tarsal Strip")

---

## 4. Figuras

### Formato obrigatório:

```markdown
![FIG-XX.Y: Legenda descritiva](../assets/figures/fig_xx_nome.png)
```

Onde:
- `XX` = número do capítulo (01-28)
- `Y` = sequência dentro do capítulo (1, 2, 3...)

### Exemplo:

```markdown
![FIG-04.2: Camadas lamelares da pálpebra](../assets/figures/fig_04_lamelas.png)
```

### Regras:

- **Chamada obrigatória no texto** antes da imagem (ex: "Como demonstrado na FIG-04.2...")
- Legendas devem ser descritivas (não "Figura 1")
- Imagens em PNG ou JPG
- Tamanho recomendado: 1200px de largura
- Figuras nunca devem aparecer "soltas" sem contexto clínico

---

## 5. Referências

### Formato no texto:

```markdown
Conforme descrito por Fagien [[REF:FAGIEN-1999]]...
```

### Formato de saída (após build):

Depende do `--ref-style` no clean_manuscript.py:
- `keep`: mantém `[[REF:FAGIEN-1999]]`
- `paren`: converte para `(FAGIEN-1999)`
- `superscript`: converte para `^[FAGIEN-1999]^`

### Regras:

- IDs seguem padrão `AUTOR-ANO` (maiúsculas)
- Todas as referências devem existir em `99_BIBLIOGRAFIA.md`

---

## 6. Tags Internas (nunca aparecem no output final)

| Tag | Comportamento no Build |
|-----|------------------------|
| `[[KEEP]]...[[/KEEP]]` | Remove tags, mantém conteúdo |
| `[[MOVE:CAP-XX]]` | Remove marcador, mantém conteúdo |
| `[[TODO: texto]]` | Remove no release |
| `[[DELETE]]...[[/DELETE]]` | Remove tudo (tag + conteúdo) |
| `Figura sugerida:` | Remove no `--strip-backlog` |

---

## 7. Listas

### Numeradas (para sequências/passos):

```markdown
1. Primeiro passo
2. Segundo passo
3. Terceiro passo
```

### Não numeradas (para itens sem ordem):

```markdown
- Item A
- Item B
- Item C
```

### Checklists (para verificação):

```markdown
- [ ] Item pendente
- [x] Item concluído
```

---

## 8. Separadores

Use `---` para separar seções grandes (aparece como `* * *` no output).

Limite: máximo 2 separadores por capítulo.

---

## Checklist de Revisão (antes de submeter capítulo)

- [ ] Negrito apenas em termos técnicos
- [ ] Máximo 3 boxes por capítulo
- [ ] Todas as `[[REF:ID]]` existem na bibliografia
- [ ] Figuras com legendas descritivas
- [ ] Sem tags `[[TODO]]` ou `[[DELETE]]` no release
- [ ] Headers em ordem correta (sem pular níveis)
