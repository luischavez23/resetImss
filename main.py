from core.config_manager import ConfigManager
from core.notifier import Notifier
from core.scheduler import Scheduler
from core.system_controller import SystemController
from ui.settings_window import SettingsWindow


def main():

    config = ConfigManager()

    notifier = Notifier()

    system = SystemController(config)

    scheduler = Scheduler(
        config=config,
        notifier=notifier,
        system=system,
    )

    scheduler.start()

    app = SettingsWindow(notifier, config, scheduler.reload_schedule,)

    app.run()


if __name__ == "__main__":
    main()


