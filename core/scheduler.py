from __future__ import annotations

import datetime
import math
import threading
import time


from core.config_manager import ConfigManager
from core.notifier import Notifier
from core.notifier_window import NotifierWindow
from core.logger import Logger
from core.system_controller import SystemController


class Scheduler:
    """
    Se encarga de monitorear el horario configurado para
    realizar el reinicio del equipo.

    Responsabilidades:
        - Calcular el tiempo restante.
        - Mostrar avisos.
        - Ejecutar el reinicio.
    """

    # Minutos antes del reinicio en los que se mostrará un aviso
    NOTIFICATION_MINUTES = (10, 5)

    # Intervalo de revisión (segundos)
    CHECK_INTERVAL = 20

    def __init__(
        self,
        config: ConfigManager,
        notifier: Notifier,
        system: SystemController,
    ) -> None:

        self._config = config
        self._notifier = notifier
        self._system = system

        self._running = False
        self._thread: threading.Thread | None = None

        # Guarda los avisos que ya fueron enviados
        self._notifications_sent: set[int] = set()
        
        self._next_restart: datetime.datetime | None = None
        self._notification_open = False

    # ---------------------------------------------------------
    # Métodos públicos
    # ---------------------------------------------------------

    def start(self) -> None:
        """
        Inicia el monitor en un hilo independiente.
        """

        if self._running:
            return
        
        self._next_restart = self._calculate_next_restart()

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )
        

        self._thread.start()

    def stop(self) -> None:
        """
        Detiene el monitor.
        """

        self._running = False

        if self._thread:
            self._thread.join()

    # ---------------------------------------------------------
    # Métodos privados
    # ---------------------------------------------------------
    def _run(self) -> None:
        Logger.info("Scheduler iniciado")

        while self._running:
            changed = self._config.has_changed()
            Logger.info(f"has_changed = {changed}")
            try:
                if changed:
                    Logger.info("Se detectó cambio en config.json")
                    self._config.load()
                    self.reload_schedule()

                minutes_left = self._minutes_until_restart()

                self._print_status(minutes_left)
                
                self._check_notifications(minutes_left)

                Logger.info(f"minutes_left={minutes_left}")

                if datetime.datetime.now() >= self._next_restart:
                    Logger.info("Se alcanzó la hora programada")
                    self._restart()
                    time.sleep(60)
                    continue

                # Durante el último minuto revisar cada segundo
                if minutes_left <= 1:
                    time.sleep(1)
                else:
                    time.sleep(self.CHECK_INTERVAL)

            except Exception as ex:
                Logger.error(f"Error en Scheduler: {ex}", exc_info=True)

    def _minutes_until_restart(self) -> int:
        """
        Calcula los minutos restantes hasta el próximo reinicio.
        """

        if self._next_restart is None:
            self._next_restart = self._calculate_next_restart()

        difference = self._next_restart - datetime.datetime.now()

        return max(
            0,
            math.ceil(difference.total_seconds() / 60),
        )
        
    def _print_status(
        self,
        minutes_left: int,
    ) -> None:
        Logger.info(
            f"Hora actual: "
            f"{datetime.datetime.now():%H:%M:%S} | "
            f"Reinicio: "
            f"{self._next_restart:%H:%M} | "
            f"Restan {minutes_left} minutos"
        )
      
        
    def _check_notifications(
        self,
        minutes_left: int,
    ) -> None:
        """
        Verifica si debe mostrarse un aviso.
        """

        if minutes_left not in self.NOTIFICATION_MINUTES:
            return

        if minutes_left in self._notifications_sent:
            return

        Logger.info(
            f"Mostrando notificación de {minutes_left} minutos"
        )
        
        if self._notification_open:
            return

        self._notification_open = True

        NotifierWindow.show(
            minutes_left=minutes_left,
            restart_time=self._next_restart.strftime("%H:%M"),
            on_postpone=self._postpone_restart,
            on_close=self._notification_closed,
        )

        self._notifications_sent.add(minutes_left)
    
    def _calculate_next_restart(self) -> datetime.datetime:
        """
        Calcula la próxima fecha y hora de reinicio.
        """

        now = datetime.datetime.now()

        target = now.replace(
            hour=self._config.hour,
            minute=self._config.minute,
            second=0,
            microsecond=0,
        )

        if target <= now:
            target += datetime.timedelta(days=1)

        return target
    def _postpone_restart(self) -> None:
        """
        Pospone el reinicio 10 minutos.
        """

        self._next_restart += datetime.timedelta(minutes=10)

        self._notifications_sent.clear()

        Logger.info(
            f"Nuevo reinicio: {self._next_restart:%H:%M}"
        )
    
    def _notification_closed(self) -> None:
        self._notification_open = False
        
    def reload_schedule(self) -> None:
        """
        Recalcula la siguiente hora de reinicio cuando cambia
        la configuración.
        """
        self._next_restart = self._calculate_next_restart()
        self._notifications_sent.clear()
        Logger.info(f"Nuevo horario cargado: {self._config.hour:02}:{self._config.minute:02}")

    def _restart(self) -> None:
        Logger.info("Entrando a _restart()")

        self._system.restart()

        Logger.info("Finalizó SystemController.restart()")

        self._next_restart = self._calculate_next_restart()
        self._notifications_sent.clear()