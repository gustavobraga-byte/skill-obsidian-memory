# Skill `obsidian-memory`

Documentação complementar à [`SKILL.md`](./SKILL.md). Cobre detalhes
operacionais: convenções de nomenclatura, versionamento, performance,
e exemplos de uso avançado.

## Estrutura de pastas recomendada no vault

```
vault/
├── .obsidian/                  # config do Obsidian (criado pelo init)
├── .backups/                   # backups automáticos (sync.py)
├── .trash/                     # lixeira do agente
├── .pesquisai-audit.log        # log de auditoria (criado pelo Vault)
├── daily/                      # notas diárias
├── research/                   # projetos de pesquisa
├── literature/                 # revisões de papers
├── methodology/                # métodos analíticos
├── hypothesis/                 # hipóteses
├── reference/                  # citações
├── sessions/                   # logs de sessão
├── moc/                        # Maps of Content (índices)
├── inbox/                      # capturas rápidas
└── datasource/                 # fontes de dados
```

## Convenções de nomenclatura

| Tipo | Padrão | Exemplo |
|---|---|---|
| Daily | `daily/YYYY-MM-DD.md` | `daily/2026-06-29.md` |
| Research | `research/<slug>.md` | `research/pnae-capacidade-estatal.md` |
| Literature | `literature/<autor>-<ano>-<slug>.md` | `literature/santos-2024-pnae-mg.md` |
| Hypothesis | `hypothesis/H<n>-<slug>.md` | `hypothesis/H1-desigualdade-renda.md` |
| Method | `methodology/<slug>.md` | `methodology/regressao-pnad.md` |
| DataSource | `datasource/<fonte>.md` | `datasource/ibge-pnad-continua.md` |
| Reference | `reference/<citekey>.md` | `reference/santos2024pnae.md` |
| MOC | `moc/<projeto>.md` | `moc/pnae-tcc.md` |
| Inbox | `inbox/<timestamp>.md` | `inbox/2026-06-29-153022.md` |
| Session | `sessions/YYYY-MM-DD-<sid>.md` | `sessions/2026-06-29-host-153022.md` |

Slug = lowercase, sem acentos, hífens no lugar de espaços.

## Frontmatter obrigatório

Toda nota **criada pelo PesquisAI** deve ter:

```yaml
---
title: "..."           # string
created: YYYY-MM-DD    # ISO 8601
updated: YYYY-MM-DD    # ISO 8601
tags: [pesquisai/...]  # sempre começa com pesquisai/
author: "..."          # vazio se criado pelo agente
created_by: pesquisai  # ESTE campo identifica autoria do agente
status: draft|review|published|archived
source: ""             # URL, DOI ou caminho
project: ""            # ID do MOC (se houver)
---
```

A regra `created_by: pesquisai` é o que permite o agente atualizar a
nota depois — notas sem esse campo são **read-only** para o agente.

## Dataview queries úteis

```dataview
LIST
FROM "research"
WHERE contains(tags, "pesquisai/ibge")
SORT file.ctime DESC
LIMIT 10
```

```dataview
TABLE
  file.cday AS "Criado",
  status AS "Estado",
  citekey AS "BibTeX"
FROM "literature"
SORT file.mday DESC
```

```dataview
LIST
FROM #pesquisai/draft
WHERE project = "pnae-tcc"
SORT file.mtime DESC
```

## Performance

- Vaults até **2.000 notas** rodam suavemente sem cache
- Entre **2.000 e 10.000** notas o índice BM25 é construído uma vez
  por sessão (~3 segundos para 5.000 notas)
- Acima de **10.000 notas** recomenda-se particionar em múltiplos
  vaults (ex.: um por projeto)

## Versionamento do vault

A skill segue **SemVer** para a estrutura do vault:

- **MAJOR** (1.x → 2.x): mudança incompatível no schema do frontmatter
- **MINOR** (0.5.0 → 0.6.0): novo template ou tag
- **PATCH** (0.5.0 → 0.5.1): correção em template existente

O campo `vault_version` no `.obsidian/pesquisai.json` rastreia a versão.

## Licença

MIT — mesmo do PesquisAI.
