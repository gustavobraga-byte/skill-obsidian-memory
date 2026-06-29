---
name: obsidian-memory
description: |
  Use esta skill SEMPRE que o PesquisAI precisar ler, escrever ou
  consultar a memória persistente do agente em um vault do Obsidian.
  Cobre: criação de notas a partir de templates (daily, research,
  literature, session-log, methodology, data-source, hypothesis,
  reference, project-moc, inbox), busca textual + tags, construção
  de backlinks e wikilinks, sincronização com Drive/git, exportação
  de logs de sessão, e manutenção de MOCs (Maps of Content).

  Ative também para frases como "salve no meu vault", "lembre disso
  na próxima sessão", "crie uma nota de revisão sobre X", "qual a
  minha última daily", "liste os papers que já revisei sobre Y",
  "monte um MOC para o projeto Z", "sincronize o vault com o Drive",
  "abrir/ativar o segundo cérebro", "memória persistente",
  "second brain", "obsidian", "vault", "wikilink", "backlink",
  "[[nota]]", "#pesquisai/...".
---

# 🧠 Skill `obsidian-memory` — Segundo Cérebro do PesquisAI

> **Versão:** 0.5.0
> **Status:** Estável (integrada ao PesquisAI ≥ v0.4.2.3)
> **Mantida por:** Gustavo Bastos Braga (UFV)
> **Inspirada em:** K-Dense `open-notebook` + Atomic Notes (Andy Matuschak)

---

## 0. REGRA DE PERSISTÊNCIA: vault SEMPRE no Google Drive

> 📍 **O vault do Obsidian DEVE ficar no Google Drive do usuário.**
> Nunca em `/content/` (efêmero no Colab) ou `/tmp/` (perdido ao
> fim da sessão).

**Caminho padrão:** `/content/drive/My Drive/PesquisAI/vault/`

A skill **rejeita** inicialização com vault fora do Drive quando
roda no Colab. Isso é uma salvaguarda de **perda de dados** —
pesquisas de meses sumiriam junto com a sessão do Colab.

Caminhos aceitos como "no Drive":

| Plataforma | Caminho |
|---|---|
| Google Colab (FUSE) | `/content/drive/My Drive/PesquisAI/vault/` |
| Google Colab (Drive compartilhado) | `/content/drive/Shared drives/<nome>/vault/` |
| Desktop macOS | `/Volumes/GoogleDrive/.../PesquisAI/vault/` |
| Desktop Linux (ocamlfuse) | `/mnt/gdrive/.../PesquisAI/vault/` |
| Desktop Windows | `G:\Meu Drive\PesquisAI\vault\` |

---

## 1. O que esta skill faz

Esta skill transforma o **vault do Obsidian** em uma camada de memória
persistente do PesquisAI. Resolve a limitação declarada no `AGENTS.md`:

> *"Sem memória entre sessões: o contexto é reiniciado a cada conversa."*

Com a skill ativa, o agente:

- **Lê** o vault no início de cada sessão (carrega contexto)
- **Escreve** notas ao final (log de sessão, achados, drafts)
- **Conecta** conceitos via wikilinks `[[nota]]` e backlinks
- **Indexa** tudo por tags padronizadas `#pesquisai/*`
- **Busca** em BM25 (offline, sem API externa) por texto e tag
- **Sincroniza** com Google Drive / git bare / Obsidian Git plugin

> ⚠️ **Política de integridade mantida:** o agente **só escreve** em
> notas marcadas com `created_by: pesquisai`. Notas humanas são
> read-only (ver :class:`Vault`).

---

## 2. Quando ativar esta skill

Ative a skill sempre que o usuário:

| Comando do usuário | Ação da skill |
|---|---|
| *"Salve isso no meu vault"* | Cria/atualiza nota com template apropriado |
| *"Lembre disso na próxima sessão"* | Grava nota + adiciona backlink ao MOC |
| *"Qual minha última daily?"* | Retorna `daily/AAAA-MM-DD.md` mais recente |
| *"Liste os papers que já revisei sobre Y"* | `search("Y")` filtrado por `#pesquisai/literature` |
| *"Monte um MOC para o projeto Z"* | Cria `moc/projeto-z.md` agregador |
| *"Sincronize o vault com o Drive"* | `sync_drive()` ou `sync_git()` |
| *"Crie uma nota de revisão sobre X"* | `create_note(..., template="research")` |
| *"O que eu já sei sobre diabetes?"* | `search("diabetes")` ordenado por score |
| *"Quero ativar o segundo cérebro"* | Configura `PESQUISAI_OBSIDIAN_VAULT` |
| *"Abra o vault"* | Retorna o path e sugere plugin Obsidian |

**Não ative** se o usuário estiver pedindo algo puramente conversacional
(perguntas sobre o mundo, geração de código, etc.) — a memória é
**automática** nesses casos, mas o usuário não precisa pedir
explicitamente.

---

## 3. Templates oficiais

A skill vem com **10 templates versionados**, todos sob
`skills/obsidian-memory/templates/`:

