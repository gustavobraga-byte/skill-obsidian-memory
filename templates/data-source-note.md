---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/datasource
  - {{source_tag}}
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: "{{url}}"
project: ""
---

# {{title}}

> **Órgão:** {{org}}
> **Granularidade:** {{granularity}}
> **Período:** {{period}}
> **Vault:** PesquisAI v0.5.0+

## 1. Identificação

| Campo | Valor |
|---|---|
| URL oficial | <{{url}}> |
| API endpoint | `{{api_url}}` |
| Periodicidade | {{frequency}} |
| Última atualização | {{last_update}} |
| Licença | {{license}} |

## 2. Estrutura dos dados

### 2.1 Tabelas / coleções

- `{{table_1}}` — *descrição*
- `{{table_2}}` — *descrição*

### 2.2 Variáveis principais

| Variável | Tipo | Unidade | Observação |
|---|---|---|---|
| | | | |

### 2.3 Chave primária

- <!-- combinação de campos -->

## 3. Como acessar

### 3.1 Via skill PesquisAI

```python
from pesquisai.skills import load_skill
ibge = load_skill("ibge-br")
data = ibge.fetch(table="...", variables=[...], period="...")
```

### 3.2 Via API direta

```bash
curl '{{api_url}}?...' | jq
```

### 3.3 Via download

<!-- Link para o portal de dados -->

## 4. Cuidados metodológicos

### 4.1 Quebras de série

<!-- Há mudanças de metodologia ao longo do tempo? -->

-

### 4.2 Valores faltantes

<!-- Como a fonte lida com missing? -->

-

### 4.3 Revisão de dados

<!-- Quando os dados são revistos? Há controle de versão? -->

-

## 5. Notas de uso

<!-- Como eu já usei esta fonte -->

- [[]] — *uso em pesquisa X, lições aprendidas*

## 6. Notas da fonte

<!-- Citação sugerida pela própria fonte -->

```
{{source_citation}}
```

## 7. Pesquisa no vault

```dataview
LIST
FROM ""
WHERE contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

---

> **Política de integridade:** sempre conferir a versão mais recente
> dos dados **diretamente** na fonte oficial. O PesquisAI pode
> intermediar o acesso, mas o usuário é responsável pela validação.
> Marcador padrão para dados desta fonte: `[DADO CONFIRMADO]`.
