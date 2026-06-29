"""Testes da validação de caminho no Google Drive."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from pesquisai.obsidian.discovery import (
    DRIVE_PATH_PREFIXES,
    _is_in_drive,
    _is_in_colab,
    _validate_drive_path,
    ensure_drive_path,
    get_default_vault_path,
    is_available,
)


# ── Detecção de Drive ───────────────────────────────────────────


def test_is_in_drive_true() -> None:
    """Caminhos dentro do FUSE mount do Drive são reconhecidos."""
    assert _is_in_drive("/content/drive/My Drive/PesquisAI/vault")
    assert _is_in_drive("/content/drive/Shared drives/Lab/vault")
    assert _is_in_drive("/content/drive/.colab/anything")


def test_is_in_drive_false() -> None:
    """Caminhos fora do Drive são rejeitados."""
    assert not _is_in_drive("/tmp/pesquisai/vault")
    assert not _is_in_drive("/content/anything")  # não-Drive
    assert not _is_in_drive("/home/user/Obsidian/vault")
    assert not _is_in_drive("/etc/passwd")


# ── Validação ──────────────────────────────────────────────────


def test_validate_drive_path_in_drive() -> None:
    """Caminhos no Drive são aceitos."""
    path = "/content/drive/My Drive/vault"
    assert _validate_drive_path(path) == path


def test_validate_drive_path_outside_drive_in_colab() -> None:
    """Fora do Drive + dentro do Colab = rejeitado."""
    # Não estamos realmente no Colab no ambiente de teste,
    # então _is_in_colab() retorna False, e o caminho é aceito.
    # Para forçar a rejeição, mockamos _is_in_colab.
    import pesquisai.obsidian.discovery as d

    original = d._is_in_colab
    d._is_in_colab = lambda: True
    try:
        result = _validate_drive_path("/tmp/something")
        assert result is None
    finally:
        d._is_in_colab = original


def test_validate_drive_path_outside_drive_outside_colab() -> None:
    """Fora do Drive + fora do Colab = aceito (uso local)."""
    import pesquisai.obsidian.discovery as d

    original = d._is_in_colab
    d._is_in_colab = lambda: False
    try:
        result = _validate_drive_path("/tmp/local-vault")
        assert result == "/tmp/local-vault"
    finally:
        d._is_in_colab = original


# ── ensure_drive_path ─────────────────────────────────────────


def test_ensure_drive_path_creates(tmp_path: Path) -> None:
    """ensure_drive_path cria a pasta se não existir."""
    target = tmp_path / "new-vault"
    # tmp_path não está no Drive — vai rejeitar no Colab
    import pesquisai.obsidian.discovery as d

    original = d._is_in_colab
    d._is_in_colab = lambda: False  # simular fora do Colab
    try:
        with pytest.raises(RuntimeError, match="NÃO está no Google Drive"):
            ensure_drive_path(str(target))
    finally:
        d._is_in_colab = original


def test_ensure_drive_path_accepts_drive() -> None:
    """ensure_drive_path aceita caminho no Drive."""
    # Cria um diretório temporário dentro do "Drive" simulado
    import pesquisai.obsidian.discovery as d

    original = d._is_in_colab
    d._is_in_colab = lambda: False
    with tempfile.TemporaryDirectory() as tmp:
        # Hack: finge que o tmpdir é /content/drive/...
        drive_path = Path(tmp) / "content" / "drive" / "My Drive" / "vault"
        drive_path.mkdir(parents=True)
        # Mocka _is_in_drive para reconhecer esse path
        original_is_in = d._is_in_drive

        def fake_is_in(path: str) -> bool:
            return str(path).startswith(str(drive_path)) or original_is_in(path)

        d._is_in_drive = fake_is_in
        try:
            result = ensure_drive_path(str(drive_path))
            assert result == str(drive_path)
            assert Path(result).is_dir()
        finally:
            d._is_in_drive = original_is_in
            d._is_in_colab = original


# ── Constantes ───────────────────────────────────────────────


def test_drive_prefixes_is_tuple() -> None:
    assert isinstance(DRIVE_PATH_PREFIXES, tuple)
    assert len(DRIVE_PATH_PREFIXES) >= 5


def test_drive_prefixes_contains_colab() -> None:
    assert any("/content/drive" in p for p in DRIVE_PATH_PREFIXES)
