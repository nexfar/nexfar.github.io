# Manuais Nexfar — site (GitHub Pages)

Site estático dos manuais de uso dos produtos Nexfar, servido em **https://nexfar.github.io/**.
Todos os `.html` de manual são **auto-contidos** (imagens em `base64`, sem assets externos).

## Estrutura e URLs de produção

```
/                     -> redireciona para /manuais/
/manuais/             -> HOME (índice de produtos; IC é uma seção com seus manuais)
/manuais/assets/      -> logo Nexfar (usado na home)
/manuais/README.md    -> este arquivo
/manuais/build-nav-export.py
/<slug>               -> manual (o GitHub Pages serve o .html)
/ic/, /ic/<slug>      -> redirects legados para /manuais/ e /<slug>
```

| URL de produção | Página |
|---|---|
| `/manuais` | Home (produtos) |
| `/objetivos-e-sugestoes` | Objetivos e Sugestões — Com meta |
| `/objetivos-e-sugestoes-sem-meta` | Objetivos e Sugestões — Sem meta |
| `/cotacao-agil` | Cotação Ágil |
| `/catalogo-digital` | Catálogo Digital — Com preço |
| `/catalogo-digital-sem-preco` | Catálogo Digital — Sem preço |

`/` e `/ic/` redirecionam para `/manuais/`; `/ic/<slug>` redireciona para `/<slug>` (via `<meta refresh>` + JS). Os stubs em `/ic/` existem só para não quebrar links já divulgados.
Novo manual = novo `.html` na raiz + nova entrada na seção do produto na home.

## Nav / export / build

`manuais/build-nav-export.py` é idempotente (marcadores `<!--NAVEXPORT-->` / `/* NAVEXPORT */`).
Injeta nos manuais (`/<slug>.html` na raiz): breadcrumb sticky (home `/manuais/` + dropdown de manuais) + índice
de seções, índice sticky com scroll suave, back-to-top, export PDF (`window.print()` página-única),
`@media print`. Na home injeta a seção de produto, o logo Nexfar, o botão + modal de export combinado
e os links de produção. Rodar sempre de dentro de `manuais/`:

```bash
cd manuais && python3 build-nav-export.py
```

Para reeditar layout: reverter os `.html` (`git checkout -- ...`), editar o script, rodar de novo.

## Versão

Manuais IC alinhados à versão **0.5.2** do produto (badge na seção IC da home).
