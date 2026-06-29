---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/literature
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: "{{doi_or_url}}"
project: ""
citekey: "{{citekey}}"
doi: "{{doi}}"
evidence_level: ""
---

# {{title}}

> **Autores:** {{authors}}
> **Ano:** {{year}}
> **Veículo:** {{venue}}
> **DOI/URL:** {{doi_or_url}}
> **Tipo:** {{type}}  # artigo, livro, capítulo, tese, relatório, preprint
> **Vault:** PesquisAI v0.5.0+

## 1. Citação (ABNT)

```
{{abnt_citation}}
```

## 2. Citação (BibTeX)

```bibtex
{{bibtex}}
```

## 3. Resumo estruturado (CARE-like)

### 3.1 Contexto
<!-- Por que este estudo existe? -->

### 3.2 Objetivo
<!-- -->

### 3.3 Métodos
<!-- -->

### 3.4 Resultados principais
<!--  -->

### 3.5 Conclusões dos autores
<!-- -->

### 3.6 Nível de evidência

<!-- Marcar conforme GRADE -->

- [ ] **Alta** (revisão sistemática de ECR)
- [ ] **Moderada** (ECR individual ou estudo observacional robusto)
- [ ] **Baixa** (série de casos, opinião de especialistas)
- [ ] **Muito baixa** (relato, abstract de congresso)

`evidence_level`: `{{evidence_level}}`  <!-- alto | moderado | baixo | muito_baixo -->

## 4. Pontos fortes

- <!-- -->

## 5. Limitações

- <!-- -->

## 6. Conceitos-chave (para virar notas filhas)

- [[]] — *conceito 1*
- [[]] — *conceito 2*

## 7. Citações diretas relevantes

> "..." (p. X)
> — *{{authors}}, {{year}}*

## 8. Conexões no vault

<!-- Wikilinks para notas relacionadas -->

- [[]] — *método utilizado*
- [[]] — *dados utilizados*
- [[]] — *aplicado em*

## 9. Citações reversas

<!-- Quem引用ou este paper (preenchido manualmente) -->

-

## 10. Minhas anotações

<!-- Comentários pessoais sobre o paper -->

### 10.1 O que achei mais importante

-

### 10.2 Como posso usar

- [[]] — *aplicação em meu projeto*

### 10.3 Discordâncias

-

---

> **Política de integridade:** o conteúdo desta nota é síntese e
> paráfrase da fonte. Citações diretas estão entre aspas e atribuídas.
> O PesquisAI **não** copia parágrafos inteiros sem transformação.
> Verificações automáticas em `tests/test_literature.py` validam
> conformidade com `citation-management`.
