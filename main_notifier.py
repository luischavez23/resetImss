from __future__ import annotations

import datetime
import time

from core.logger import Logger
from core.notifier_window import NotifierWindow
from core.runtime_manager import RuntimeManager


class ResetIMSSNotifier:
    """
    Aplicación visible encargada de mostrar las notificaciones
    en la sesión del usuario.
    """

    NOTIFICATION_MINUTES = (10, 5)
    CHECK_INTERVAL = 5

    def __init__(self) -> None:
        Logger.configure()

        self._runtime = RuntimeManager()
        self._notifications_sent: set[int] = set()
        self._notification_open = False
        self._last_restart: datetime.datetime | None = None

    def run(self) -> None:
        """
        Mantiene activo el monitor de notificaciones.
        """

        Logger.info("ResetIMSSNotifier iniciado.")

        while True:
            try:
                self._check_state()
            except Exception as ex:
                Logger.error(
                    f"Error en ResetIMSSNotifier: {ex}"
                )

            time.sleep(self.CHECK_INTERVAL)

    def _check_state(self) -> None:
        """
        Lee el próximo reinicio publicado por ResetIMSSCore.
        """

        state = self._runtime.load_state()

        if not state:
            return

        restart_value = state.get("next_restart")

        if not restart_value:
            return

        try:
            next_restart = datetime.datetime.fromisoformat(
                restart_value
            )
        except ValueError:
            Logger.warning(
                "La fecha de runtime.json no es válida."
            )
            return

        if self._last_restart != next_restart:
            self._last_restart = next_restart
            self._notifications_sent.clear()

        difference = (
            next_restart - datetime.datetime.now()
        ).total_seconds()

        if difference <= 0:
            return

        minutes_left = max(
            0,
            int((difference + 59) // 60),
        )

        self._show_notification_if_needed(
            minutes_left=minutes_left,
            next_restart=next_restart,
        )

    def _show_notification_if_needed(
        self,
        minutes_left: int,
        next_restart: datetime.datetime,
    ) -> None:

        if minutes_left not in self.NOTIFICATION_MINUTES:
            return

        if minutes_left in self._notifications_sent:
            return

        if self._notification_open:
            return

        self._notification_open = True
        self._notifications_sent.add(minutes_left)

        Logger.info(
            f"Mostrando notificación visible de "
            f"{minutes_left} minutos."
        )

        NotifierWindow.show(
            minutes_left=minutes_left,
            restart_time=next_restart.strftime("%H:%M"),
            on_postpone=self._request_postpone,
            on_close=self._notification_closed,
        )

    def _request_postpone(self) -> None:
        """
        Solicita al Core posponer el reinicio.
        """

        self._runtime.request_postpone(minutes=10)

        Logger.info(
            "Solicitud de posposición enviada al Core."
        )

    def _notification_closed(self) -> None:
        self._notification_open = False


def main() -> None:
    notifier = ResetIMSSNotifier()
    notifier.run()


if __name__ == "__main__":
    main()