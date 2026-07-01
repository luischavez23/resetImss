from __future__ import annotations

import os

from core.config_manager import ConfigManager


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

        if self._config.real_restart:
            os.system("shutdown /r /t 0")
        else:
            print("\n[SIMULACIÓN] Reinicio del sistema.")

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