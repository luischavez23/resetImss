from core.config_manager import ConfigManager

config = ConfigManager()

print(config.hour)
print(config.minute)

config.hour = 3
config.minute = 00

print("Guardado")