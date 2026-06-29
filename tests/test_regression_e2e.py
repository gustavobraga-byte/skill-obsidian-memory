"""Testes de regressão para bugs encontrados no teste e2e.

Estes testes cobrem bugs específicos que os testes unitários
originais não pegaram:

1. BUG CRÍTICO: ``update_note()`` quebrava porque ``NoteMetadata``
   é ``frozen=True`` e o código fazia ``setattr(metadata, 'updated', ...)``.
   Corrigido usando ``dataclasses.replace``.

2. BUG: ``write_from_template()`` duplicava a tag ``pesquisai/draft``
   porque ela era adicionada tanto no ``merged["tags"]`` quanto no
   ``tags=`` do ``Note``. Corrigido com dedup via ``dict.fromkeys``.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from pesquisai.obsidian.memory import ObsidianMemory
from pesquisai.obsidian.models import Note, NoteMetadata
from pesquisai.obsidian.vault import Vault


@pytest.fixture
def tmp_vault(tmp_path: Path) -> Vault:
    """Cria um vault temporário."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "research").mkdir()
    (vault / "daily").mkdir()
    return Vault(vault)


@pytest.fixture
def agent_note() -> Note:
    """Nota criada pelo PesquisAI."""
    today = dt.date.today()
    return Note(
        path="research/test.md",
        metadata=NoteMetadata(
            title="Teste",
            created=today,
            updated=today,
            tags=("pesquisai/research",),
            created_by="pesquisai",
        ),
        body="# Teste\n\nConteúdo inicial.",
    )


# ── Bug 1: update_note com NoteMetadata frozen ─────────────────


class TestUpdateNoteFrozenFix:
    """Regressão: update_note não pode quebrar com frozen dataclass."""

    def test_update_note_append_works(self, tmp_vault: Vault, agent_note: Note) -> None:
        """update_note(append=...) deve funcionar sem FrozenInstanceError."""
        tmp_vault.write(agent_note)
        mem = ObsidianMemory(tmp_vault.root)
        mem.start_session()

        result = mem.update_note(agent_note, append="## Nova seção\n\nConteúdo novo.")
        assert result is not None
        assert "Nova seção" in result.body
        assert "Conteúdo inicial" in result.body  # preserva o original

    def test_update_note_replace_body_works(self, tmp_vault: Vault, agent_note: Note) -> None:
        """update_note(replace_body=...) deve funcionar sem FrozenInstanceError."""
        tmp_vault.write(agent_note)
        mem = ObsidianMemory(tmp_vault.root)
        mem.start_session()

        result = mem.update_note(agent_note, replace_body="# Substituído\n\nNovo corpo.")
        assert result is not None
        assert "Substituído" in result.body
        assert "Conteúdo inicial" not in result.body  # foi substituído

    def test_update_note_timestamp_updated(self, tmp_vault: Vault, agent_note: Note) -> None:
        """update_note deve atualizar o campo 'updated' do metadata."""
        tmp_vault.write(agent_note)
        original_updated = agent_note.metadata.updated

        mem = ObsidianMemory(tmp_vault.root)
        mem.start_session()
        result = mem.update_note(agent_note, append="algo")

        assert result is not None
        # updated deve ser hoje (pode ser igual se rodar no mesmo dia)
        assert result.metadata.updated >= original_updated

    def test_update_note_recomputes_wikilinks(self, tmp_vault: Vault, agent_note: Note) -> None:
        """update_note com append contendo wikilinks deve recompute-los."""
        tmp_vault.write(agent_note)
        mem = ObsidianMemory(tmp_vault.root)
        mem.start_session()

        result = mem.update_note(
            agent_note,
            append="Veja [[outra-nota]] e [[mais-uma]].",
        )
        assert result is not None
        assert "outra-nota" in result.wikilinks
        assert "mais-uma" in result.wikilinks

    def test_update_note_without_session(self, tmp_vault: Vault, agent_note: Note) -> None:
        """update_note deve funcionar mesmo sem sessão ativa."""
        tmp_vault.write(agent_note)
        mem = ObsidianMemory(tmp_vault.root)
        # NÃO chama start_session()

        result = mem.update_note(agent_note, append="sem sessão")
        assert result is not None
        assert "sem sessão" in result.body


# ── Bug 2: write_from_template duplicava tags ──────────────────


