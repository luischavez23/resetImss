from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any


class RuntimeManager:
    """
    Intercambia información entre ResetIMSSCore y
    ResetIMSSNotifier mediante archivos en ProgramData.
    """

    def __init__(self) -> None:
        self.base_path = (
            Path(os.environ["PROGRAMDATA"])
            / "ResetIMSS"
        )

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.state_path = self.base_path / "runtime.json"
        self.command_path = self.base_path / "command.json"

    def save_state(
        self,
        next_restart: datetime.datetime,
    ) -> None:
        """
        Publica la siguiente fecha y hora de reinicio.
        """

        data = {
            "next_restart": next_restart.isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        self._write_json_atomic(
            path=self.state_path,
            data=data,
        )

    def load_state(self) -> dict[str, Any] | None:
        """
        Lee el estado publicado por ResetIMSSCore.
        """

        return self._read_json(self.state_path)

    def request_postpone(
        self,
        minutes: int = 10,
    ) -> None:
        """
        Registra una solicitud de posposición.
        """

        data = {
            "command": "postpone",
            "minutes": minutes,
            "created_at": datetime.datetime.now().isoformat(),
        }

        self._write_json_atomic(
            path=self.command_path,
            data=data,
        )

    def consume_command(self) -> dict[str, Any] | None:
        """
        Lee y elimina una orden pendiente.
        Solo debe ser utilizado por ResetIMSSCore.
        """

        data = self._read_json(self.command_path)

        if data is None:
            return None

        try:
            self.command_path.unlink(missing_ok=True)
        except OSError:
            return None

        return data

    @staticmethod
    def _read_json(
        path: Path,
    ) -> dict[str, Any] | None:

        if not path.exists():
            return None

        try:
            with path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return None

        return None

    @staticmethod
    def _write_json_atomic(
        path: Path,
        data: dict[str, Any],
    ) -> None:
        """
        Guarda primero en un archivo temporal y después lo
        reemplaza, evitando lecturas de JSON incompleto.
        """

        temporary_path = path.with_suffix(".tmp")

        with temporary_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

        temporary_path.replace(path)