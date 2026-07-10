from core.config_manager import ConfigManager
from core.notifier import Notifier
from ui.settings_window import SettingsWindow


def main():

    config = ConfigManager()
    notifier = Notifier()

    app = SettingsWindow(
        notifier=notifier,
        config=config,
    )

    app.run()


if __name__ == "__main__":
    main()