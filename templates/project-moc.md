---
title: "{{title}} — MOC"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/moc
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: ""
project: "{{project}}"
---

# {{title}} — Map of Content

> **Projeto:** {{project}}
> **Escopo:** {{scope}}
> **Vault:** PesquisAI v0.5.0+

## 1. Visão geral do projeto

<!-- 2-3 parágrafos sobre o que é este projeto -->

## 2. Pergunta de pesquisa central

> **P:** {{research_question}}

## 3. Objetivos

- **Geral:** <!-- -->
- **Específicos:**
  - [ ] <!-- -->
  - [ ] <!-- -->

## 4. Hipóteses

```dataview
LIST
FROM "hypothesis"
WHERE project = "{{project}}"
SORT file.ctime ASC
```

## 5. Revisão de literatura

```dataview
LIST
FROM "literature"
WHERE project = "{{project}}" OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

## 6. Metodologia

```dataview
LIST
FROM "methodology"
WHERE project = "{{project}}" OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

## 7. Dados utilizados

```dataview
LIST
FROM "datasource"
WHERE project = "{{project}}" OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

## 8. Notas de pesquisa

```dataview
LIST
FROM "research"
WHERE project = "{{project}}" OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

## 9. Daily notes do projeto

```dataview
LIST
FROM "daily"
WHERE contains(file.outlinks, this.file.link) OR contains(tags, "pesquisai/{{project}}")
SORT file.name DESC
LIMIT 30
```

## 10. Sessões recentes

```dataview
LIST
FROM "sessions"
WHERE contains(file.outlinks, this.file.link)
SORT file.ctime DESC
LIMIT 10
```

## 11. Cronograma

| Etapa | Início | Fim | Status |
|---|---|---|---|
| | | | ⬜ |

## 12. Próximas ações

- [ ] <!-- ação concreta -->

## 13. MOCs vizinhos (sub-projetos)

- [[]] — *sub-MOC 1*
- [[]] — *sub-MOC 2*

---

> **Política de integridade:** este MOC é uma **VIEW** sobre o
> vault. O PesquisAI pode regenerar as queries Dataview acima a
> cada abertura. Não edite as queries diretamente — em vez disso,
> ajuste os campos `project` e tags das notas filhas.
