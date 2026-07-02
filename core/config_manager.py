from __future__ import annotations

import json
from pathlib import Path


class ConfigManager:
    """
    Se encarga de leer y guardar la configuración
    del programa.
    """

    DEFAULT_CONFIG = {
        "hour": 3,
        "minute": 0,
        "real_restart": True
    }

    def __init__(self, file_name: str = "config.json"):

        self.path = Path(file_name)
        self._config = {}

        self.load()

    def load(self) -> None:
        """
        Lee el archivo JSON.
        Si no existe, crea uno nuevo.
        """

        if not self.path.exists():

            self._config = self.DEFAULT_CONFIG.copy()

            self.save()

            return

        with self.path.open("r", encoding="utf-8") as file:
            self._config = json.load(file)

    def save(self) -> None:
        """
        Guarda la configuración.
        """

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                self._config,
                file,
                indent=4
            )

    @property
    def hour(self) -> int:
        return self._config["hour"]

    @hour.setter
    def hour(self, value: int):

        self._config["hour"] = value

        self.save()

    @property
    def minute(self) -> int:
        return self._config["minute"]

    @minute.setter
    def minute(self, value: int):

        self._config["minute"] = value

        self.save()

    @property
    def real_restart(self) -> bool:
        return self._config["real_restart"]

    @real_restart.setter
    def real_restart(self, value: bool):

        self._config["real_restart"] = value

        self.save()