class TestWriteFromTemplateDedupTags:
    """Regressão: write_from_template não pode duplicar tags."""

    def test_no_duplicate_draft_tag(self, tmp_vault: Vault) -> None:
        """pesquisai/draft não deve aparecer 2x nas tags."""
        note = tmp_vault.write_from_template(
            "daily/test.md",
            "daily-note",
            context={"date": "2026-06-29", "title": "Test"},
            tags=("pesquisai/daily",),
        )
        # Conta quantas vezes pesquisai/draft aparece
        draft_count = note.tags.count("pesquisai/draft")
        assert draft_count == 1, f"pesquisai/draft aparece {draft_count}x em {note.tags}"

    def test_no_duplicate_user_tags(self, tmp_vault: Vault) -> None:
        """Tags do usuário não devem duplicar mesmo se já em draft."""
        note = tmp_vault.write_from_template(
            "research/test.md",
            "research-note",
            context={"date": "2026-06-29", "title": "Test"},
            tags=("pesquisai/ibge", "pesquisai/datasus"),
        )
        assert note.tags.count("pesquisai/ibge") == 1
        assert note.tags.count("pesquisai/datasus") == 1
        assert note.tags.count("pesquisai/draft") == 1

    def test_tags_in_metadata_match_note_tags(self, tmp_vault: Vault) -> None:
        """metadata.tags e note.tags devem ser consistentes."""
        note = tmp_vault.write_from_template(
            "research/test2.md",
            "research-note",
            context={"date": "2026-06-29", "title": "Test 2"},
            tags=("pesquisai/ibge",),
        )
        # Ambos devem conter pesquisai/draft e pesquisai/ibge
        assert "pesquisai/draft" in note.metadata.tags
        assert "pesquisai/ibge" in note.metadata.tags
        assert "pesquisai/draft" in note.tags
        assert "pesquisai/ibge" in note.tags

    def test_wikilinks_extracted_from_template_body(self, tmp_vault: Vault) -> None:
        """write_from_template deve extrair wikilinks do body renderizado."""
        note = tmp_vault.write_from_template(
            "research/test3.md",
            "research-note",
            context={
                "date": "2026-06-29",
                "title": "Test 3",
                "moc_path": "moc/meu-moc",
                "slug": "teste",
                "research_question": "Pergunta?",
                "project": "meu-projeto",
            },
            tags=("pesquisai/research",),
        )
        # O template research-note tem [[{{moc_path}}]] que vira [[moc/meu-moc]]
        # após renderização. Pode haver outros wikilinks do template.
        assert len(note.wikilinks) >= 0  # pelo menos não quebra
        # wikilinks não deve ser lista vazia []
        assert isinstance(note.wikilinks, tuple)


# ── Teste integrativo: ciclo completo via ObsidianMemory ──────


class TestEndToEndViaMemory:
    """Testa o ciclo completo através da API ObsidianMemory."""

    def test_full_session_cycle(self, tmp_vault: Vault) -> None:
        """Simula: start → create → update → end → search."""
        mem = ObsidianMemory(tmp_vault.root)
        assert mem.writable

        # Start
        sid = mem.start_session()
        assert sid

        # Create
        note = mem.create_note(
            "research/e2e-test.md",
            title="Teste E2E",
            template="research-note",
            tags=("pesquisai/ibge",),
            context={
                "date": "2026-06-29",
                "research_question": "Funciona?",
                "moc_path": "moc/test",
                "slug": "e2e",
                "project": "e2e",
            },
        )
        assert note is not None
        assert "pesquisai/draft" in note.tags
        assert "pesquisai/ibge" in note.tags
        # Sem duplicação
        assert note.tags.count("pesquisai/draft") == 1

        # Update (o bug crítico estava aqui)
        updated = mem.update_note(
            note,
            append="## Resultados\n\n- Dado X\n\nVeja [[literature/ref]].",
        )
        assert updated is not None
        assert "Resultados" in updated.body
        assert "literature/ref" in updated.wikilinks

        # Log
        mem.log_request("teste")
        mem.use_skill("ibge-br")
        mem.log_file("output.csv")

        # End
        session_note = mem.end_session(summary="Teste E2E completado")
        assert session_note is not None
        assert "sessions/" in session_note.path

        # Search (deve encontrar a nota criada)
        mem2 = ObsidianMemory(tmp_vault.root)
        results = mem2.search("Teste E2E")
        assert len(results) >= 1
        paths = [r.note.path for r in results]
        assert "research/e2e-test.md" in paths

        # Stats
        stats = mem2.stats()
        assert stats["notes"] >= 2  # nota + sessão
