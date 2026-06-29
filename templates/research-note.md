---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/research
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: ""
project: "{{project}}"
citekey: ""
doi: ""
---

# {{title}}

> **Projeto:** [[{{moc_path}}]]
> **Data de início:** {{date}}
> **Vault:** PesquisAI v0.5.0+

## 1. Pergunta de pesquisa

<!-- A pergunta central, em uma frase. -->

**P:** {{research_question}}

## 2. Objetivos

### 2.1 Objetivo geral

<!-- -->

### 2.2 Objetivos específicos

- [ ]
- [ ]
- [ ]

## 3. Hipóteses

<!-- Liste hipóteses com notas filhas -->

- [[H1-{{slug}}]] — *Hipótese 1*
- [[H2-{{slug}}]] — *Hipótese 2 (se houver)*

## 4. Revisão de literatura

<!-- Notas filhas em literature/ -->

- [[santos-2024-{{slug}}]]
- [[]]

### 4.1 Lacunas identificadas

<!-- O que ainda não foi respondido na literatura? -->

-

## 5. Estratégia metodológica

<!-- Link para nota de método -->

- [[methodology/{{slug}}]]

### 5.1 Dados utilizados

<!-- Links para notas de fontes de dados -->

- [[datasource/]]
- [[]]

### 5.2 Variáveis

| Variável | Tipo | Fonte | Nota |
|---|---|---|---|
| | | | |

## 6. Análises

### 6.1 Descritiva

<!-- outputs, tabelas, gráficos -->

```python

```

### 6.2 Inferencial

<!-- modelos, regressões, testes -->

```python

```

## 7. Resultados preliminares

<!-- O que os dados mostram até aqui? -->

-

## 8. Discussão

<!-- Como interpretar à luz da teoria? -->

-

## 9. Cronograma

| Etapa | Início | Fim | Status |
|---|---|---|---|
| Levantamento bibliográfico | | | ⬜ |
| Coleta de dados | | | ⬜ |
| Análise | | | ⬜ |
| Redação | | | ⬜ |
| Revisão | | | ⬜ |
| Submissão | | | ⬜ |

## 10. Referências

<!-- Notas filhas em reference/ -->

```bibtex

```

## 11. Próximos passos

- [ ]

## 12. Notas de sessão

<!-- Auto-preenchido pelo PesquisAI -->

```dataview
LIST
FROM "sessions"
WHERE contains(file.outlinks, this.file.link)
SORT file.ctime DESC
```

---

> **Política de integridade:** esta nota é gerada pelo PesquisAI
> (`created_by: pesquisai`). O pesquisador pode editar livremente.
> O agente só atualiza esta nota se o usuário pedir explicitamente ou
> se for o próprio PesquisAI executando uma skill de revisão.
