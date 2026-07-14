from __future__ import annotations

import os

from core.config_manager import ConfigManager
import subprocess

from core.logger import Logger


class SystemController:
    """
    Encapsula todas las acciones relacionadas con el sistema operativo.
    """

    def __init__(self, config: ConfigManager) -> None:
        self._config = config

    def restart(self) -> None:
        """
        Reinicia el equipo.
        """

        Logger.info(f"real_restart = {self._config.real_restart}")

        if not self._config.real_restart:
            Logger.info("[SIMULACIÓN] Reinicio del sistema.")
            return

        Logger.info("Ejecutando: shutdown /r /t 0")

        result = subprocess.run(
            ["shutdown", "/r", "/f","/t", "0"],
            capture_output=True,
            text=True,
        )

        Logger.info(f"Código de salida: {result.returncode}")
        Logger.info(f"stdout: {result.stdout}")
        Logger.info(f"stderr: {result.stderr}")

    def shutdown(self) -> None:
        """
        Apaga el equipo.
        """

        if self._config.real_restart:
            os.system("shutdown /s /t 0")
        else:
            print("\n[SIMULACIÓN] Apagado del sistema.")

    def logoff(self) -> None:
        """
        Cierra la sesión del usuario.
        """

        if self._config.real_restart:
            os.system("shutdown /l")
        else:
            print("\n[SIMULACIÓN] Cerrar sesión.")

    def lock(self) -> None:
        """
        Bloquea el equipo.
        """

        if self._config.real_restart:
            os.system("rundll32.exe user32.dll,LockWorkStation")
        else:
            print("\n[SIMULACIÓN] Bloquear equipo.")