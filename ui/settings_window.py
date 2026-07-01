from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core.config_manager import ConfigManager


class SettingsWindow:

    WINDOW_WIDTH = 360
    WINDOW_HEIGHT = 300

    def __init__(self, config: ConfigManager):

        self._config = config

        self.root = tk.Tk()

        self.hour = tk.StringVar(value=self._config.hour)
        self.minute = tk.StringVar(value=self._config.minute)
        self.real_restart = tk.BooleanVar(
            value=self._config.real_restart
        )

        self._configure_window()
        self._build()
        self._center_window()

    # ---------------------------------------------------------
    # Métodos públicos
    # ---------------------------------------------------------

    def run(self) -> None:
        self.root.mainloop()

    # ---------------------------------------------------------
    # Configuración
    # ---------------------------------------------------------

    def _configure_window(self) -> None:

        self.root.title("Reinicio Programado")
        self.root.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}"
        )
        self.root.resizable(False, False)

    def _center_window(self) -> None:

        self.root.update_idletasks()

        width = self.root.winfo_width()
        height = self.root.winfo_height()

        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # ---------------------------------------------------------
    # Construcción de la interfaz
    # ---------------------------------------------------------

    def _build(self) -> None:

        frame = ttk.Frame(
            self.root,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        title = ttk.Label(
            frame,
            text="Configuración del reinicio",
            font=("Segoe UI", 11, "bold")
        )

        title.pack(anchor="w")

        ttk.Separator(frame).pack(
            fill="x",
            pady=(10, 15)
        )

        self._build_time(frame)

        ttk.Checkbutton(
            frame,
            text="Realizar reinicio real",
            variable=self.real_restart
        ).pack(anchor="w", pady=15)

        self.current_label = ttk.Label(
            frame,
            font=("Segoe UI", 9)
        )

        self.current_label.pack(pady=(0, 15))

        ttk.Button(
            frame,
            text="Guardar configuración",
            command=self._save
        ).pack(fill="x")

        self._update_label()

    def _build_time(self, parent) -> None:

        ttk.Label(
            parent,
            text="Hora de reinicio"
        ).pack(anchor="w")

        time_frame = ttk.Frame(parent)

        time_frame.pack(pady=10)

        self.hour_box = ttk.Combobox(
            time_frame,
            textvariable=self.hour,
            state="readonly",
            width=4,
            justify="center",
            values=[f"{i:02}" for i in range(24)]
        )

        self.hour_box.pack(side="left")

        ttk.Label(
            time_frame,
            text=":",
            font=("Segoe UI", 14, "bold")
        ).pack(
            side="left",
            padx=8
        )

        self.minute_box = ttk.Combobox(
            time_frame,
            textvariable=self.minute,
            state="readonly",
            width=4,
            justify="center",
            values=[f"{i:02}" for i in range(60)]
        )

        self.minute_box.pack(side="left")

    # ---------------------------------------------------------
    # Eventos
    # ---------------------------------------------------------

    def _save(self) -> None:

        self._config.hour = int(self.hour.get())
        self._config.minute = int(self.minute.get())
        self._config.real_restart = self.real_restart.get()

        self._update_label()

    def _update_label(self) -> None:

        self.current_label.config(
            text=(
                "Reinicio programado: "
                f"{self._config.hour:02}:"
                f"{self._config.minute:02}"
            )
        )