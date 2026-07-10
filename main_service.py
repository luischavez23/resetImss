from __future__ import annotations

import time

from core.config_manager import ConfigManager
from core.logger import Logger
from core.notifier import Notifier
from core.scheduler import Scheduler
from core.system_controller import SystemController


class ResetIMSSApp:
    """
    Aplicación principal.

    Puede ejecutarse desde consola o desde un
    Servicio de Windows.
    """

    def __init__(self) -> None:

        Logger.configure()

        self._config = ConfigManager()

        self._notifier = Notifier()

        self._system = SystemController(
            self._config
        )

        self._scheduler = Scheduler(
            config=self._config,
            notifier=self._notifier,
            system=self._system,
        )

    def start(self) -> None:
        """
        Inicia la aplicación.
        """

        Logger.info("Iniciando ResetIMSS Service")

        self._scheduler.start()

    def stop(self) -> None:
        """
        Detiene la aplicación.
        """

        Logger.info("Deteniendo ResetIMSS Service")

        self._scheduler.stop()
    
    def wait(self) -> None:
        """
        Mantiene viva la aplicación.
        """

        while True:
            time.sleep(1)


def main():

    app = ResetIMSSApp()

    app.start()

    try:
        app.wait()

    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    main()