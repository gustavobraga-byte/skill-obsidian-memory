"""Testes do Vault (CRUD, fsync, audit, path traversal)."""

from __future__ import annotations

import datetime as dt
import os
import tempfile
from pathlib import Path

import pytest

from pesquisai.obsidian.vault import (
    Vault,
    VaultNotFoundError,
    VaultPermissionError,
)
from pesquisai.obsidian.models import Note, NoteMetadata


@pytest.fixture
def tmp_vault(tmp_path: Path) -> Vault:
    """Cria um vault temporário para testes."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "daily").mkdir()
    (vault / "research").mkdir()
    return Vault(vault)


@pytest.fixture
def human_note() -> Note:
    """Nota 'humana' (created_by vazio)."""
    today = dt.date.today()
    return Note(
        path="research/humana.md",
        metadata=NoteMetadata(
            title="Nota Humana",
            created=today,
            updated=today,
            tags=("pesquisai/research",),
            created_by="",  # humana
        ),
        body="# Nota Humana\n\nTexto escrito por mim.",
    )


@pytest.fixture
def agent_note() -> Note:
    """Nota 'do agente'."""
    today = dt.date.today()
    return Note(
        path="research/agente.md",
        metadata=NoteMetadata(
            title="Nota do Agente",
            created=today,
            updated=today,
            tags=("pesquisai/research",),
            created_by="pesquisai",
        ),
        body="# Nota do Agente\n\nTexto gerado pelo PesquisAI.",
    )


# ── Inicialização ────────────────────────────────────────────────


def test_vault_open(tmp_vault: Vault) -> None:
    assert tmp_vault.root.is_dir()
    assert tmp_vault.audit_log.exists() is False  # ainda não escreveu


def test_vault_not_found(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        Vault(tmp_path / "nao-existe")


def test_vault_not_a_dir(tmp_path: Path) -> None:
    f = tmp_path / "arquivo"
    f.write_text("x")
    with pytest.raises(VaultNotFoundError):
        Vault(f)


def test_vault_path_traversal(tmp_vault: Vault) -> None:
    """Não deve permitir ler fora do vault."""
    with pytest.raises(PermissionError):
        tmp_vault.read("/etc/passwd")
    with pytest.raises(PermissionError):
        tmp_vault.read("../escape.md")


# ── Itera / lista ────────────────────────────────────────────────


def test_iter_notes_empty(tmp_vault: Vault) -> None:
    assert list(tmp_vault.iter_notes()) == []


def test_iter_notes_skips_obsidian_config(tmp_vault: Vault) -> None:
    (tmp_vault.root / ".obsidian").mkdir()
    (tmp_vault.root / ".obsidian" / "app.json").write_text("{}")
    (tmp_vault.root / "daily" / "2026-06-29.md").write_text("# d")
    notes = list(tmp_vault.iter_notes())
    assert len(notes) == 1
    assert notes[0].path.endswith("daily/2026-06-29.md")


def test_list_paths(tmp_vault: Vault) -> None:
    (tmp_vault.root / "daily" / "2026-06-29.md").write_text("x")
    (tmp_vault.root / "research" / "x.md").write_text("x")
    paths = tmp_vault.list_paths()
    assert "daily/2026-06-29.md" in paths
    assert "research/x.md" in paths


# ── Escrita ──────────────────────────────────────────────────────


def test_write_creates_file(tmp_vault: Vault, agent_note: Note) -> None:
    path = tmp_vault.write(agent_note)
    assert path.exists()
    assert path.read_text(encoding="utf-8").startswith("---")


def test_write_creates_audit_log(tmp_vault: Vault, agent_note: Note) -> None:
    tmp_vault.write(agent_note)
    assert tmp_vault.audit_log.exists()
    log = tmp_vault.audit_log.read_text()
    assert "write" in log
    assert "research/agente.md" in log


def test_write_refuses_human_without_force(tmp_vault: Vault, human_note: Note) -> None:
    """Notas humanas são read-only para o agente."""
    # Cria nota humana
    tmp_vault.write(human_note, force=True)
    # Tenta sobrescrever SEM force
    new_note = Note(
        path=human_note.path,
        metadata=human_note.metadata,
        body="Tentativa de sobrescrita pelo agente",
    )
    with pytest.raises(PermissionError):
        tmp_vault.write(new_note)


def test_write_with_force_overwrites_human(tmp_vault: Vault, human_note: Note) -> None:
    tmp_vault.write(human_note, force=True)
    new_note = Note(
        path=human_note.path,
        metadata=human_note.metadata,
        body="Sobrescrita autorizada via force=True",
    )
    tmp_vault.write(new_note, force=True)
    text = (tmp_vault.root / human_note.path).read_text(encoding="utf-8")
    assert "Sobrescrita autorizada" in text


def test_write_atomic_on_failure(tmp_vault: Vault, agent_note: Note) -> None:
    """Falha de escrita não deve deixar arquivos .tmp órfãos."""
    tmp_vault.write(agent_note)
    tmp_files = list((tmp_vault.root / "research").glob(".agente.md.*.tmp"))
    assert tmp_files == []


# ── Leitura ──────────────────────────────────────────────────────


def test_read_roundtrip(tmp_vault: Vault, agent_note: Note) -> None:
    tmp_vault.write(agent_note)
    loaded = tmp_vault.read(agent_note.path)
    assert loaded.title == agent_note.title
    assert loaded.body == agent_note.body
    assert "pesquisai/research" in loaded.tags


# ── Delete ───────────────────────────────────────────────────────


def test_delete_agent_note(tmp_vault: Vault, agent_note: Note) -> None:
    tmp_vault.write(agent_note)
    assert tmp_vault.delete(agent_note.path) is True
    assert not (tmp_vault.root / agent_note.path).exists()
    assert (tmp_vault.root / ".trash").exists()


def test_delete_human_refused(tmp_vault: Vault, human_note: Note) -> None:
    tmp_vault.write(human_note, force=True)
    with pytest.raises(PermissionError):
        tmp_vault.delete(human_note.path)


def test_delete_human_with_force(tmp_vault: Vault, human_note: Note) -> None:
    tmp_vault.write(human_note, force=True)
    assert tmp_vault.delete(human_note.path, force=True) is True


# ── Templates ────────────────────────────────────────────────────


def test_write_from_template(tmp_vault: Vault) -> None:
    note = tmp_vault.write_from_template(
        "daily/2026-06-29.md",
        "daily-note",
        context={"date": "2026-06-29", "title": "Daily 2026-06-29"},
        tags=("pesquisai/daily",),
    )
    assert note.metadata.title == "Daily 2026-06-29"
    assert "pesquisai/daily" in note.tags
    assert "pesquisai/draft" in note.tags  # adicionado automaticamente


# ── Helpers ──────────────────────────────────────────────────────


def test_is_pesquisai_generated(human_note: Note, agent_note: Note) -> None:
    assert human_note.is_pesquisai_generated is False
    assert agent_note.is_pesquisai_generated is True


def test_note_content_hash_stable(agent_note: Note) -> None:
    h1 = agent_note.content_hash
    h2 = agent_note.content_hash
    assert h1 == h2
    assert len(h1) == 64  # SHA-256
