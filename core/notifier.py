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
        
        return response
        

    def info(self, title: str, message: str) -> None:
        """
        Muestra un mensaje informativo.
        """
        
        response = self._show(
            title=title,
            message=message,
            icon=self.ICON_INFORMATION,
            window=self.MB_YESNO,
        )
        return response
            
        

    def warning(self, title: str, message: str) -> None:
        """
        Muestra un mensaje de advertencia.
        """
        response = self._show(
            title=title,
            message=message,
            icon=self.ICON_WARNING,
            window=self.MB_OK,
        )
        return response
        
    def confirmation(self, title: str, message: str) -> None:
        """
        Muestra un mensaje de confirmación.
        """
        response = self._show(
            title=title,
            message=message,
            icon=self.ICON_INFORMATION,
            window=self.MB_OK,
        )
        return response

    def error(self, title: str, message: str) -> None:
        """
        Muestra un mensaje de error.
        """
        response = self._show(
            title=title,
            message=message,
            icon=self.ICON_ERROR,
            window=self.MB_OK,
        )
        return response
