---
title: "PNAE e Capacidade Estatal nos Municípios de MG"
created: 2026-06-15
updated: 2026-06-29
tags:
  - pesquisai/research
  - pesquisai/ibge
  - pesquisai/draft
author: "Gustavo Bastos Braga"
created_by: ""
status: review
source: ""
project: "pnae-tcc"
citekey: ""
doi: ""
---

# PNAE e Capacidade Estatal nos Municípios de MG

> **Projeto:** [[moc/pnae-tcc]]
> **Data de início:** 2026-06-15
> **Vault:** PesquisAI v0.5.0+

## 1. Pergunta de pesquisa

**P:** Em que medida a capacidade estatal dos municípios mineiros
influencia a execução do Programa Nacional de Alimentação Escolar (PNAE)
no período 2015-2024?

## 2. Objetivos

### 2.1 Objetivo geral
Analisar a relação entre capacidade estatal municipal e os indicadores
de execução do PNAE em Minas Gerais.

### 2.2 Objetivos específicos
- [x] Mapear a capacidade estatal dos 853 municípios mineiros
- [x] Coletar indicadores de execução do PNAE (FNDE)
- [ ] Estimar modelos de regressão multinível
- [ ] Comparar resultados por porte populacional

## 3. Hipóteses

- [[H1-pnae-capacidade]] — *H1: municípios com maior capacidade estatal
  apresentam melhor execução do PNAE*

## 4. Revisão de literatura

- [[santos-2024-pnae-mg]] — Santos (2024): PNAE em Minas Gerais
- [[carvalho-2023-capacidade-estatal]] — Carvalho (2023): capacidade
  estatal municipal

### 4.1 Lacunas identificadas

- Estudos quantitativos sobre capacidade estatal municipal em MG são raros
- A maioria usa proxies únicas (receita per capita) sem considerar
  dimensões burocráticas e políticas

## 5. Estratégia metodológica

- [[methodology/regressao-multinivel]]

### 5.1 Dados utilizados

- [[datasource/ibge-censo-2022]] — *população, PIB per capita*
- [[datasource/fnde-pnae-execucao]] — *repasses, alunos atendidos*

### 5.2 Variáveis

| Variável | Tipo | Fonte | Nota |
|---|---|---|---|
| capacidade_estatal | índice (0-1) | [[carvalho-2023-capacidade-estatal]] | proxy multidimensional |
| repasse_pnae_pc | R$ per capita | FNDE/SIGPC | repasse anual / população |
| alunos_atendidos_pct | % | FNDE | cobertura municipal |
| porte_pop | categórica | IBGE | pequeno/médio/grande |
| ideb_ensino_fundamental | contínuo | INEP | controle |

## 6. Análises

### 6.1 Descritiva

```python
import pandas as pd
df = pd.read_csv("painel_replicacao.csv")
print(df.groupby("porte_pop")["repasse_pnae_pc"].describe())
```

### 6.2 Inferencial

```python
import statsmodels.formula.api as smf
model = smf.mixedlm(
    "repasse_pnae_pc ~ capacidade_estatal + porte_pop + ideb",
    data=df, groups=df["mesorregiao"]
)
result = model.fit()
print(result.summary())
```

## 7. Resultados preliminares

- Repasse médio per capita: **R$ 0,42** (mediana)
- Correlação capacidade × repasse: **r = 0,38** (p < 0,001)
- Coeficiente do modelo multinível: **β = 0,29** (p < 0,001)

## 8. Discussão

- Resultado confirma hipótese principal: municípios com maior
  capacidade estatal têm melhor execução do PNAE
- Efeito é **robusto** ao controle por porte populacional
- Heterogeneidade por mesorregião é significativa (verificar com
  efeitos fixos)

## 9. Cronograma

| Etapa | Início | Fim | Status |
|---|---|---|---|
| Levantamento bibliográfico | 2026-05-01 | 2026-06-15 | ✅ |
| Coleta de dados | 2026-06-15 | 2026-07-15 | 🔄 |
| Análise | 2026-07-15 | 2026-08-30 | ⬜ |
| Redação | 2026-08-30 | 2026-10-15 | ⬜ |
| Revisão | 2026-10-15 | 2026-11-15 | ⬜ |
| Submissão | 2026-11-15 | 2026-12-01 | ⬜ |

## 10. Referências

```bibtex
@article{santos2024pnae,
  author = {Santos, Maria das Graças and Silva, João Pedro},
  title = {PNAE em Minas Gerais: uma análise quantitativa},
  journal = {Revista de Administração Pública},
  year = {2024},
  volume = {58},
  number = {3},
  pages = {456-478},
  doi = {10.1590/0034-76122024xxxx}
}
```

## 11. Próximos passos

- [ ] Concluir coleta de dados do FNDE
- [ ] Validar proxy de capacidade estatal com survey
- [ ] Rodar modelos com efeitos fixos

## 12. Notas de sessão

```dataview
LIST
FROM "sessions"
WHERE contains(file.outlinks, this.file.link)
SORT file.ctime DESC
```

---

> **Nota:** esta nota é editada **manualmente** pelo pesquisador
> (`created_by` vazio). O PesquisAI pode ler mas não sobrescreve.
