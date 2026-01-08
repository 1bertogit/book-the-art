# Modern Face - Guia de Uso

## 📚 Estrutura dos 5 Ebooks

Cada ebook tem sua própria pasta independente:

```
modern-face/
├─ config_template.yml         # Template de configuração
├─ ebook-1/
│  ├─ content/                 # Capítulos .md
│  ├─ assets/figures/          # Imagens
│  └─ dist/                    # Output gerado
├─ ebook-2/
│  ├─ content/
│  ├─ assets/figures/
│  └─ dist/
├─ ebook-3/
├─ ebook-4/
└─ ebook-5/
```

## 🚀 Como Criar Cada Ebook

### Passo 1: Adicionar Conteúdo
```bash
cd projects/modern-face/ebook-1/content

# Adicione seus capítulos com prefixos numéricos:
# 01-introducao.md
# 02-conceitos-basicos.md
# 03-tecnicas-avancadas.md
# ...
```

### Passo 2: Configurar
```bash
cd projects/modern-face/ebook-1

# Copie o template e customize
cp ../config_template.yml config.yml

# Edite config.yml:
# - Troque [NUMERO] pelo número do ebook
# - Ajuste nome, autor, paths
```

### Passo 3: Gerar
```bash
# De dentro de projects/modern-face/ebook-1/
python ../../../shared/generate_complete_ebook.py

# Output: dist/modern_face_ebook_1.md
```

### Passo 4: Exportar (Opcional)
```bash
# HTML
pandoc dist/modern_face_ebook_1.md -o dist/ebook_1.html

# DOCX
pandoc dist/modern_face_ebook_1.md -o dist/ebook_1.docx

# PDF (requer LaTeX)
pandoc dist/modern_face_ebook_1.md -o dist/ebook_1.pdf
```

## 📋 Checklist Rápido

- [ ] Criar arquivos .md numerados em `ebook-X/content/`
- [ ] Copiar e editar `config.yml` para cada ebook
- [ ] Adicionar imagens em `ebook-X/assets/figures/`
- [ ] Rodar `generate_complete_ebook.py`
- [ ] Verificar output em `ebook-X/dist/`
- [ ] Exportar para formato final (HTML/DOCX/PDF)

## 🔄 Scripts Disponíveis

Todos os scripts estão em `../../shared/`:
- `generate_complete_ebook.py` - Compila capítulos em um único markdown
- `build.py` - Build avançado com validações

## ✨ Dicas

1. **Numeração consistente**: Use prefixos `01-`, `02-`, etc. nos capítulos
2. **Reutilize assets**: Imagens podem ser compartilhadas entre ebooks
3. **Teste incremental**: Gere o ebook após adicionar cada capítulo
4. **Versionamento**: Use git para versionar cada ebook independentemente
