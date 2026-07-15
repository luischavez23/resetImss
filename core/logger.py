from __future__ import annotations

import logging
import os
from pathlib import Path
from datetime import datetime



class Logger:
    """
    Configura y proporciona el logger de la aplicación.
    """

    _logger = logging.getLogger("ResetIMSS")
    _configured = False

    @classmethod
    def configure(cls) -> None:
        """
        Configura el sistema de logs.
        """

        if cls._configured:
            return

        # Carpeta compartida para los logs
        log_dir = Path(os.environ["PROGRAMDATA"]) / "ResetIMSS" / "logs"
        print(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        #log_file = log_dir / "resetimss.log"
        log_file = log_dir / f"resetimss_{datetime.now():%Y-%m-%d}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(
                    log_file,
                    encoding="utf-8"
                ),
                logging.StreamHandler()
            ]
        )

        cls._configured = True

        cls.info(f"Log iniciado: {log_file}")

    @classmethod
    def info(cls, message: str) -> None:
        cls._logger.info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        cls._logger.warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        cls._logger.error(message)