| Template | Arquivo | Quando usar |
|---|---|---|
| `daily` | `daily-note.md` | Nota diária automática ao iniciar sessão |
| `research` | `research-note.md` | Estrutura para um projeto de pesquisa |
| `literature` | `literature-note.md` | Revisão de um paper/livro/capítulo |
| `session` | `session-log.md` | Log de uma sessão do agente (criado auto) |
| `methodology` | `methodology-note.md` | Método/estratégia analítica |
| `datasource` | `data-source-note.md` | Fonte de dados (IBGE, DataSUS, …) |
| `hypothesis` | `hypothesis-note.md` | Hipótese de pesquisa (H₁, H₀, …) |
| `reference` | `reference-note.md` | Citação, DOI, BibTeX, anotação |
| `moc` | `project-moc.md` | Map of Content (índice temático) |
| `inbox` | `inbox-note.md` | Captura rápida (default) |

Cada template tem frontmatter YAML padronizado, expõe campos Dataview
e tem seção explícita "Política de Integridade" no rodapé.

---

## 4. Taxonomia oficial de tags

Use **apenas** as tags abaixo para classificar notas:

```
pesquisai/ibge             # dados do IBGE
pesquisai/datasus          # dados do DataSUS
pesquisai/agrobr           # dados do agrobr
pesquisai/dados-brasil     # outros dados BR
pesquisai/capes            # dados da CAPES (Sucupira, etc.)
pesquisai/sucupira         # específico Sucupira

pesquisai/daily            # daily note
pesquisai/research         # projeto de pesquisa
pesquisai/literature       # revisão de literatura
pesquisai/session          # log de sessão
pesquisai/methodology      # método
pesquisai/datasource       # fonte de dados
pesquisai/hypothesis       # hipótese
pesquisai/reference        # citação / referência
pesquisai/moc              # Map of Content
pesquisai/inbox            # captura rápida

pesquisai/draft            # rascunho
pesquisai/review           # em revisão
pesquisai/published        # finalizado
pesquisai/archived         # arquivado
```

Tags customizadas (ex.: `pesquisai/area/educacao`) são permitidas mas
não são indexadas pelo autocompletar.

---

## 5. Como integrar com o OpenCode / agente

A skill é carregada automaticamente quando:

1. O PesquisAI detecta a variável `PESQUISAI_OBSIDIAN_VAULT`
2. O diretório apontado existe
3. O pacote `pesquisai.obsidian` está instalado (default no v0.5.0+)

Exemplo de uso dentro do agente:

```python
from pesquisai.obsidian import ObsidianMemory, ObsidianMemoryStatus

mem = ObsidianMemory.from_env()

if mem.status == ObsidianMemoryStatus.READY:
    # 1. Carrega contexto
    for daily in mem.recent_daily_notes(limit=3):
        mem.add_to_context(daily)

    # 2. Inicia sessão
    mem.start_session()
    mem.log_request(user_input)
    mem.use_skill("ibge-br")

    # 3. Cria nota
    note = mem.create_note(
        "research/diabetes-prevalencia.md",
        title="Prevalência de Diabetes no Brasil",
        template="research",
        tags=("pesquisai/ibge", "pesquisai/datasus"),
        context={"research_question": "Qual a tendência 2010-2024?"},
    )
    # ... preenche o corpo ...
    mem.update_note(note, append=resultados_ibge)

    # 4. Encerra
    mem.end_session(summary="Levantamento inicial da prevalência de diabetes")
    mem.sync_drive(mirror="/content/drive/My Drive/PesquisAI/vault-mirror")
else:
    # Fallback: PesquisAI continua funcionando sem memória
    logger.info("Obsidian memory desativado: %s", mem.status)
```

---

## 6. Setup mínimo

```bash
# 1. Definir a variável (no shell ou no Colab)
export PESQUISAI_OBSIDIAN_VAULT="/content/drive/My Drive/PesquisAI/vault"

# 2. Criar a estrutura do vault
./scripts/init_vault.sh

# 3. Instalar a skill dentro do Obsidian (no desktop)
./scripts/install_plugin.sh

# 4. Sincronizar com o Obsidian
./scripts/sync_drive_to_obsidian.sh
```

---

## 7. Limitações e ética

- **Não substitui revisão por pares.** O vault é memória, não verdade.
- **Não faz coleta primária.** Não use a skill para "lembrar" algo que
  não foi dito ou verificado.
- **Não armazena dados pessoais sensíveis** sem anonimizar antes.
- **Citações exigem `citation-management`.** Tags `#pesquisai/reference`
  sem DOI e BibTeX são bloqueadas pela validação.
- **Marcadores de evidência** são preservados no template
  `literature-note.md` (campo `evidence_level`).

---

## 8. Testes

A skill vem com testes pytest em `skills/obsidian-memory/tests/`:

```bash
pytest skills/obsidian-memory/tests/ -v
pytest skills/obsidian-memory/tests/ --cov=pesquisai/obsidian
```

Cobertura mínima exigida: **80%** (definida em `pyproject.toml`).

---

## 9. Referências

- [Obsidian Help — Internal links](https://help.obsidian.md/links)
- [Obsidian Help — Tags](https://help.obsidian.md/tags)
- [Dataview Plugin](https://github.com/blacksmithgu/obsidian-dataview)
- [Remotely Save Plugin](https://github.com/remotely-save/remotely-save)
- [Self-hosted LiveSync](https://github.com/vrtmrz/obsidian-livesync)
- K-Dense `open-notebook` skill (referência conceitual)
- Andy Matuschak — *Evergreen Notes* (modelo de notas atômicas)

---

*PesquisAI · obsidian-memory skill · v0.5.0 · 2026-06-29*
*Compatível com PesquisAI ≥ v0.4.2.3*
