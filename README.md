# ResetIMSS

Aplicación para programar el reinicio automático de equipos con Windows.

## Funciones

* Configuración de horario en formato de 24 horas.
* Reinicio automático diario.
* Ejecución en segundo plano como servicio de Windows.
* Notificaciones 10 y 5 minutos antes del reinicio.
* Opción para posponer el reinicio 10 minutos.
* Registro de actividad mediante logs diarios.
* Instalador y desinstalador para Windows.

## Componentes

* **ResetIMSSCore:** controla el horario y ejecuta el reinicio.
* **ResetIMSSNotifier:** muestra las notificaciones al usuario.
* **ResetIMSSConfig:** permite modificar el horario de reinicio.

## Archivos de configuración

La configuración y los logs se almacenan en:

```text
C:\ProgramData\ResetIMSS
```

Archivos principales:

```text
config.json
runtime.json
command.json
logs\
```

## Tecnologías

* Python
* Tkinter
* PyInstaller
* WinSW
* Inno Setup

## Compilación

```powershell
pyinstaller --clean ResetIMSSCore.spec
pyinstaller --clean ResetIMSSNotifier.spec
pyinstaller --clean ResetIMSSConfig.spec
```

## Advertencia

El programa puede forzar el cierre de las aplicaciones abiertas durante el reinicio. Se recomienda guardar el trabajo antes de la hora programada.

## Autor

Luis Pablo
