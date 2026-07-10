from __future__ import annotations

import datetime
import threading
import time

from core.config_manager import ConfigManager
from core.notifier import Notifier
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
        """
        Bucle principal del monitor.
        """

        while self._running:

            # Si cambió el archivo de configuración,
            # recarga la configuración.
            if self._config.has_changed():
                self._config.load()
                self.reload_schedule()

            minutes_left = self._minutes_until_restart()

            self._print_status(minutes_left)

            self._check_notifications(minutes_left)

            if minutes_left == 0:

                self._restart()

                time.sleep(60)

            time.sleep(self.CHECK_INTERVAL)

    def _minutes_until_restart(self) -> int:
        """
        Calcula los minutos restantes hasta el próximo reinicio.
        """

        if self._next_restart is None:
            self._next_restart = self._calculate_next_restart()

        difference = self._next_restart - datetime.datetime.now()

        return max(
            0,
            int(difference.total_seconds() // 60)
        )
        
    def _print_status(
        self,
        minutes_left: int,
    ) -> None:
        """
        Muestra el estado actual del programador.
        """

        print(
            f"\rHora actual: "
            f"{datetime.datetime.now():%H:%M:%S} "
            f"| Reinicio: "
            f"{self._next_restart:%H:%M} "
            f"| Restan {minutes_left} minutos",
            end="",
            flush=True,
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

        message =(
            "AVISO IMPORTANTE\n\n"
            f"El equipo se reiniciará automáticamente en {minutes_left} minutos.\n\n"
            f"¿Deseas posponer 10 minutos?"
       
        )

        response=self._notifier.info(
            "Reinicio Programado",
            message,
        )
        
        if response == self._notifier.IDYES:
            self._next_restart += datetime.timedelta(minutes=10)
            print(f"Nuevo reinicio: {self._next_restart:%H:%M}")
            
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
    
    def reload_schedule(self) -> None:
        """
        Recalcula la siguiente hora de reinicio cuando cambia
        la configuración.
        """
        self._next_restart = self._calculate_next_restart()
        self._notifications_sent.clear()

    def _restart(self) -> None:
        self._system.restart()

        self._next_restart = self._calculate_next_restart()
        self._notifications_sent.clear()