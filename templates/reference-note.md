---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/reference
  - {{type_tag}}
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: "{{url}}"
project: ""
citekey: "{{citekey}}"
doi: "{{doi}}"
---

# {{title}}

> **Tipo:** {{ref_type}}  # article, book, chapter, thesis, report, web
> **Vault:** PesquisAI v0.5.0+

## 1. Identificadores

| Campo | Valor |
|---|---|
| Citekey | `{{citekey}}` |
| DOI | `{{doi}}` |
| URL | <{{url}}> |
| ISBN | `{{isbn}}` |
| ISSN | `{{issn}}` |

## 2. Citação ABNT

```
{{abnt_citation}}
```

## 3. Citação BibTeX

```bibtex
{{bibtex}}
```

## 4. Citação APA

```
{{apa_citation}}
```

## 5. Metadados

| Campo | Valor |
|---|---|
| Autores | {{authors}} |
| Ano | {{year}} |
| Título | {{title_full}} |
| Veículo | {{venue}} |
| Volume | {{volume}} |
| Número | {{number}} |
| Páginas | {{pages}} |
| Editora | {{publisher}} |
| Idioma | {{language}} |

## 6. Resumo

> {{abstract}}

## 7. Onde é citado neste vault

```dataview
LIST
FROM ""
WHERE contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

## 8. Notas de uso

<!-- Como eu uso / vou usar esta referência -->

- [[]] — *citado em*
- [[]] — *citado em*

## 9. PDF / arquivo

- <!-- caminho no Drive ou local -->

## 10. Citações reversas (outras obras que citam)

<!-- Preencher manualmente ou via Scopus -->

-

---

> **Política de integridade:** toda referência DEVE ter DOI verificado
> via `citation-management` antes de entrar no vault. O PesquisAI
> recusa citações sem DOI / URL válida para artigos científicos.
