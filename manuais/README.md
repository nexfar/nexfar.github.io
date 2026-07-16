# Manuais IC — Inteligência Comercial

Páginas HTML estáticas dos manuais de uso da Inteligência Comercial (Nexfar), servidas via **GitHub Pages**.

Todos os `.html` são **auto-contidos**: as imagens estão embutidas em `base64`, sem dependência de assets externos. Basta copiar os arquivos e ligar o Pages.

## Conteúdo

| Arquivo | Página |
|---|---|
| `index.html` | Home / índice com cards (ordem: Objetivos → Cotação → Catálogo) |
| `manual-objetivos-sugestoes.html` | Objetivos e Sugestões — Com meta |
| `manual-objetivos-sugestoes-sem-meta.html` | Objetivos e Sugestões — Sem meta |
| `manual-cotacao-agil.html` | Cotação Ágil |
| `manual-catalogo-digital.html` | Catálogo Digital — Com preço |
| `manual-catalogo-digital-sem-preco.html` | Catálogo Digital — Sem preço |

Os links do `index.html` são **relativos**, então funcionam em qualquer domínio/repo sem edição.

## Hospedagem (GitHub Pages)

1. Commit desta pasta num repo público.
2. **Settings → Pages → Source:** branch `main`, pasta `/root` (ou `/docs` conforme o layout).
3. URL final: `https://<org>.github.io/<repo>/manuais/`

## Atualizar

**Trocar texto/layout de um manual:** editar o `.html` correspondente e commitar. Pages rebuilda em ~1 min; qualquer site que embute por iframe reflete sozinho.

**Regerar do zero (imagens novas):** precisa da fonte editável (repo interno `prd-docs`, pasta `features-tutorials/nf-next-ic/` com os `manual-*.html` originais + pasta `assets/`) e do script `build-inline.py`:

```bash
python3 build-inline.py <dir-fonte> <dir-saida>
# ex.: python3 build-inline.py ../prd-docs/features-tutorials/nf-next-ic ./manuais
```

O script lê cada `manual-*.html`, converte todo `src="assets/*.png"` em `data:` base64 e grava as versões auto-contidas no destino.

## Versão

Documentação alinhada à versão **0.5.2** do produto.
