from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from typing import Callable

import os

from core.resources import resource_path
from core.logger import Logger


class NotifierWindow:
    """
    Ventana de aviso de reinicio.

    Se ejecuta en un hilo independiente para no bloquear
    el Scheduler.
    """

    @staticmethod
    def show(
        minutes_left: int,
        restart_time: str,
        on_postpone: Callable[[], None],
        on_close: Callable[[], None],
    ) -> None:
        """
        Muestra la ventana sin bloquear el programa.
        """

        thread = threading.Thread(
            target=NotifierWindow._create_window,
            args=(
                minutes_left,
                restart_time,
                on_postpone,
                on_close,
            ),
            daemon=True,
        )

        thread.start()
    
    @staticmethod
    def _create_window(
        minutes_left: int,
        restart_time: str,
        on_postpone: Callable[[], None],
        on_close: Callable[[], None],
    ) -> None:

        root = tk.Tk()

        try:
            icon = resource_path("assets/reiniciar.ico")
            if os.path.exists(icon):
                root.iconbitmap(icon)
        except Exception as ex:
            Logger.error(f"No se pudo cargar el icono: {ex}")

        root.title("ResetIMSS")
        root.resizable(False, False)

        # Siempre al frente
        root.attributes("-topmost", True)
        root.lift()
        root.focus_force()

        # Centrar ventana
        width = 520
        height = 330

        root.update_idletasks()

        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)

        root.geometry(f"{width}x{height}+{x}+{y}")

        # -------------------------------------------------
        # Cierre seguro
        # -------------------------------------------------

        window_closed = False

        def close_window() -> None:
            nonlocal window_closed

            if window_closed:
                return

            window_closed = True

            on_close()

            if root.winfo_exists():
                root.destroy()

        root.protocol(
            "WM_DELETE_WINDOW",
            close_window,
        )

        # -------------------------------------------------
        # Estilos
        # -------------------------------------------------

        style = ttk.Style()

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
        )

        style.configure(
            "Big.TLabel",
            font=("Segoe UI", 22, "bold"),
        )

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
        )

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        # -------------------------------------------------
        # Encabezado
        # -------------------------------------------------

        ttk.Label(
            frame,
            text="⚠ Reinicio Programado",
            style="Title.TLabel",
            anchor="center",
        ).pack()

        ttk.Label(
            frame,
            text="El equipo se reiniciará automáticamente.",
            style="Subtitle.TLabel",
            anchor="center",
        ).pack(pady=(5, 0))

        ttk.Label(
            frame,
            text="Guarda tu trabajo para evitar pérdida de información.",
            style="Subtitle.TLabel",
            anchor="center",
        ).pack(pady=(0, 15))

        ttk.Separator(frame).pack(fill="x", pady=10)

        # -------------------------------------------------
        # Tiempo restante
        # -------------------------------------------------

        ttk.Label(
            frame,
            text="Reinicio en",
            style="Subtitle.TLabel",
        ).pack()

        ttk.Label(
            frame,
            text=f"{minutes_left} minutos",
            style="Big.TLabel",
        ).pack(pady=(0, 15))

        # -------------------------------------------------
        # Botones
        # -------------------------------------------------

        def postpone():
            on_postpone()
            close_window()

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(10, 0))

        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)

        ttk.Button(
            buttons,
            text="✖ Cerrar",
            style="Accent.TButton",
            command=close_window,
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 6),
            ipady=10,
        )

        ttk.Button(
            buttons,
            text="⏳ Posponer 10 minutos",
            style="Accent.TButton",
            command=postpone,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(6, 0),
            ipady=10,
        )

        # -------------------------------------------------
        # Si sigue abierta cuando llegue el aviso de 5
        # minutos, se cierra automáticamente para permitir
        # mostrar la nueva ventana.
        # -------------------------------------------------

        if minutes_left > 5:
            milliseconds = (minutes_left - 5) * 60 * 1000
            root.after(milliseconds, close_window)

        root.mainloop()