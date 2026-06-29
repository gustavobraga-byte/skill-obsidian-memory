---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/session
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: ""
project: ""
---

# {{title}}

> **Sessão ID:** `{{session_id}}`
> **Início:** {{started_at}}
> **Vault:** PesquisAI v0.5.0+

## Resumo executivo

<!-- 2-3 frases sobre o que foi feito nesta sessão -->

## Interações do usuário

> {{request_1}}

> {{request_2}}

> {{request_3}}

## Skills usadas

- `{{skill_1}}` — *motivo*
- `{{skill_2}}` — *motivo*

## Dados acessados

<!-- Fontes consultadas -->

- [[datasource/ibge-{{dataset}}]] — *usado para X*
- [[datasource/datasus-{{dataset}}]] — *usado para Y*

## Notas criadas

- [[{{note_1}}]]
- [[{{note_2}}]]

## Notas atualizadas

- [[{{note_updated}}]]

## Arquivos gerados

- `{{file_1}}` (no Drive)
- `{{file_2}}` (no Drive)

## Comandos executados (resumo)

```bash
# (apenas comandos "seguros" — sem chaves, sem paths absolutos)
{{cmd_1}}
```

## Outputs relevantes

```
{{output_1}}
```

## Marcadores de evidência usados

- `[DADO CONFIRMADO]` — X vezes
- `[ESTIMATIVA FUNDAMENTADA]` — Y vezes
- `[SEM DADOS SUFICIENTES]` — Z vezes

## Métricas

| Métrica | Valor |
|---|---|
| Duração | Xm Ys |
| Tokens (in/out) | X / Y |
| Skills invocadas | N |
| Notas criadas | N |
| Arquivos gerados | N |

## Próximas ações

- [ ] {{action_1}}
- [ ] {{action_2}}

## Reflexões

<!-- O que aprendi sobre o próprio agente? -->

-

---

> **Nota:** esta nota é gerada automaticamente por
> `ObsidianMemory.end_session()`. Não edite manualmente; em vez disso,
> corrija o agente e reexecute a sessão.
