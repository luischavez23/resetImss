from __future__ import annotations

import json
import os

from core.logger import Logger
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

        base_path = self._get_base_path()
        self.path = base_path / file_name
        self._config = {}
        self.load()

    # ---------------------------------------------------------
    # Métodos públicos
    # ---------------------------------------------------------
    @staticmethod
    def _get_base_path() -> Path:
        """
        Carpeta donde se guarda la configuración compartida.
        """

        base = Path(os.environ["PROGRAMDATA"]) / "ResetIMSS"
        base.mkdir(parents=True, exist_ok=True)

        return base
    
    def load(self) -> None:
        """
        Lee el archivo JSON.
        Si no existe, carga la configuración por defecto.
        """

        if not self.path.exists():

            Logger.warning(
                "No existe config.json."
            )

            self._config = self.DEFAULT_CONFIG.copy()
            
            self._last_modified = 0

            return

        try:

            with self.path.open(
                "r",
                encoding="utf-8"
            ) as file:

                self._config = json.load(file)

            self._last_modified = os.path.getmtime(self.path)

        except json.JSONDecodeError:

            Logger.error(
                "config.json está dañado. "
                "Se cargará la configuración por defecto."
            )

            self._config = self.DEFAULT_CONFIG.copy()

            self.save()

        except OSError as ex:

            Logger.error(
                f"No fue posible leer config.json: {ex}"
            )

    def save(self) -> None:
        try:

            self.path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with self.path.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self._config,
                    file,
                    indent=4
                )

            self._last_modified = os.path.getmtime(self.path)

            Logger.info(
                f"Configuración guardada en: {self.path}"
            )

        except OSError as ex:

            Logger.error(
                f"No fue posible guardar config.json: {ex}"
            )
            
    def has_changed(self) -> bool:
        """
        Indica si el archivo de configuración fue modificado.
        """

        if not self.path.exists():
            return False

        current_modified = os.path.getmtime(self.path)

        if current_modified != self._last_modified:
            self._last_modified = current_modified
            return True

        return False
    
    def update(
        self,
        hour: int,
        minute: int,
        real_restart: bool,
    ) -> None:
        """
        Actualiza toda la configuración y la guarda una sola vez.
        """

        self._config["hour"] = hour
        self._config["minute"] = minute
        self._config["real_restart"] = real_restart

        self.save()
    
    # ---------------------------------------------------------
    # Propiedades
    # ---------------------------------------------------------

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
    
    @property
    def loaded(self) -> bool:
        return bool(self._config)