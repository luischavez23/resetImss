from __future__ import annotations

import sys
from pathlib import Path

import servicemanager
import win32event
import win32service
import win32serviceutil

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from main_service import ResetIMSSApp


class ResetIMSSService(win32serviceutil.ServiceFramework):

    _svc_name_ = "ResetIMSS"

    _svc_display_name_ = "ResetIMSS Service"

    _svc_description_ = (
        "Reinicio automático programado del equipo."
    )

    def __init__(self, args):

        super().__init__(args)

        self.stop_event = win32event.CreateEvent(
            None,
            0,
            0,
            None,
        )

        self.app = ResetIMSSApp()

    def SvcStop(self):

        self.ReportServiceStatus(
            win32service.SERVICE_STOP_PENDING
        )

        self.app.stop()

        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):

        servicemanager.LogInfoMsg(
            "ResetIMSS Service iniciado."
        )

        self.app.start()

        while True:

            result = win32event.WaitForSingleObject(
                self.stop_event,
                1000,
            )

            if result == win32event.WAIT_OBJECT_0:
                break

        servicemanager.LogInfoMsg(
            "ResetIMSS Service detenido."
        )


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(
        ResetIMSSService
    )