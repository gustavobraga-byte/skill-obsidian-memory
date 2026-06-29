"""Testes do LinkIndex (wikilinks + backlinks + resolução)."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from pesquisai.obsidian.links import (
    LinkIndex,
    _normalize_title,
    _strip_accents,
    find_mentionable_terms,
    make_wikilink,
    replace_in_text,
)
from pesquisai.obsidian.models import Note, NoteMetadata, extract_wikilinks
from pesquisai.obsidian.vault import Vault


@pytest.fixture
def sample_notes() -> list[Note]:
    today = dt.date.today()
    return [
        Note(
            path="research/diabetes.md",
            metadata=NoteMetadata(
                title="Prevalência de Diabetes",
                created=today,
                updated=today,
                tags=("pesquisai/research",),
                created_by="pesquisai",
            ),
            body="A [[hipertensão]] é um fator de risco.\nVeja [[obesidade]].",
            wikilinks=extract_wikilinks(
                "A [[hipertensão]] é um fator de risco.\nVeja [[obesidade]]."
            ),
        ),
        Note(
            path="research/hipertensao.md",
            metadata=NoteMetadata(
                title="Hipertensão Arterial",
                created=today,
                updated=today,
                tags=("pesquisai/research",),
                created_by="pesquisai",
            ),
            body="A hipertensão está associada a [[diabetes]].",
            wikilinks=extract_wikilinks(
                "A hipertensão está associada a [[diabetes]]."
            ),
        ),
        Note(
            path="research/obesidade.md",
            metadata=NoteMetadata(
                title="Obesidade Infantil",
                created=today,
                updated=today,
                tags=("pesquisai/research",),
                created_by="pesquisai",
            ),
            body="Sem links.",
            wikilinks=(),
        ),
    ]


# ── Helpers ──────────────────────────────────────────────────────


def test_strip_accents() -> None:
    assert _strip_accents("PesquisAÇÃO") == "PesquisACAO"
    assert _strip_accents("não") == "nao"


def test_normalize_title() -> None:
    assert _normalize_title("PNAE em MG") == "pnae em mg"
    assert _normalize_title("Obesidade") == "obesidade"
    assert _normalize_title("Ação") == "acao"


def test_extract_wikilinks_simple() -> None:
    text = "Veja [[diabetes]] e [[obesidade]]."
    assert extract_wikilinks(text) == ("diabetes", "obesidade")


def test_extract_wikilinks_with_heading() -> None:
    text = "Método em [[metodologia#regressão]]"
    assert extract_wikilinks(text) == ("metodologia",)


def test_extract_wikilinks_with_alias() -> None:
    text = "Veja [[diabetes|a doença]]"
    assert extract_wikilinks(text) == ("diabetes",)


def test_extract_wikilinks_dedup() -> None:
    # Dedup é case-sensitive (a normalização case-insensitive
    # é feita no LinkIndex). Aqui testamos apenas dedup exato.
    text = "[[x]] e [[x]] e [[y]]"
    assert extract_wikilinks(text) == ("x", "y")


def test_make_wikilink() -> None:
    assert make_wikilink("alvo") == "[[alvo]]"
    assert make_wikilink("alvo", alias="apelido") == "[[alvo|apelido]]"


# ── LinkIndex ────────────────────────────────────────────────────


def test_index_adds_notes(sample_notes: list[Note]) -> None:
    idx = LinkIndex()
    for n in sample_notes:
        idx.add_note(n)
    stats = idx.stats()
    assert stats["notes"] == 3
    assert stats["targets"] >= 3
    assert stats["edges"] >= 3


def test_resolve_case_insensitive(sample_notes: list[Note]) -> None:
    idx = LinkIndex()
    for n in sample_notes:
        idx.add_note(n)
    # Case insensitive
    assert idx.resolve("DIABETES") is not None
    # Accent insensitive
    assert idx.resolve("HIPERTENSAO") is not None
    # Stem (sem path prefix)
    assert idx.resolve("obesidade") is not None


def test_backlinks(sample_notes: list[Note]) -> None:
    idx = LinkIndex()
    for n in sample_notes:
        idx.add_note(n)
    # diabetes tem 1 backlink (hipertensão)
    bl = idx.backlinks("research/diabetes.md")
    assert "research/hipertensao.md" in bl


def test_backlinks_by_title(sample_notes: list[Note]) -> None:
    idx = LinkIndex()
    for n in sample_notes:
        idx.add_note(n)
    # hipertensão é backlink de diabetes
    bl = idx.backlinks("hipertensao")
    assert "research/diabetes.md" in bl


def test_outgoing(sample_notes: list[Note]) -> None:
    idx = LinkIndex()
    for n in sample_notes:
        idx.add_note(n)
    out = idx.outgoing("research/diabetes.md")
    # O índice normaliza (sem acentos) — testamos o normalizado
    assert "hipertensao" in out
    assert "obesidade" in out


def test_remove_note(sample_notes: list[Note]) -> None:
    idx = LinkIndex()
    for n in sample_notes:
        idx.add_note(n)
    before = len(idx.backlinks("obesidade"))
    idx.remove_note("research/diabetes.md")
    after = idx.backlinks("obesidade")
    assert len(after) < before or after == ()


def test_from_vault(tmp_path: Path, sample_notes: list[Note]) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "research").mkdir()
    v = Vault(vault)
    for n in sample_notes:
        v.write(n)
    idx = LinkIndex.from_vault(v)
    assert idx.stats()["notes"] == 3


# ── replace_in_text ──────────────────────────────────────────────


def test_replace_in_text() -> None:
    text = "Diabetes é uma doença crônica. diabetes mellitus tipo 2."
    out = replace_in_text(text, {"diabetes": "diabetes-conceito"})
    assert "[[diabetes-conceito]]" in out
    # Word boundary — não deve substituir "diabético"
    out2 = replace_in_text("O paciente diabético.", {"diabetes": "X"})
    assert "[[X]]" not in out2
    assert "diabético" in out2


def test_find_mentionable_terms(sample_notes: list[Note]) -> None:
    terms = find_mentionable_terms(sample_notes)
    assert "research/diabetes.md" in terms
    assert "Prevalência de Diabetes" in terms["research/diabetes.md"]
