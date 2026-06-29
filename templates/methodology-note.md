---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/methodology
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: ""
project: ""
---

# {{title}}

> **Tipo de método:** {{method_type}}  # descritivo, correlacional, experimental, qualitativo, misto
> **Vault:** PesquisAI v0.5.0+

## 1. Quando usar

<!-- Em que situações este método é apropriado? -->

## 2. Quando **não** usar

<!-- Limitações, casos em que falha -->

## 3. Pressupostos

<!-- Hipóteses que o método assume -->

-

## 4. Variáveis

### 4.1 Dependente(s)

-

### 4.2 Independente(s)

-

### 4.3 Controle / confundidoras

-

## 5. Procedimento

<!-- Passo a passo detalhado -->

1.
2.
3.

## 6. Implementação

```python
# Código de referência (R, Python, Stata...)
{{code_example}}
```

## 7. Interpretação

### 7.1 O que os coeficientes / estatísticas significam

-

### 7.2 Como reportar (template IMRaD)

> "Foi realizado {{method}} com {{n}} observações. Os resultados
> indicam que {{interpretation}} (β = X, p < Y)."

## 8. Limitações e vieses

- **Viés de seleção:** <!-- -->
- **Viés de informação:** <!-- -->
- **Viés de confundimento:** <!-- -->
- **Endogeneidade:** <!-- -->

## 9. Diagnósticos recomendados

- [ ] <!-- teste 1 -->
- [ ] <!-- teste 2 -->
- [ ] <!-- teste 3 -->

## 10. Alternativas

<!-- Outros métodos para o mesmo problema -->

- [[]] — *método alternativo 1*
- [[]] — *método alternativo 2*

## 11. Referências metodológicas

```dataview
LIST
FROM "literature"
WHERE contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

## 12. Aplicações neste vault

```dataview
LIST
FROM "research"
WHERE contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

---

> **Política de integridade:** antes de aplicar o método, valide
> pressupostos e reporte limitações conforme diretrizes da área
> (CONSORT, STROBE, PRISMA, SRQR, etc.).
