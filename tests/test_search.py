"""Testes do Searcher (busca textual + tags + BM25)."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from pesquisai.obsidian.models import Note, NoteMetadata, extract_tags
from pesquisai.obsidian.search import (
    Searcher,
    _normalize_text,
    _snippet,
    _tokenize,
)
from pesquisai.obsidian.vault import Vault


@pytest.fixture
def vault_with_notes(tmp_path: Path) -> Vault:
    """Cria um vault com 5 notas para testar busca."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "research").mkdir()
    (vault / "literature").mkdir()

    today = dt.date.today()
    notes = [
        Note(
            path="research/diabetes.md",
            metadata=NoteMetadata(
                title="Prevalência de Diabetes",
                created=today,
                updated=today,
                tags=("pesquisai/research", "pesquisai/ibge"),
                created_by="pesquisai",
            ),
            body=(
                "A prevalência de diabetes mellitus no Brasil é de 10,2% "
                "segundo o VIGITEL 2023. A doença é mais comum em pessoas "
                "com menor escolaridade e maiores de 65 anos."
            ),
        ),
        Note(
            path="research/hipertensao.md",
            metadata=NoteMetadata(
                title="Hipertensão Arterial",
                created=today,
                updated=today,
                tags=("pesquisai/research", "pesquisai/datasus"),
                created_by="pesquisai",
            ),
            body=(
                "A hipertensão afeta 25% da população adulta brasileira. "
                "É o principal fator de risco para AVC e infarto."
            ),
        ),
        Note(
            path="literature/santos-2024.md",
            metadata=NoteMetadata(
                title="Santos (2024) — PNAE em MG",
                created=today,
                updated=today,
                tags=("pesquisai/literature",),
                created_by="pesquisai",
                citekey="santos2024pnae",
                doi="10.1590/0034-7612202400000",
            ),
            body=(
                "Este artigo analisa a execução do PNAE nos municípios "
                "mineiros entre 2015 e 2023. Usa dados do FNDE e do IBGE."
            ),
        ),
        Note(
            path="research/obesidade.md",
            metadata=NoteMetadata(
                title="Obesidade Infantil",
                created=today,
                updated=today,
                tags=("pesquisai/research", "pesquisai/datasus"),
                created_by="pesquisai",
            ),
            body=(
                "A obesidade em crianças cresceu 300% nas últimas três "
                "décadas, segundo dados do SISVAN."
            ),
        ),
        Note(
            path="daily/2026-06-29.md",
            metadata=NoteMetadata(
                title="Daily 2026-06-29",
                created=today,
                updated=today,
                tags=("pesquisai/daily",),
                created_by="pesquisai",
            ),
            body="Levantamento inicial sobre diabetes.\n#pesquisai/draft",
        ),
    ]
    v = Vault(vault)
    for n in notes:
        v.write(n)
    return v


# ── Helpers ──────────────────────────────────────────────────────


def test_normalize_text() -> None:
    assert _normalize_text("PNAE") == "pnae"
    assert _normalize_text("Ação") == "acao"
    assert _normalize_text("PESQUISA") == "pesquisa"


def test_tokenize_removes_stopwords() -> None:
    tokens = _tokenize("o diabetes é uma doença crônica e silenciosa")
    # "o", "é", "uma", "e" são stopwords
    # A função normaliza para lowercase + remove acentos
    assert "diabetes" in tokens
    assert "doenca" in tokens  # acento removido na normalização
    assert "cronica" in tokens  # acento removido na normalização
    assert "silenciosa" in tokens
    assert "o" not in tokens
    assert "e" not in tokens
    # Note: "é" -> "e" e "e" -> "e" colidem. O resultado é só "e" removido.


def test_tokenize_keeps_covid_hyphen() -> None:
    tokens = _tokenize("covid-19 pandêmico")
    assert "covid-19" in tokens
    assert "pandemico" in tokens  # acento removido


def test_snippet_with_match() -> None:
    text = "abcdef " * 50 + "DIABETES" + " ghijkl" * 50
    s = _snippet(text, "diabetes")
    assert "…" in s  # tem elipse
    assert "diabetes" in s.lower()


def test_snippet_no_match() -> None:
    s = _snippet("texto sem match", "diabetes")
    assert s == "texto sem match"


def test_extract_tags() -> None:
    text = "Hoje eu trabalho com #pesquisai/ibge e #pesquisai/datasus. Nada de código `#ignore`."
    tags = extract_tags(text)
    assert "pesquisai/ibge" in tags
    assert "pesquisai/datasus" in tags
    assert "ignore" not in tags  # tag em code span é ignorada


def test_extract_tags_skips_code_fences() -> None:
    text = (
        "#tag-real\n"
        "```python\n"
        "#isso-nao-e-tag\n"
        "```\n"
        "#outra-real"
    )
    tags = extract_tags(text)
    assert "tag-real" in tags
    assert "outra-real" in tags
    assert "isso-nao-e-tag" not in tags


# ── Searcher ─────────────────────────────────────────────────────


def test_searcher_rebuild(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    s.rebuild()
    stats = s.stats()
    assert stats["notes"] == 5
    assert stats["tags"] >= 5


def test_search_finds_relevant(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    results = s.search("diabetes", limit=5)
    assert len(results) >= 1
    # A nota de diabetes deve ser a primeira
    assert "diabetes" in results[0].note.path


def test_search_returns_snippet(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    results = s.search("VIGITEL", limit=5)
    assert len(results) >= 1
    assert "VIGITEL" in results[0].snippet or "10,2%" in results[0].snippet


def test_search_filters_by_tag(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    # "prevalência" só está em diabetes (com tag ibge)
    results = s.search("prevalência", tags=["pesquisai/ibge"], limit=5)
    assert all("pesquisai/ibge" in r.note.tags for r in results)


def test_by_tag(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    datasus_notes = s.by_tag("pesquisai/datasus")
    assert len(datasus_notes) == 2  # hipertensão + obesidade
    paths = {n.path for n in datasus_notes}
    assert "research/hipertensao.md" in paths
    assert "research/obesidade.md" in paths


def test_by_path_prefix(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    research = s.by_path_prefix("research/")
    assert len(research) == 3
    literature = s.by_path_prefix("literature/")
    assert len(literature) == 1


def test_get_by_path(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    n = s.note("research/diabetes.md")
    assert n is not None
    assert n.title == "Prevalência de Diabetes"


def test_search_case_and_accent_insensitive(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    # "hipertensão" tem acento, "hipertensao" não
    r1 = s.search("hipertensão")
    r2 = s.search("hipertensao")
    assert len(r1) == len(r2)
    assert r1[0].note.path == r2[0].note.path


def test_search_empty_query(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    assert s.search("") == []
    assert s.search("   ") == []


def test_search_invalidates_on_invalidate(vault_with_notes: Vault) -> None:
    s = Searcher(vault_with_notes)
    s.rebuild()
    s.invalidate()
    # Deve reconstruir no próximo acesso
    assert s.stats()["notes"] == 5
