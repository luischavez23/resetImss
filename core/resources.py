from __future__ import annotations

import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta correcta de recursos.

    Funciona:
    - Desarrollo.
    - PyInstaller.
    """

    if getattr(sys, "frozen", False):

        base_path = Path(sys._MEIPASS)

    else:

        base_path = Path(__file__).resolve().parent.parent

    return str(base_path / relative_path)