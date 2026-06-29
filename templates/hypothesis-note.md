---
title: "{{title}}"
created: {{date}}
updated: {{date}}
tags:
  - pesquisai/hypothesis
  - pesquisai/draft
author: ""
created_by: pesquisai
status: draft
source: ""
project: "{{project}}"
---

# {{title}}

> **Projeto:** [[{{moc_path}}]]
> **Tipo:** {{hypothesis_type}}  # nula, alternativa, direcional, não-direcional
> **Vault:** PesquisAI v0.5.0+

## 1. Enunciado

**H{{number}}:** {{statement}}

<!-- Em uma frase, declarar a relação esperada entre variáveis. -->

## 2. Variáveis envolvidas

### 2.1 Independente (X)

- <!-- nome da variável, unidade, fonte -->

### 2.2 Dependente (Y)

- <!-- nome da variável, unidade, fonte -->

### 2.3 Mediadoras / Moderadoras (se houver)

-

## 3. Base teórica

<!-- Em que teoria / literatura esta hipótese se apoia? -->

- [[literature/]]
- [[methodology/]]

## 4. Operacionalização

### 4.1 Como X será medida

<!-- Operacionalização concreta: instrumento, fórmula, etc. -->

### 4.2 Como Y será medida

<!-- -->

### 4.3 Como a relação X → Y será testada

<!-- Método estatístico -->

- [[methodology/]]

## 5. Predições

<!-- Se a hipótese for verdadeira, o que se espera observar? -->

### 5.1 Sinal esperado

- <!-- + ou - -->

### 5.2 Magnitude esperada

- <!-- tamanho de efeito esperado -->

### 5.3 Nível de significância alvo

- <!-- α = 0.05, 0.01, etc. -->

## 6. Testes alternativos

- **H{{number}}_alt_1:** <!-- -->
- **H{{number}}_alt_2:** <!-- -->

## 7. Dados que podem confirmar / refutar

- [[datasource/]]

## 8. Status

- [ ] Formulada
- [ ] Operacionalizada
- [ ] Testada
- [ ] Confirmada
- [ ] Refutada
- [ ] Rejeitada (mas informativo)

## 9. Resultados (a preencher após teste)

| Indicador | Valor | p | IC 95% |
|---|---|---|---|
| | | | |

## 10. Discussão

<!-- Como interpretar o resultado -->

-

## 11. Conexões

```dataview
LIST
FROM ""
WHERE contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```

---

> **Política de integridade:** hipóteses devem ser formuladas **antes**
> da coleta de dados. Re-formulação após ver os resultados é
> aceitável, mas deve ser explicitamente declarada.
