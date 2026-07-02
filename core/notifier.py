from __future__ import annotations
from typing import Optional
import ctypes


class Notifier:
    """
    Se encarga de mostrar mensajes al usuario mediante
    cuadros de diálogo de windows.
    """

    ICON_ERROR = 0x10
    ICON_WARNING = 0x30
    ICON_INFORMATION = 0x40
    
    MB_OK = 0x0
    MB_YESNO = 0x04
    IDYES = 6
    IDNO = 7

    def _show(
        self,
        title: str,
        message: str,
        icon: int,
        window:Optional[int]=None,
    ) -> None:
        """
        Muestra un cuadro de diálogo de Windows.
        """
        response = ctypes.windll.user32.MessageBoxW(
            0,
            message,
            title,
            window | icon,
        )
        
        if response == self.IDYES:
            print("Click Yes")
        else:
            print("Click Not")

    def info(self, title: str, message: str) -> None:
        """
        Muestra un mensaje informativo.
        """
        self._show(
            title=title,
            message=message,
            icon=self.ICON_INFORMATION,
            window=self.MB_YESNO,
        )
            
        

    def warning(self, title: str, message: str) -> None:
        """
        Muestra un mensaje de advertencia.
        """
        self._show(
            title=title,
            message=message,
            icon=self.ICON_WARNING,
            window=self.MB_OK,
        )

    def error(self, title: str, message: str) -> None:
        """
        Muestra un mensaje de error.
        """
        self._show(
            title=title,
            message=message,
            icon=self.ICON_ERROR,
            window=self.MB_OK,
        )

    def restart_warning(
        self,
        hour: int,
        minute: int,
        minutes_left: int,
    ) -> None:
        """
        Muestra el aviso de reinicio programado.
        """

        message = (
            "AVISO IMPORTANTE\n\n"
            f"El equipo se reiniciará automáticamente a las "
            f"{hour:02}:{minute:02}.\n\n"
            f"Tiempo restante: {minutes_left} minutos.\n\n"
            "Por favor guarde su trabajo y cierre las aplicaciones necesarias."
        )

        self.warning(
            title="Reinicio Programado",
            message=message,
        )