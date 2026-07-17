#define MyAppName "ResetIMSS"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Luis Pablo Chávez"

#define MyConfigExe "ResetIMSSConfig.exe"
#define MyNotifierExe "ResetIMSSNotifier.exe"
#define MyCoreExe "ResetIMSSCore.exe"
#define MyServiceExe "ResetIMSSService.exe"
#define MyServiceXml "ResetIMSSService.xml"


[Setup]
AppId={{B4DF9EB2-5DF6-44A7-A8B9-8C5EFC297A36}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

UninstallDisplayIcon={app}\assets\reiniciar.ico

PrivilegesRequired=admin

ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

OutputDir=output
OutputBaseFilename=ResetIMSS_Setup_{#MyAppVersion}

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

SetupIconFile=..\Release\assets\reiniciar.ico

DisableProgramGroupPage=yes
DisableWelcomePage=no

Uninstallable=yes
CreateUninstallRegKey=yes

CloseApplications=yes
RestartApplications=no
RestartIfNeededByRun=no

VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Sistema de reinicio programado
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}


[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"


[Tasks]
Name: "desktopicon"; \
Description: "Crear un acceso directo en el escritorio"; \
GroupDescription: "Accesos directos adicionales:"; \
Flags: unchecked


[Dirs]
Name: "{commonappdata}\ResetIMSS"; \
Permissions: users-modify

Name: "{commonappdata}\ResetIMSS\logs"; \
Permissions: users-modify


[Files]
Source: "..\Release\{#MyConfigExe}"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "..\Release\{#MyNotifierExe}"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "..\Release\{#MyCoreExe}"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "..\Release\{#MyServiceExe}"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "..\Release\{#MyServiceXml}"; \
DestDir: "{app}"; \
Flags: ignoreversion

Source: "..\Release\assets\reiniciar.ico"; \
DestDir: "{app}\assets"; \
Flags: ignoreversion


[Icons]
Name: "{group}\Configurar ResetIMSS"; \
Filename: "{app}\{#MyConfigExe}"; \
WorkingDir: "{app}"; \
IconFilename: "{app}\assets\reiniciar.ico"

Name: "{group}\Desinstalar ResetIMSS"; \
Filename: "{uninstallexe}"

Name: "{autodesktop}\Configurar ResetIMSS"; \
Filename: "{app}\{#MyConfigExe}"; \
WorkingDir: "{app}"; \
IconFilename: "{app}\assets\reiniciar.ico"; \
Tasks: desktopicon


[Registry]
; Inicia el Notifier cuando un usuario inicia sesión.
Root: HKLM; \
Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
ValueType: string; \
ValueName: "ResetIMSSNotifier"; \
ValueData: """{app}\{#MyNotifierExe}"""; \
Flags: uninsdeletevalue


[Run]
; Detener el servicio anterior solamente si está instalado.
Filename: "{app}\{#MyServiceExe}"; \
Parameters: "stop"; \
WorkingDir: "{app}"; \
Flags: runhidden waituntilterminated; \
StatusMsg: "Deteniendo una versión anterior del servicio..."; \
Check: IsResetIMSSServiceInstalled

; Eliminar el servicio anterior solamente si está instalado.
Filename: "{app}\{#MyServiceExe}"; \
Parameters: "uninstall"; \
WorkingDir: "{app}"; \
Flags: runhidden waituntilterminated; \
StatusMsg: "Actualizando el servicio de ResetIMSS..."; \
Check: IsResetIMSSServiceInstalled

; Instalar el servicio.
Filename: "{app}\{#MyServiceExe}"; \
Parameters: "install"; \
WorkingDir: "{app}"; \
Flags: runhidden waituntilterminated; \
StatusMsg: "Instalando el servicio de ResetIMSS..."

; Iniciar el servicio.
Filename: "{app}\{#MyServiceExe}"; \
Parameters: "start"; \
WorkingDir: "{app}"; \
Flags: runhidden waituntilterminated; \
StatusMsg: "Iniciando el servicio de ResetIMSS..."

; Iniciar automáticamente el Notifier en la sesión del usuario.
Filename: "{app}\{#MyNotifierExe}"; \
WorkingDir: "{app}"; \
Flags: nowait runasoriginaluser

; Permitir abrir la configuración al finalizar.
Filename: "{app}\{#MyConfigExe}"; \
WorkingDir: "{app}"; \
Description: "Configurar el horario de reinicio"; \
Flags: postinstall nowait skipifsilent runasoriginaluser


[UninstallRun]
; Cerrar el Notifier.
Filename: "{sys}\taskkill.exe"; \
Parameters: "/F /IM {#MyNotifierExe}"; \
Flags: runhidden waituntilterminated; \
RunOnceId: "CloseResetIMSSNotifier"

; Detener el servicio.
Filename: "{app}\{#MyServiceExe}"; \
Parameters: "stop"; \
WorkingDir: "{app}"; \
Flags: runhidden waituntilterminated skipifdoesntexist; \
RunOnceId: "StopResetIMSSService"

; Eliminar el servicio.
Filename: "{app}\{#MyServiceExe}"; \
Parameters: "uninstall"; \
WorkingDir: "{app}"; \
Flags: runhidden waituntilterminated skipifdoesntexist; \
RunOnceId: "RemoveResetIMSSService"


[UninstallDelete]
Type: files; \
Name: "{commonappdata}\ResetIMSS\runtime.json"

Type: files; \
Name: "{commonappdata}\ResetIMSS\command.json"

; Se conservan config.json y los archivos de logs.
; Para eliminarlos también, descomenta estas líneas:

; Type: files; Name: "{commonappdata}\ResetIMSS\config.json"
; Type: filesandordirs; Name: "{commonappdata}\ResetIMSS\logs"
; Type: dirifempty; Name: "{commonappdata}\ResetIMSS"


[Code]

function IsResetIMSSServiceInstalled(): Boolean;
begin
  Result := RegKeyExists(
    HKLM,
    'SYSTEM\CurrentControlSet\Services\ResetIMSS'
  );
end;


procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel1.Caption :=
    'Bienvenido al instalador de ResetIMSS';

  WizardForm.WelcomeLabel2.Caption :=
    'Este asistente instalará el servicio de reinicio programado, ' +
    'la aplicación de configuración y el sistema de notificaciones.';
end;


procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssInstall then
  begin
    { Cerrar el Notifier anterior antes de reemplazarlo. }
    Exec(
      ExpandConstant('{sys}\taskkill.exe'),
      '/F /IM ResetIMSSNotifier.exe',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode
    );

    { Detener el servicio anterior antes de copiar los ejecutables. }
    if IsResetIMSSServiceInstalled() then
    begin
      Exec(
        ExpandConstant('{sys}\sc.exe'),
        'stop ResetIMSS',
        '',
        SW_HIDE,
        ewWaitUntilTerminated,
        ResultCode
      );

      Sleep(2000);
    end;
  end;
end;