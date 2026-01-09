#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários compartilhados para scripts de ferramentas.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Union


def atomic_write(filepath: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
    """
    Escreve conteúdo em arquivo de forma atômica.

    Usa o padrão write-to-temp-then-rename para garantir que:
    - Se a escrita falhar, o arquivo original permanece intacto
    - Não há janela de tempo com arquivo corrompido

    Args:
        filepath: Caminho do arquivo de destino
        content: Conteúdo a ser escrito
        encoding: Encoding do arquivo (default: utf-8)

    Raises:
        OSError: Se falhar a escrita ou rename
    """
    filepath = Path(filepath)

    # Criar diretório pai se não existir
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Escrever em arquivo temporário no mesmo diretório (para garantir mesmo filesystem)
    fd, tmp_path = tempfile.mkstemp(
        suffix='.tmp',
        prefix=filepath.stem + '_',
        dir=filepath.parent
    )

    try:
        # Escrever conteúdo
        with os.fdopen(fd, 'w', encoding=encoding) as tmp_file:
            tmp_file.write(content)

        # Renomear atomicamente (funciona no mesmo filesystem)
        os.replace(tmp_path, filepath)

    except Exception:
        # Limpar arquivo temporário em caso de erro
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def safe_read(filepath: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Lê arquivo com tratamento de erros melhorado.

    Args:
        filepath: Caminho do arquivo
        encoding: Encoding do arquivo (default: utf-8)

    Returns:
        Conteúdo do arquivo

    Raises:
        FileNotFoundError: Se arquivo não existir
        PermissionError: Se não tiver permissão de leitura
        UnicodeDecodeError: Se encoding estiver incorreto
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    if not filepath.is_file():
        raise ValueError(f"Caminho não é um arquivo: {filepath}")

    return filepath.read_text(encoding=encoding)
